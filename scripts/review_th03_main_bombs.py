#!/usr/bin/env python3
"""Independently review TH03 MAIN_05_TEXT bomb-owner boundaries in the target."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
SEGMENT = 0x183C
OWNER_START = 0x0001
OWNER_SIZE = 0x0C29
FUNCTIONS = (
    ("chiyuri_bomb", 0x0001, 0x01EA, "retf"),
    ("ellen_bomb_update", 0x01EB, 0x0118, "retf"),
    ("ellen_bomb_render", 0x0303, 0x00A3, "ret"),
    ("ellen_bomb", 0x03A6, 0x0244, "retf"),
    ("kana_bomb", 0x05EA, 0x020E, "retf"),
    ("kotohime_bomb", 0x07F8, 0x0210, "retf"),
    ("rikako_bomb", 0x0A08, 0x0222, "retf"),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relocation_order(image) -> list[int]:
    start = SEGMENT * 16 + OWNER_START
    end = start + OWNER_SIZE
    return [
        relocation.linear - start
        for relocation in image.relocations
        if start <= relocation.linear < end
    ]


def review(candidate: Path | None = None) -> dict:
    artifact = find_artifact(
        load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
    )
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    if not image.valid:
        raise ValueError("target is not a valid MZ image")

    payload_start = SEGMENT * 16 + OWNER_START
    payload_end = payload_start + OWNER_SIZE
    if payload_end > len(image.program_image):
        raise ValueError("owner exceeds target program image")

    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    rows = []
    cursor = OWNER_START
    for name, offset, size, expected_return in FUNCTIONS:
        if offset != cursor:
            raise ValueError(f"non-contiguous function partition before {name}")
        start = SEGMENT * 16 + offset
        code = image.program_image[start:start + size]
        instructions = list(decoder.disasm(code, offset))
        if not instructions or sum(ins.size for ins in instructions) != size:
            raise ValueError(f"incomplete linear decode: {name}")
        last = instructions[-1]
        if last.address + last.size != offset + size:
            raise ValueError(f"function does not end on an instruction boundary: {name}")
        if last.mnemonic != expected_return:
            raise ValueError(
                f"unexpected return for {name}: {last.mnemonic}, expected {expected_return}"
            )
        rows.append({
            "name": name,
            "segment_offset": offset,
            "payload_offset": start,
            "size": size,
            "instruction_count": len(instructions),
            "first_instruction": instructions[0].mnemonic,
            "last_instruction": last.mnemonic,
            "last_instruction_offset": last.address,
            "sha256": sha(code),
        })
        cursor += size
    if cursor != OWNER_START + OWNER_SIZE:
        raise ValueError("function partition does not cover the owner exactly")

    crossing = []
    relocations = []
    for relocation in image.relocations:
        if relocation.linear < payload_end and relocation.linear + 2 > payload_start:
            if not payload_start <= relocation.linear <= payload_end - 2:
                crossing.append(relocation.linear)
            else:
                relocations.append(relocation.linear - payload_start)
    if crossing:
        raise ValueError(f"relocation crosses owner edge: {crossing}")

    result = {
        "kind": "th03-main-bombs-target-boundary-review",
        "artifact": "th03-main",
        "target_sha256": sha(target),
        "segment": SEGMENT,
        "owner_start": OWNER_START,
        "owner_size": OWNER_SIZE,
        "payload_start": payload_start,
        "file_offset": image.header.header_size + payload_start,
        "function_bytes": sum(row["size"] for row in rows),
        "functions": rows,
        "relocation_sites": relocations,
        "relocation_order": relocation_order(image),
        "relocation_count": len(relocations),
        "complete_partition": True,
        "observed_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pass": True,
    }
    if candidate is not None:
        candidate_data = candidate.read_bytes()
        candidate_image = parse_mz(candidate_data)
        if not candidate_image.valid:
            raise ValueError("candidate is not a valid MZ image")
        if payload_end > len(candidate_image.program_image):
            raise ValueError("owner exceeds candidate program image")

        candidate_payload = candidate_image.program_image[payload_start:payload_end]
        target_payload = image.program_image[payload_start:payload_end]
        candidate_relocations = [
            relocation.linear - payload_start
            for relocation in candidate_image.relocations
            if payload_start <= relocation.linear <= payload_end - 2
        ]
        candidate_order = relocation_order(candidate_image)
        candidate_functions = []
        owner_mismatches = [
            {
                "offset": index,
                "target": target_byte,
                "candidate": candidate_byte,
            }
            for index, (target_byte, candidate_byte) in enumerate(
                zip(target_payload, candidate_payload)
            )
            if target_byte != candidate_byte
        ]
        for row in rows:
            start = SEGMENT * 16 + int(row["segment_offset"])
            size = int(row["size"])
            target_code = image.program_image[start:start + size]
            code = candidate_image.program_image[start:start + size]
            mismatch_offsets = [
                index
                for index, (target_byte, candidate_byte) in enumerate(
                    zip(target_code, code)
                )
                if target_byte != candidate_byte
            ]
            candidate_functions.append({
                "name": row["name"],
                "sha256": sha(code),
                "bytes_equal": sha(code) == row["sha256"],
                "byte_mismatch_count": len(mismatch_offsets),
                "byte_mismatch_offsets": mismatch_offsets,
            })
        target_relocation_counts = Counter(result["relocation_sites"])
        candidate_relocation_counts = Counter(candidate_relocations)
        missing_relocations = list((target_relocation_counts - candidate_relocation_counts).elements())
        extra_relocations = list((candidate_relocation_counts - target_relocation_counts).elements())
        result["candidate"] = {
            "path": candidate.as_posix(),
            "sha256": sha(candidate_data),
            "owner_sha256": sha(candidate_payload),
            "owner_bytes_equal": candidate_payload == target_payload,
            "owner_byte_mismatch_count": len(owner_mismatches),
            "owner_byte_mismatches": owner_mismatches,
            "relocation_sites": candidate_relocations,
            "relocation_sites_equal": candidate_relocation_counts == target_relocation_counts,
            "missing_relocation_sites": sorted(missing_relocations),
            "extra_relocation_sites": sorted(extra_relocations),
            "relocation_order": candidate_order,
            "relocation_order_equal": candidate_order == result["relocation_order"],
            "functions": candidate_functions,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    try:
        candidate = None
        if args.candidate:
            candidate = args.candidate
            if not candidate.is_absolute():
                candidate = ROOT / candidate
        result = review(candidate)
        text = json.dumps(result, indent=2) + "\n"
        if args.output:
            output = args.output if args.output.is_absolute() else ROOT / args.output
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text)
        print(
            f"th03-main-bombs-review: PASS; {len(result['functions'])} functions / "
            f"{result['function_bytes']} bytes, {result['relocation_count']} relocations"
        )
        if args.output:
            print(f"output: {args.output}")
        return 0
    except (OSError, KeyError, ValueError) as error:
        print(f"th03-main-bombs-review: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
