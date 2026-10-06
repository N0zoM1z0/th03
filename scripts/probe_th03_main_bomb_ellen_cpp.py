#!/usr/bin/env python3
"""Compile the maintained Ellen bomb C++ producer and compare its code shape."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tomllib

import capstone

from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
SOURCE = ROOT / "src/main/player/bomb_ellen.cpp"
OVERLAY = Path("th03/b_ellen.cpp")
OBJECT = Path("obj/th03/b_ellen.obj")
TARGET_SEGMENT = 0x183C
TARGET_OFFSET = 0x01EB
SUPPORT = (
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/player/bomb.hpp",
    "compat/rec98/th03/main/sprite16.hpp",
    "compat/rec98/th03/math/vector.hpp",
    "compat/rec98/th03/math/randring.hpp",
    "compat/rec98/th02/snd/snd.h",
    "compat/rec98/th03/formats/mrs.hpp",
    "compat/rec98/th03/hardware/palette.hpp",
    "compat/rec98/libs/master.lib/pc98_gfx.hpp",
)
FUNCTIONS = (
    ("ellen_bomb_update", 280, "retf"),
    ("ellen_bomb_render", 163, "ret"),
    ("ellen_bomb", 580, "retf"),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def omf_index(data: bytes, pos: int = 0) -> tuple[int, int]:
    first = data[pos]
    if first & 0x80:
        return (((first & 0x7F) << 8) | data[pos + 1], pos + 2)
    return (first, pos + 1)


def code_bytes(raw: bytes) -> tuple[bytes, list[dict]]:
    parts = []
    for record_index, record in enumerate(parse_omf(raw)):
        if record.name != "LEDATA":
            continue
        segment, pos = omf_index(record.data)
        offset = int.from_bytes(record.data[pos:pos + 2], "little")
        payload = record.data[pos + 2:]
        parts.append((segment, offset, payload, record_index))
    by_segment: dict[int, list[tuple[int, bytes, int]]] = {}
    for segment, offset, payload, record_index in parts:
        by_segment.setdefault(segment, []).append((offset, payload, record_index))
    # TC4J emits this module's code in segment index 1. Keep this assertion
    # explicit so a producer-shape change cannot silently move the evidence.
    selected = by_segment.get(1)
    if not selected:
        raise ValueError("Ellen object has no TC4J code LEDATA in segment index 1")
    end = max(offset + len(payload) for offset, payload, _ in selected)
    image = bytearray(end)
    coverage = bytearray(end)
    receipt_parts = []
    for offset, payload, record_index in selected:
        for i in range(offset, offset + len(payload)):
            coverage[i] += 1
        image[offset:offset + len(payload)] = payload
        receipt_parts.append({
            "record_index": record_index,
            "offset": offset,
            "size": len(payload),
            "sha256": sha(payload),
        })
    if not coverage or any(value != 1 for value in coverage):
        raise ValueError("Ellen code LEDATA is gapped or overlapping")
    return bytes(image), receipt_parts


def instruction_signature(blob: bytes) -> tuple[list[dict], list[tuple[int, int, str]]]:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, 0))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError("Capstone did not cover complete Ellen code image")
    rows = [
        {
            "offset": insn.address,
            "size": insn.size,
            "mnemonic": insn.mnemonic,
        }
        for insn in insns
    ]
    signature = [(insn.address, insn.size, insn.mnemonic) for insn in insns]
    return rows, signature


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", args.run_id):
        raise ValueError("invalid run id")

    out = ROOT / ".analysis/th03-main-bomb-ellen-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/player/bomb_ellen.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_bomb_ellen_cpp.py",
        "config/toolchain.toml",
        "config/targets.toml",
        "config/th03_main_exact_units.toml",
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
        r"-nobj/th03/ th03/b_ellen.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")
    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("Ellen probe used the wrong compiler producer")
    segdef_sizes = [
        int.from_bytes(record.data[1:3], "little")
        for record in parse_omf(raw)
        if record.name == "SEGDEF"
    ]
    if segdef_sizes != [1023, 0, 132]:
        raise ValueError(f"unexpected Ellen CODE/DATA/BSS segment sizes: {segdef_sizes}")

    candidate, ledata = code_bytes(raw)
    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    expected_size = sum(size for _, size, _ in FUNCTIONS)
    target = target_image[target_start:target_start + expected_size]
    if len(target) != expected_size or len(candidate) != expected_size:
        raise ValueError(
            f"Ellen size mismatch: candidate={len(candidate)} target={len(target)} "
            f"expected={expected_size}"
        )

    candidate_rows, candidate_signature = instruction_signature(candidate)
    target_rows, target_signature = instruction_signature(target)
    if candidate_signature != target_signature:
        for index, (left, right) in enumerate(zip(candidate_signature, target_signature)):
            if left != right:
                raise ValueError(
                    f"Ellen instruction shape differs at instruction {index}: "
                    f"candidate={left} target={right}"
                )
        raise ValueError("Ellen instruction shape differs in instruction count")

    expected_end = 0
    expected_returns = []
    for name, size, return_mnemonic in FUNCTIONS:
        expected_end += size
        expected_returns.append({
            "name": name,
            "end": expected_end,
            "return_offset": expected_end - 1,
            "return_mnemonic": return_mnemonic,
        })
    return_rows = [
        row for row in candidate_rows if row["mnemonic"] in {"ret", "retf"}
    ]
    if [
        (row["offset"], row["mnemonic"]) for row in return_rows
    ] != [
        (row["return_offset"], row["return_mnemonic"]) for row in expected_returns
    ]:
        raise ValueError("Ellen ABI/function boundaries differ")

    fixupp = [
        {
            "record_index": index,
            "size": len(record.data),
            "sha256": sha(record.data),
            "payload_hex": record.data.hex(),
        }
        for index, record in enumerate(parse_omf(raw))
        if record.name == "FIXUPP"
    ]
    report = {
        "kind": "th03-main-bomb-ellen-cpp-producer-shape",
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
            "segment_sizes": {
                "code": segdef_sizes[0],
                "data": segdef_sizes[1],
                "bss": segdef_sizes[2],
            },
            "private_bss_layout": {
                "particle_spawn_count": [0, 2],
                "particles": [2, 128],
                "particle_p": [130, 2],
            },
            "ledata": ledata,
            "fixupp": fixupp,
        },
        "comparison": {
            "target_segment": TARGET_SEGMENT,
            "target_offset": TARGET_OFFSET,
            "size": expected_size,
            "candidate_sha256": sha(candidate),
            "target_sha256": sha(target),
            "raw_differing_bytes_before_link": sum(
                left != right for left, right in zip(candidate, target)
            ),
            "instruction_count": len(candidate_rows),
            "instruction_shape_equal": True,
            "function_boundaries": expected_returns,
        },
        "source_acceptance": True,
        "exact_acceptance": False,
        "notes": (
            "Fresh TC4J object-level producer proof only. The 1023-byte Ellen "
            "candidate exactly matches the target's decoded instruction offsets, "
            "sizes, mnemonics, and three ABI boundaries. Unresolved OMF fixup/data "
            "operands are intentionally not treated as raw linked equality. "
            "Promotion still requires private-BSS placement plus full MAIN_05_TEXT "
            "link/MAP/MZ relocation-order acceptance."
        ),
    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    for path, before in inputs.items():
        if sha((ROOT / path).read_bytes()) != before:
            raise ValueError("probe input changed during run: " + path)

    print(
        "Ellen TC4J producer shape: PASS; "
        f"{expected_size} bytes; {len(candidate_rows)} instructions; "
        "280/163/580 ABI partition"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
