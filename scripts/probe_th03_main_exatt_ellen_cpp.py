#!/usr/bin/env python3
"""Compile the Ellen Extra Attack TC4J producer and compare target code shape."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
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
SOURCE = ROOT / "src/main/player/exatt_ellen.cpp"
HEADER = "src/main/player/exatt_ellen.hpp"
OVERLAY = Path("th03/ex_ellen.cpp")
OBJECT = Path("obj/th03/ex_ellen.obj")
TARGET_SEGMENT = 0x18FE
TARGET_OFFSET = 0x040F
TARGET_SIZE = 0x0436

SUPPORT = (
    HEADER,
    "compat/rec98/th03/common.h",
    "src/main/math/polar.hpp",
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/collmap.hpp",
    "compat/rec98/th03/main/hitbox.hpp",
    "compat/rec98/th03/main/sprite16.hpp",
    "compat/rec98/th03/main/playfld.hpp",
    "compat/rec98/th03/math/randring.hpp",
    "compat/rec98/th03/math/vector.hpp",
    "compat/rec98/th02/snd/snd.h",
    "compat/rec98/libs/master.lib/master.hpp",
    "compat/rec98/libs/master.lib/pc98_gfx.hpp",
    "compat/rec98/libs/sprite16/sprite16.h",
)

# semantic name, owner-relative start, size, return mnemonic, operand
FUNCTIONS = (
    ("exatt_add_ellen", 0x0000, 186, "retf", "6"),
    ("ellen_extra_add", 0x00BA, 103, "retf", "8"),
    ("ellen_exatt_render_one", 0x0121, 269, "ret", ""),
    ("exatt_update_ellen", 0x022E, 470, "retf", ""),
    ("exatt_render_ellen", 0x0404, 50, "retf", ""),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_index(data: bytes, at: int) -> tuple[int, int]:
    first = data[at]
    at += 1
    if first & 0x80:
        return (((first & 0x7F) << 8) | data[at], at + 1)
    return (first, at)


def code_publics(raw: bytes, segment_index: int) -> list[tuple[int, str]]:
    result = []
    for record in parse_omf(raw):
        if record.record_type not in {0x90, 0xB6}:
            continue
        data = record.data
        _, at = read_index(data, 0)
        segment, at = read_index(data, at)
        if segment == 0:
            at += 2
        while at < len(data):
            width = data[at]
            at += 1
            name = data[at:at + width].decode("ascii", errors="backslashreplace")
            at += width
            offset = int.from_bytes(data[at:at + 2], "little")
            at += 2
            _, at = read_index(data, at)
            if segment == segment_index:
                result.append((offset, name))
    return sorted(result)


def decode(blob: bytes, base: int) -> list:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, base))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError(
            f"incomplete Capstone decode at 0x{base:X}: "
            f"{sum(insn.size for insn in insns)} != {len(blob)}"
        )
    return insns


def shape(insns: list, base: int) -> list[tuple[int, int, str]]:
    return [(i.address - base, i.size, i.mnemonic) for i in insns]


def linker_normalized_shape(insns: list, base: int) -> list[tuple[int, int, str]]:
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.run_id):
        raise ValueError("invalid run id")

    out = ROOT / ".analysis/th03-main-exatt-ellen-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/player/exatt_ellen.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_exatt_ellen_cpp.py",
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
        dst = work / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((ROOT / name).read_bytes())
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
        r"-a2 -nobj/th03/ th03/ex_ellen.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")

    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("Ellen Extra Attack probe used the wrong compiler")
    segments = segment_definitions(raw)
    nonempty_code = [
        s for s in segments if s["class"] == "CODE" and s["size"]
    ]
    if (
        len(nonempty_code) != 1
        or nonempty_code[0]["name"] != "P_EXATT_TEXT"
        or nonempty_code[0]["overlay"] != ""
    ):
        raise ValueError(f"unexpected Ellen Extra Attack CODE segments: {nonempty_code}")

    code_segment = nonempty_code[0]
    candidate, ledata = code_bytes(raw, int(code_segment["index"]))
    publics = code_publics(raw, int(code_segment["index"]))
    starts = sorted({offset for offset, _ in publics})

    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    target = target_image[target_start:target_start + TARGET_SIZE]
    if len(target) != TARGET_SIZE:
        raise ValueError("target Ellen Extra Attack extent is truncated")

    expected_starts = [x[1] for x in FUNCTIONS]
    candidate_blobs = []
    if len(starts) == len(FUNCTIONS):
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else len(candidate)
            candidate_blobs.append(candidate[start:end])

    differences = []
    if len(candidate_blobs) == len(FUNCTIONS):
        for i, (spec, cand_blob) in enumerate(zip(FUNCTIONS, candidate_blobs)):
            name, target_offset, target_size, ret_mnemonic, ret_operand = spec
            target_blob = target[target_offset:target_offset + target_size]
            cand_start = starts[i]
            cand_insns = decode(cand_blob, cand_start)
            target_insns = decode(target_blob, target_offset)
            cand_shape = linker_normalized_shape(cand_insns, cand_start)
            targ_shape = linker_normalized_shape(target_insns, target_offset)
            first = None
            for index, (left, right) in enumerate(zip(cand_shape, targ_shape)):
                if left != right:
                    first = {
                        "instruction_index": index,
                        "candidate": left,
                        "target": right,
                    }
                    break
            if first is None and len(cand_shape) != len(targ_shape):
                first = {
                    "instruction_index": min(len(cand_shape), len(targ_shape)),
                    "candidate": None if len(cand_shape) <= len(targ_shape) else cand_shape[len(targ_shape)],
                    "target": None if len(targ_shape) <= len(cand_shape) else targ_shape[len(cand_shape)],
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
                "linker_normalized_shape_equal": cand_shape == targ_shape,
                "first_shape_difference": first,
                "candidate_return": [last.mnemonic, last.op_str],
                "target_return": [ret_mnemonic, ret_operand],
            }
            if (
                len(cand_blob) != target_size
                or cand_shape != targ_shape
                or last.mnemonic != ret_mnemonic
                or last.op_str != ret_operand
            ):
                differences.append(row)

    bss = [s for s in segments if s["class"] == "BSS" and s["size"]]
    fixupp = [
        {"record_index": i, "size": len(r.data), "sha256": sha(r.data)}
        for i, r in enumerate(parse_omf(raw))
        if r.name == "FIXUPP"
    ]

    accepted = (
        len(candidate) == TARGET_SIZE
        and starts == expected_starts
        and len(candidate_blobs) == len(FUNCTIONS)
        and not differences
        and not bss
    )
    report = {
        "kind": "th03-main-exatt-ellen-cpp-producer-shape",
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
            "bss_size": sum(s["size"] for s in bss),
            "ledata": ledata,
            "fixupp": fixupp,
            "code_publics": [{"offset": o, "name": n} for o, n in publics],
        },
        "comparison": {
            "target_segment": TARGET_SEGMENT,
            "target_offset": TARGET_OFFSET,
            "target_size": TARGET_SIZE,
            "candidate_size": len(candidate),
            "candidate_function_starts": starts,
            "target_function_starts": expected_starts,
            "function_differences": differences,
            "raw_differing_bytes_before_link": sum(
                a != b for a, b in zip(candidate, target)
            ) + abs(len(candidate) - len(target)),
        },
        "source_acceptance": accepted,
        "exact_acceptance": False,
        "notes": (
            "Object-level TC4J producer proof only. Full-link MAP placement, "
            "historical DATA/BSS ownership and ordered MZ relocations are separate gates."
        ),
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    if not accepted:
        first = differences[0] if differences else None
        raise ValueError(
            "Ellen Extra Attack producer shape differs: "
            f"candidate={len(candidate)} target={TARGET_SIZE}; starts={starts}; "
            f"first_function_difference={first}"
        )

    for path, before in inputs.items():
        if sha((ROOT / path).read_bytes()) != before:
            raise ValueError("probe input changed during run: " + path)

    print(
        "Ellen Extra Attack TC4J producer shape: PASS; "
        f"{TARGET_SIZE} bytes; {len(FUNCTIONS)} functions"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
