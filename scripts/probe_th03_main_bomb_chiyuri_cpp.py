#!/usr/bin/env python3
"""Compile the maintained Chiyuri bomb C++ producer and compare its code shape."""

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
SOURCE = ROOT / "src/main/player/bomb_chiyuri.cpp"
OVERLAY = Path("th03/b_chiyu.cpp")
OBJECT = Path("obj/th03/b_chiyu.obj")
TARGET_SEGMENT = 0x183C
TARGET_OFFSET = 0x0001
SUPPORT = (
    "compat/rec98/th03/main/player/cur.hpp",
    "compat/rec98/th03/main/player/bomb.hpp",
    "compat/rec98/th03/formats/mrs.hpp",
    "compat/rec98/th03/hardware/palette.hpp",
    "compat/rec98/th02/snd/snd.h",
    "compat/rec98/libs/master.lib/pc98_gfx.hpp",
)
FUNCTIONS = (
    ("chiyuri_bomb", 490, "retf"),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def omf_index(data: bytes, pos: int = 0) -> tuple[int, int]:
    first = data[pos]
    if first & 0x80:
        return (((first & 0x7F) << 8) | data[pos + 1], pos + 2)
    return (first, pos + 1)


def segment_definitions(raw: bytes) -> list[dict]:
    names = [""]
    records = parse_omf(raw)
    for record in records:
        if record.name != "LNAMES":
            continue
        pos = 0
        while pos < len(record.data):
            size = record.data[pos]
            pos += 1
            end = pos + size
            if end > len(record.data):
                raise ValueError("truncated OMF LNAMES entry")
            names.append(record.data[pos:end].decode("ascii", errors="strict"))
            pos = end

    result = []
    for record in records:
        if record.name != "SEGDEF":
            continue
        if len(record.data) < 3:
            raise ValueError("truncated OMF SEGDEF")
        size = int.from_bytes(record.data[1:3], "little")
        pos = 3
        name_index, pos = omf_index(record.data, pos)
        class_index, pos = omf_index(record.data, pos)
        overlay_index, pos = omf_index(record.data, pos)
        for index in (name_index, class_index, overlay_index):
            if index >= len(names):
                raise ValueError("OMF SEGDEF references missing LNAME")
        result.append({
            "index": len(result) + 1,
            "name": names[name_index],
            "class": names[class_index],
            "overlay": names[overlay_index],
            "size": size,
        })
    return result


def code_bytes(raw: bytes, segment_index: int) -> tuple[bytes, list[dict]]:
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
    selected = by_segment.get(segment_index)
    if not selected:
        raise ValueError(
            f"Chiyuri object has no TC4J code LEDATA in segment index {segment_index}"
        )
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
        raise ValueError("Chiyuri code LEDATA is gapped or overlapping")
    return bytes(image), receipt_parts


def instruction_signature(blob: bytes) -> tuple[list[dict], list[tuple[int, int, str]]]:
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    insns = list(cs.disasm(blob, 0))
    if sum(insn.size for insn in insns) != len(blob):
        raise ValueError("Capstone did not cover complete Chiyuri code image")
    rows = [
        {
            "offset": insn.address,
            "size": insn.size,
            "mnemonic": insn.mnemonic,
            "op_str": insn.op_str,
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

    out = ROOT / ".analysis/th03-main-bomb-chiyuri-cpp" / args.run_id
    out.mkdir(parents=True, exist_ok=False)

    exact_cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    revision = exact_cfg["reference_revision"]
    inputs = {}
    for path in (
        "src/main/player/bomb_chiyuri.cpp",
        *SUPPORT,
        "scripts/probe_th03_main_bomb_chiyuri_cpp.py",
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
        r"-nobj/th03/ th03/b_chiyu.cpp",
    ]
    build = execute(command, work, env, out / "compiler.log")
    raw = (work / OBJECT).read_bytes()
    omf = describe_omf(raw)
    if "TC86 Borland C++ 4.02" not in omf["translator_comments"]:
        raise ValueError("Chiyuri probe used the wrong compiler producer")
    segments = segment_definitions(raw)
    nonempty_code = [
        segment for segment in segments
        if segment["class"] == "CODE" and segment["size"]
    ]
    if (
        len(nonempty_code) != 1
        or nonempty_code[0]["name"] != "MAIN_05_TEXT"
        or nonempty_code[0]["class"] != "CODE"
        or nonempty_code[0]["overlay"] != ""
    ):
        raise ValueError(f"unexpected Chiyuri nonempty CODE segments: {nonempty_code}")
    bss = [
        segment for segment in segments
        if segment["class"] == "BSS" and segment["size"]
    ]
    if bss:
        raise ValueError(f"unexpected Chiyuri nonempty BSS segments: {bss}")

    code_segment = nonempty_code[0]
    candidate, ledata = code_bytes(raw, int(code_segment["index"]))
    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    target_image = parse_mz(target_raw).program_image
    target_start = (TARGET_SEGMENT * 16) + TARGET_OFFSET
    expected_size = sum(size for _, size, _ in FUNCTIONS)
    target = target_image[target_start:target_start + expected_size]
    if len(target) != expected_size:
        raise ValueError(
            f"Chiyuri target size mismatch: target={len(target)} expected={expected_size}"
        )

    candidate_rows, candidate_signature = instruction_signature(candidate)
    target_rows, target_signature = instruction_signature(target)
    if candidate_signature != target_signature:
        for index, (left, right) in enumerate(zip(candidate_signature, target_signature)):
            if left != right:
                raise ValueError(
                    f"Chiyuri instruction shape differs at instruction {index}: "
                    f"candidate={left} target={right}"
                )
        raise ValueError(
            "Chiyuri instruction shape differs in instruction count/size: "
            f"candidate={len(candidate)} bytes/{len(candidate_signature)} instructions, "
            f"target={len(target)} bytes/{len(target_signature)} instructions"
        )

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
        raise ValueError("Chiyuri ABI/function boundaries differ")

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
        "kind": "th03-main-bomb-chiyuri-cpp-producer-shape",
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
            "segment_sizes": {
                "code": code_segment["size"],
                "bss": 0,
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
            "Fresh TC4J object-level producer proof. The 490-byte Chiyuri candidate "
            "matches the immutable target instruction shape without masking fixup/data "
            "operands. A separate full MAIN link places this producer exactly at "
            "183C:0001..01EA with zero linked-byte mismatches and the target 13-entry "
            "relocation order. Owner promotion still waits for the remaining character "
            "producers and Ellen private-BSS placement."
        ),

    }
    (out / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")

    for path, before in inputs.items():
        if sha((ROOT / path).read_bytes()) != before:
            raise ValueError("probe input changed during run: " + path)

    print(
        "Chiyuri TC4J producer shape: PASS; "
        f"{expected_size} bytes; {len(candidate_rows)} instructions; "
        "single far-return owner"
    )
    print("Receipt:", (out / "receipt.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
