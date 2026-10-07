#!/usr/bin/env python3
"""Compile the maintained Marisa boss C++ producer and compare target code shape."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tomllib

import capstone

from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from probe_th03_main_bomb_rikako_cpp import code_bytes, segment_definitions

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
SOURCE = ROOT / "src/main/boss/marisa.cpp"
HEADER = "src/main/boss/marisa.hpp"
OVERLAY = Path("th03/ba_maris.cpp")
OBJECT = Path("obj/th03/ba_maris.obj")
TARGET_SEGMENT = 0x0F1F
TARGET_OFFSET = 0x03BF
TARGET_SIZE = 0x0597
TARGET_TABLE_START = 0x03A6
TARGET_TABLE_END = 0x03F7

SUPPORT = (
    HEADER,
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/player/gba.hpp",
    "compat/rec98/th03/main/bullet/bullet.hpp",
    "compat/rec98/th03/main/collmap.hpp",
    "compat/rec98/th03/main/hitbox.hpp",
    "compat/rec98/th03/main/sprite16.hpp",
    "compat/rec98/th03/main/playfld.hpp",
    "compat/rec98/th03/math/randring.hpp",
    "compat/rec98/th02/snd/snd.h",
    "compat/rec98/libs/sprite16/sprite16.h",
)

# Relative to the Marisa owner, excluding the compiler switch table.
FUNCTIONS = (
    ("boss_marisa_template_init", 0x0000, 79, "retf", "2"),
    ("marisa_pattern_spread", 0x004F, 135, "ret", ""),
    ("marisa_pattern_columns_wide", 0x00D6, 168, "ret", ""),
    ("marisa_pattern_ring", 0x017E, 144, "ret", ""),
    ("marisa_pattern_columns_narrow", 0x020E, 139, "ret", ""),
    ("gba_boss_update_marisa", 0x0299, 269, "retf", ""),
    ("marisa_render_main", 0x03F7, 203, "ret", ""),
    ("marisa_render_split", 0x04C2, 119, "ret", "2"),
    ("gba_boss_render_marisa", 0x0539, 94, "retf", ""),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(blob: bytes, base: int = 0) -> list:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, base))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError(
            f"Capstone did not cover complete function image at 0x{base:X}: "
            f"{sum(insn.size for insn in insns)} != {len(blob)}"
        )
    return insns


def shape(insns: list, base: int) -> list[tuple[int, int, str]]:
    return [(insn.address - base, insn.size, insn.mnemonic) for insn in insns]


def linker_normalized_shape(insns: list, base: int) -> list[tuple[int, int, str]]:
    """Normalize the TLINK far-to-near relaxation without masking bytes.

    A compiler-emitted five-byte far CALL to a symbol that ends up in the same
    code segment is relaxed by TLINK to NOP; PUSH CS; CALL near.  The span and
    call semantics stay five bytes; raw linked bytes remain a later full-link
    gate.
    """
    result = []
    i = 0
    while i < len(insns):
        insn = insns[i]
        if insn.mnemonic == "lcall" and insn.size == 5:
            result.append((insn.address - base, 5, "link-relaxed-far-call"))
            i += 1
            continue
        if (
            i + 2 < len(insns)
            and insn.mnemonic == "nop"
            and insn.size == 1
            and insns[i + 1].mnemonic == "push"
            and insns[i + 1].op_str == "cs"
            and insns[i + 1].size == 1
            and insns[i + 2].mnemonic == "call"
            and insns[i + 2].size == 3
            and insns[i + 1].address == insn.address + 1
            and insns[i + 2].address == insn.address + 2
        ):
            result.append((insn.address - base, 5, "link-relaxed-far-call"))
            i += 3
            continue
        result.append((insn.address - base, insn.size, insn.mnemonic))
        i += 1
    return result


def read_index(data: bytes, at: int) -> tuple[int, int]:
    if at >= len(data):
        raise ValueError("truncated OMF index")
    first = data[at]
    at += 1
    if first & 0x80:
        if at >= len(data):
            raise ValueError("truncated two-byte OMF index")
        return (((first & 0x7F) << 8) | data[at], at + 1)
    return (first, at)


def code_publics(raw: bytes, segment_index: int) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for record in parse_omf(raw):
        if record.record_type not in {0x90, 0xB6}:
            continue
        data = record.data
        group, at = read_index(data, 0)
        segment, at = read_index(data, at)
        if segment == 0:
            if at + 2 > len(data):
                raise ValueError("truncated absolute PUBDEF frame")
            at += 2
        while at < len(data):
            width = data[at]
            at += 1
            if at + width + 2 > len(data):
                raise ValueError("truncated PUBDEF symbol")
            name = data[at:at + width].decode("ascii", errors="backslashreplace")
            at += width
            offset = int.from_bytes(data[at:at + 2], "little")
            at += 2
            _, at = read_index(data, at)
            if segment == segment_index:
                result.append((offset, name))
    result.sort()
    return result


def split_candidate_functions(candidate: bytes, starts: list[int]) -> tuple[list[bytes], tuple[int, int]]:
    if len(starts) != len(FUNCTIONS):
        raise ValueError(
            f"Marisa producer public function count differs: {len(starts)} != {len(FUNCTIONS)}; "
            f"starts={starts}"
        )
    functions: list[bytes] = []
    update_index = 5
    table_span = None
    for i, start in enumerate(starts):
        if i == update_index:
            cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
            cursor = start
            end = None
            for insn in cs.disasm(candidate[start:], start):
                cursor = insn.address + insn.size
                if insn.mnemonic == "retf":
                    end = cursor
                    break
            if end is None:
                raise ValueError("candidate Marisa update has no RETF")
            functions.append(candidate[start:end])
            next_start = starts[i + 1]
            if end > next_start:
                raise ValueError("candidate Marisa update overlaps next public")
            table_span = (end, next_start)
        else:
            end = starts[i + 1] if i + 1 < len(starts) else len(candidate)
            functions.append(candidate[start:end])
    assert table_span is not None
    return functions, table_span


def target_function_blobs(target: bytes) -> list[bytes]:
    return [
        target[offset:offset + size]
        for _, offset, size, _, _ in FUNCTIONS
    ]


def table_structure(blob: bytes, owner_base: int) -> dict:
    if len(blob) != 81:
        return {"size": len(blob), "valid": False}
    if blob[0] != 0:
        return {"size": len(blob), "valid": False, "alignment_byte": blob[0]}
    keys = struct.unpack_from("<20H", blob, 1)
    destinations = struct.unpack_from("<20H", blob, 41)
    expected_keys = tuple(range(0x12)) + (0x80, 0xFF)
    return {
        "size": len(blob),
        "valid": keys == expected_keys,
        "alignment_byte": blob[0],
        "keys": list(keys),
        "destinations_owner_relative": [value - owner_base for value in destinations],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.run_id):
        raise ValueError("invalid run id")

    out = ROOT / ".analysis/th03-main-boss-marisa-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/boss/marisa.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_boss_marisa_cpp.py",
        "config/toolchain.toml",
        "config/targets.toml",
        "scripts/lib/omf.py",
        "scripts/lib/pc98.py",
        "scripts/lib/targets.py",
    ):
        inputs[path] = sha((ROOT / path).read_bytes())

    archive = out / "reference.tar"
    subprocess.run(
        ["git", "archive", "--format=tar", f"--output={archive}", revision],
        cwd=REFERENCE,
        check=True,
    )
    work = out / "source"
    work.mkdir()
    subprocess.run(["tar", "-xf", str(archive), "-C", str(work)], check=True)
    (work / OVERLAY).write_bytes(SOURCE.read_bytes())
    for name in SUPPORT:
        destination = work / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((ROOT / name).read_bytes())
    (work / "obj/th03").mkdir(parents=True, exist_ok=True)

    tool = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    env = os.environ.copy()
    env.update(
        DISPLAY="",
        WAYLAND_DISPLAY="",
        WINEDEBUG="-all",
        WINEPREFIX=str(ROOT / tool["paths"]["wine_prefix"]),
        MSDOS_PATH=r"C:\TC4\BIN",
    )
    command = [
        "wine", "cmd", "/d", "/c",
        r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
        r"&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=3 -ml "
        r"-a2 -nobj/th03/ th03/ba_maris.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")

    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("Marisa boss probe used the wrong compiler producer")
    segments = segment_definitions(raw)
    nonempty_code = [
        segment for segment in segments
        if segment["class"] == "CODE" and segment["size"]
    ]
    if (
        len(nonempty_code) != 1
        or nonempty_code[0]["name"] != "MAIN_03_TEXT"
        or nonempty_code[0]["overlay"] != ""
    ):
        raise ValueError(f"unexpected Marisa boss CODE segments: {nonempty_code}")

    code_segment = nonempty_code[0]
    candidate, ledata = code_bytes(raw, int(code_segment["index"]))
    publics = code_publics(raw, int(code_segment["index"]))
    starts = sorted({offset for offset, _ in publics})
    candidate_functions, candidate_table_span = split_candidate_functions(candidate, starts)

    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    target = target_image[target_start:target_start + TARGET_SIZE]
    if len(target) != TARGET_SIZE:
        raise ValueError("target Marisa boss extent is truncated")

    target_functions = target_function_blobs(target)
    differences = []
    for i, ((name, target_offset, target_size, ret_mnemonic, ret_operand), cand_blob, target_blob) in enumerate(
        zip(FUNCTIONS, candidate_functions, target_functions)
    ):
        cand_start = starts[i]
        cand_insns = decode(cand_blob, cand_start)
        target_insns = decode(target_blob, target_offset)
        cand_shape = shape(cand_insns, cand_start)
        targ_shape = shape(target_insns, target_offset)
        cand_link_shape = linker_normalized_shape(cand_insns, cand_start)
        targ_link_shape = linker_normalized_shape(target_insns, target_offset)
        first = None
        for index, (left, right) in enumerate(zip(cand_link_shape, targ_link_shape)):
            if left != right:
                first = {"instruction_index": index, "candidate": left, "target": right}
                break
        if first is None and len(cand_link_shape) != len(targ_link_shape):
            first = {
                "instruction_index": min(len(cand_link_shape), len(targ_link_shape)),
                "candidate": None if len(cand_link_shape) <= len(targ_link_shape) else cand_link_shape[len(targ_link_shape)],
                "target": None if len(targ_link_shape) <= len(cand_link_shape) else targ_link_shape[len(cand_link_shape)],
            }
        last = cand_insns[-1]
        row = {
            "name": name,
            "candidate_start": cand_start,
            "target_start": target_offset,
            "candidate_size": len(cand_blob),
            "target_size": target_size,
            "candidate_instruction_count": len(cand_insns),
            "target_instruction_count": len(target_insns),
            "raw_instruction_shape_equal": cand_shape == targ_shape,
            "linker_normalized_shape_equal": cand_link_shape == targ_link_shape,
            "first_shape_difference": first,
            "candidate_return": [last.mnemonic, last.op_str],
            "target_return": [ret_mnemonic, ret_operand],
        }
        if (
            len(cand_blob) != target_size
            or cand_link_shape != targ_link_shape
            or last.mnemonic != ret_mnemonic
            or last.op_str != ret_operand
        ):
            differences.append(row)

    cand_table = candidate[candidate_table_span[0]:candidate_table_span[1]]
    target_table = target[TARGET_TABLE_START:TARGET_TABLE_END]
    cand_table_info = table_structure(cand_table, 0)
    target_table_info = table_structure(target_table, TARGET_OFFSET)
    table_semantics_equal = (
        cand_table_info.get("valid") is True
        and target_table_info.get("valid") is True
        and cand_table_info.get("keys") == target_table_info.get("keys")
        and cand_table_info.get("destinations_owner_relative")
        == target_table_info.get("destinations_owner_relative")
    )

    bss = [
        segment for segment in segments
        if segment["class"] == "BSS" and segment["size"]
    ]
    fixupp = [
        {"record_index": index, "size": len(record.data), "sha256": sha(record.data)}
        for index, record in enumerate(parse_omf(raw))
        if record.name == "FIXUPP"
    ]

    accepted = (
        len(candidate) == TARGET_SIZE
        and starts == [offset for _, offset, _, _, _ in FUNCTIONS]
        and not differences
        and candidate_table_span == (TARGET_TABLE_START, TARGET_TABLE_END)
        and table_semantics_equal
        and not bss
    )
    report = {
        "kind": "th03-main-marisa-boss-cpp-producer-shape",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "reference_revision": revision,
        "target_sha256": sha(target_raw),
        "inputs": inputs,
        "build": build,
        "object": {
            "path": str(OBJECT),
            "sha256": sha(raw),
            "module_name": omf["module_name"],
            "translator_comments": omf["translator_comments"],
            "record_counts": omf["record_counts"],
            "segments": segments,
            "code_size": len(candidate),
            "bss_size": sum(segment["size"] for segment in bss),
            "ledata": ledata,
            "fixupp": fixupp,
            "code_publics": [{"offset": offset, "name": name} for offset, name in publics],
        },
        "comparison": {
            "target_segment": TARGET_SEGMENT,
            "target_offset": TARGET_OFFSET,
            "target_size": TARGET_SIZE,
            "candidate_size": len(candidate),
            "candidate_function_starts": starts,
            "target_function_starts": [offset for _, offset, _, _, _ in FUNCTIONS],
            "function_differences": differences,
            "candidate_table_span": list(candidate_table_span),
            "target_table_span": [TARGET_TABLE_START, TARGET_TABLE_END],
            "candidate_table": cand_table_info,
            "target_table": target_table_info,
            "table_raw_equal_before_link": cand_table == target_table,
            "table_semantics_equal": table_semantics_equal,
            "raw_differing_bytes_before_link": sum(
                left != right for left, right in zip(candidate, target)
            ) + abs(len(candidate) - len(target)),
        },
        "source_acceptance": accepted,
        "exact_acceptance": False,
        "notes": (
            "Object-level TC4J producer proof only. Full-link MAP placement, "
            "historical DATA/BSS ownership and ordered MZ relocations remain separate gates."
        ),
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    if not accepted:
        first = differences[0] if differences else None
        raise ValueError(
            "Marisa boss producer shape differs: "
            f"candidate={len(candidate)} target={TARGET_SIZE}; "
            f"starts={starts}; table={candidate_table_span}; "
            f"first_function_difference={first}"
        )

    for path, before in inputs.items():
        if sha((ROOT / path).read_bytes()) != before:
            raise ValueError("probe input changed during run: " + path)

    print(
        "Marisa boss TC4J producer shape: PASS; "
        f"{TARGET_SIZE} bytes; {len(FUNCTIONS)} functions + {len(cand_table)} switch bytes"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
