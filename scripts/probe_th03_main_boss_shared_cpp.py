#!/usr/bin/env python3
"""Compile the maintained shared boss C++ producer and compare target code shape."""

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
SOURCE = ROOT / "src/main/boss/shared.cpp"
HEADER = "src/main/boss/shared.hpp"
OVERLAY = Path("th03/ba_share.cpp")
OBJECT = Path("obj/th03/ba_share.obj")
TARGET_SEGMENT = 0x0F1F
TARGET_OFFSET = 0x000A
TARGET_SIZE = 0x03B5

SUPPORT = (
    HEADER,
    "src/main/math/polar.hpp",
    "src/main/player/combo.hpp",
    "src/main/player/score_add.hpp",
    "compat/rec98/th03/common.h",
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/player/gba.hpp",
    "compat/rec98/th03/main/sprite16.hpp",
    "compat/rec98/th03/main/playfld.hpp",
    "compat/rec98/th03/math/randring.hpp",
    "compat/rec98/th03/math/vector.hpp",
    "compat/rec98/th02/snd/snd.h",
)

FUNCTIONS = (
    ("boss_explosion_ring", 0x0000, 348, "ret", "6"),
    ("boss_move_sine", 0x015C, 83, "ret", ""),
    ("boss_fall", 0x01AF, 89, "ret", ""),
    ("boss_update_start", 0x0208, 178, "ret", ""),
    ("boss_hittest_end", 0x02BA, 94, "retf", ""),
    ("boss_target_update", 0x0318, 27, "ret", ""),
    ("boss_pattern_next", 0x0333, 95, "ret", ""),
    ("boss_explosion_render", 0x0392, 35, "ret", ""),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode(blob: bytes, base: int = 0) -> list:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, base))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError(
            f"Capstone did not cover complete shared boss function at 0x{base:X}"
        )
    return insns


def normalized_shape(insns: list, base: int) -> list[tuple[int, int, str]]:
    """Normalize only TLINK's five-byte far-to-near call relaxation."""
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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.run_id):
        raise ValueError("invalid run id")

    out = ROOT / ".analysis/th03-main-boss-shared-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/boss/shared.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_boss_shared_cpp.py",
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
    (work / OVERLAY).parent.mkdir(parents=True, exist_ok=True)
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
        r"-nobj/th03/ th03/ba_share.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")

    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("shared boss probe used the wrong compiler producer")
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
        raise ValueError(f"unexpected shared boss CODE segments: {nonempty_code}")

    code_segment = nonempty_code[0]
    candidate, ledata = code_bytes(raw, int(code_segment["index"]))
    publics = code_publics(raw, int(code_segment["index"]))
    starts = sorted({offset for offset, _ in publics})
    expected_starts = [offset for _, offset, _, _, _ in FUNCTIONS]

    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    target = target_image[target_start:target_start + TARGET_SIZE]

    differences = []
    if len(starts) == len(FUNCTIONS):
        for i, (name, target_offset, target_size, ret_mnemonic, ret_operand) in enumerate(FUNCTIONS):
            cand_start = starts[i]
            cand_end = starts[i + 1] if i + 1 < len(starts) else len(candidate)
            cand_blob = candidate[cand_start:cand_end]
            target_blob = target[target_offset:target_offset + target_size]
            cand_insns = decode(cand_blob, cand_start)
            target_insns = decode(target_blob, target_offset)
            cand_shape = normalized_shape(cand_insns, cand_start)
            target_shape = normalized_shape(target_insns, target_offset)
            last = cand_insns[-1]
            first = None
            for index, (left, right) in enumerate(zip(cand_shape, target_shape)):
                if left != right:
                    first = {"instruction_index": index, "candidate": left, "target": right}
                    break
            if first is None and len(cand_shape) != len(target_shape):
                index = min(len(cand_shape), len(target_shape))
                first = {
                    "instruction_index": index,
                    "candidate": None if index >= len(cand_shape) else cand_shape[index],
                    "target": None if index >= len(target_shape) else target_shape[index],
                }
            row = {
                "name": name,
                "candidate_start": cand_start,
                "target_start": target_offset,
                "candidate_size": len(cand_blob),
                "target_size": target_size,
                "candidate_instruction_count": len(cand_insns),
                "target_instruction_count": len(target_insns),
                "linker_normalized_shape_equal": cand_shape == target_shape,
                "first_shape_difference": first,
                "candidate_return": [last.mnemonic, last.op_str],
                "target_return": [ret_mnemonic, ret_operand],
            }
            if (
                len(cand_blob) != target_size
                or cand_shape != target_shape
                or last.mnemonic != ret_mnemonic
                or last.op_str != ret_operand
            ):
                differences.append(row)
    else:
        differences.append({
            "name": "<public-start-count>",
            "candidate_starts": starts,
            "target_starts": expected_starts,
        })

    bss = [
        segment for segment in segments
        if segment["class"] == "BSS" and segment["size"]
    ]
    accepted = (
        len(candidate) == TARGET_SIZE
        and starts == expected_starts
        and not differences
        and not bss
    )
    report = {
        "kind": "th03-main-shared-boss-cpp-producer-shape",
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
            "code_publics": [{"offset": offset, "name": name} for offset, name in publics],
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
                left != right for left, right in zip(candidate, target)
            ) + abs(len(candidate) - len(target)),
        },
        "source_acceptance": accepted,
        "exact_acceptance": False,
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    if not accepted:
        raise ValueError(
            "shared boss producer shape differs: "
            f"candidate={len(candidate)} target={TARGET_SIZE}; "
            f"starts={starts}; first_difference={differences[0] if differences else None}"
        )

    print(
        "Shared boss TC4J producer shape: PASS; "
        f"{TARGET_SIZE} bytes / {len(FUNCTIONS)} functions / zero BSS"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
