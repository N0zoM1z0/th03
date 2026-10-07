#!/usr/bin/env python3
"""Review the complete TH03 character Extra Attack frontier.

This is target-boundary evidence only. The immutable MAIN target is the byte
oracle. Frozen ReC98 labels and current MAP publics provide names, while raw
instruction coverage, RET/RETF endings and MZ relocations define boundaries.

The reviewed frontier is deliberately split around the already-maintained
generic exatt_add owner at 18FE:119E..11C6:
- P_EXATT_TEXT residual: five character owners, 000A..119D
- MAIN_06_TEXT residual: shared helper owner + four character owners, 11C7..227F
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
SEGMENT = 0x18FE

# owner id, character, map segment, start, end, functions
OWNERS = (
    (
        "th03-main-exatt-chiyuri", "chiyuri", "P_EXATT_TEXT", 0x000A, 0x040F,
        (
            ("exatt_add_chiyuri", 0x000A, 0x007A, "retf", "6"),
            ("chiyuri_1905A", 0x007A, 0x0280, "ret", ""),
            ("exatt_update_chiyuri", 0x0280, 0x03AA, "retf", ""),
            ("exatt_render_chiyuri", 0x03AA, 0x03DC, "retf", ""),
            ("sub_193BC", 0x03DC, 0x040F, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-ellen", "ellen", "P_EXATT_TEXT", 0x040F, 0x0845,
        (
            ("exatt_add_ellen", 0x040F, 0x04C9, "retf", "6"),
            ("ellen_194A9", 0x04C9, 0x0530, "retf", "8"),
            ("ellen_19510", 0x0530, 0x063D, "ret", ""),
            ("exatt_update_ellen", 0x063D, 0x0813, "retf", ""),
            ("exatt_render_ellen", 0x0813, 0x0845, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-kana", "kana", "P_EXATT_TEXT", 0x0845, 0x0ADC,
        (
            ("exatt_add_kana", 0x0845, 0x08B6, "retf", "6"),
            ("kana_19896", 0x08B6, 0x08FD, "retf", "6"),
            ("kana_198DD", 0x08FD, 0x09B9, "ret", ""),
            ("exatt_update_kana", 0x09B9, 0x0AAD, "retf", ""),
            ("exatt_render_kana", 0x0AAD, 0x0ADC, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-marisa", "marisa", "P_EXATT_TEXT", 0x0ADC, 0x0D80,
        (
            ("exatt_add_marisa", 0x0ADC, 0x0B26, "retf", "6"),
            ("marisa_19B06", 0x0B26, 0x0B6F, "retf", "6"),
            ("marisa_19B4F", 0x0B6F, 0x0C56, "ret", ""),
            ("exatt_update_marisa", 0x0C56, 0x0D51, "retf", ""),
            ("exatt_render_marisa", 0x0D51, 0x0D80, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-kotohime", "kotohime", "P_EXATT_TEXT", 0x0D80, 0x119E,
        (
            ("exatt_add_kotohime", 0x0D80, 0x0DF3, "retf", "6"),
            ("kotohime_19DD3", 0x0DF3, 0x0E4A, "retf", "4"),
            ("kotohime_19E2A", 0x0E4A, 0x0F19, "ret", ""),
            ("kotohime_19EF9", 0x0F19, 0x0F3F, "ret", ""),
            ("kotohime_19F1F", 0x0F3F, 0x0FA7, "ret", ""),
            ("kotohime_19F87", 0x0FA7, 0x100F, "ret", ""),
            ("exatt_update_kotohime", 0x100F, 0x116E, "retf", ""),
            ("exatt_render_kotohime", 0x116E, 0x119E, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-shared-main06", "shared", "MAIN_06_TEXT", 0x11C7, 0x129E,
        (
            ("sub_1A1A7", 0x11C7, 0x120D, "ret", ""),
            ("sub_1A1ED", 0x120D, 0x129E, "ret", "0xc"),
        ),
    ),
    (
        "th03-main-exatt-reimu", "reimu", "MAIN_06_TEXT", 0x129E, 0x164B,
        (
            ("exatt_add_reimu", 0x129E, 0x12EE, "retf", "6"),
            ("reimu_1A2CE", 0x12EE, 0x134A, "retf", "6"),
            ("sub_1A32A", 0x134A, 0x1397, "ret", "6"),
            ("sub_1A377", 0x1397, 0x13E4, "ret", "6"),
            ("reimu_1A3C4", 0x13E4, 0x14B1, "ret", ""),
            ("sub_1A491", 0x14B1, 0x1500, "ret", "4"),
            ("exatt_update_reimu", 0x1500, 0x1619, "retf", ""),
            ("exatt_render_reimu", 0x1619, 0x164B, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-mima", "mima", "MAIN_06_TEXT", 0x164B, 0x1922,
        (
            ("exatt_add_mima", 0x164B, 0x16A4, "retf", "6"),
            ("mima_1A684", 0x16A4, 0x1765, "ret", ""),
            ("exatt_update_mima", 0x1765, 0x18F3, "retf", ""),
            ("exatt_render_mima", 0x18F3, 0x1922, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-yumemi", "yumemi", "MAIN_06_TEXT", 0x1922, 0x1FC2,
        (
            ("exatt_add_yumemi", 0x1922, 0x197F, "retf", "6"),
            ("yumemi_1A95F", 0x197F, 0x19D0, "retf", "4"),
            ("yumemi_1A9B0", 0x19D0, 0x1E4E, "ret", ""),
            ("exatt_update_yumemi", 0x1E4E, 0x1F92, "retf", ""),
            ("exatt_render_yumemi", 0x1F92, 0x1FC2, "retf", ""),
        ),
    ),
    (
        "th03-main-exatt-rikako", "rikako", "MAIN_06_TEXT", 0x1FC2, 0x2280,
        (
            ("exatt_add_rikako", 0x1FC2, 0x2026, "retf", "6"),
            ("rikako_1B006", 0x2026, 0x207A, "retf", "6"),
            ("rikako_1B05A", 0x207A, 0x2125, "ret", ""),
            ("exatt_update_rikako", 0x2125, 0x2251, "retf", ""),
            ("exatt_render_rikako", 0x2251, 0x2280, "retf", ""),
        ),
    ),
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def review() -> dict:
    artifact = find_artifact(
        load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
    )
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    if not image.valid:
        raise ValueError("target is not a valid MZ image")

    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    segment_base = SEGMENT * 16
    owners = []

    for owner_id, character, map_segment, owner_start, owner_end, functions in OWNERS:
        cursor = owner_start
        function_rows = []
        for name, start, end, expected_return, expected_operand in functions:
            if start != cursor:
                raise ValueError(
                    f"function partition gap in {owner_id}: {cursor:04X} -> {start:04X}"
                )
            if not owner_start <= start < end <= owner_end:
                raise ValueError(f"function escapes owner: {name}")

            code = image.program_image[segment_base + start:segment_base + end]
            instructions = list(decoder.disasm(code, start))
            covered = sum(ins.size for ins in instructions)
            if not instructions or covered != len(code):
                raise ValueError(f"incomplete linear decode: {name}")
            last = instructions[-1]
            if last.address + last.size != end:
                raise ValueError(f"function does not end on instruction boundary: {name}")
            if last.mnemonic != expected_return or last.op_str.lower() != expected_operand.lower():
                raise ValueError(
                    f"return contract drifted for {name}: "
                    f"{last.mnemonic} {last.op_str!r} != "
                    f"{expected_return} {expected_operand!r}"
                )

            start_linear = segment_base + start
            relocs = [
                relocation.linear - start_linear
                for relocation in image.relocations
                if start_linear <= relocation.linear < segment_base + end
            ]
            function_rows.append({
                "name": name,
                "segment_offset": start,
                "payload_offset": start_linear,
                "file_offset": image.header.header_size + start_linear,
                "size": end - start,
                "instruction_count": len(instructions),
                "return_offset": last.address,
                "return_mnemonic": last.mnemonic,
                "return_operand": last.op_str,
                "relocation_order": relocs,
                "relocation_count": len(relocs),
                "sha256": sha(code),
            })
            cursor = end

        if cursor != owner_end:
            raise ValueError(
                f"owner partition does not reach end {owner_id}: "
                f"{cursor:04X} != {owner_end:04X}"
            )

        owner_linear = segment_base + owner_start
        owner_end_linear = segment_base + owner_end
        crossing = [
            relocation.linear
            for relocation in image.relocations
            if relocation.linear < owner_end_linear
            and relocation.linear + 2 > owner_linear
            and not owner_linear <= relocation.linear <= owner_end_linear - 2
        ]
        if crossing:
            raise ValueError(f"relocation crosses owner edge {owner_id}: {crossing}")

        owner_relocs = [
            relocation.linear - owner_linear
            for relocation in image.relocations
            if owner_linear <= relocation.linear <= owner_end_linear - 2
        ]
        blob = image.program_image[owner_linear:owner_end_linear]
        function_bytes = sum(row["size"] for row in function_rows)
        if function_bytes != len(blob):
            raise ValueError(f"owner byte accounting drifted: {owner_id}")

        owners.append({
            "id": owner_id,
            "character": character,
            "map_segment": map_segment,
            "segment": SEGMENT,
            "owner_start": owner_start,
            "owner_end": owner_end,
            "owner_size": len(blob),
            "payload_start": owner_linear,
            "file_offset": image.header.header_size + owner_linear,
            "function_count": len(function_rows),
            "function_bytes": function_bytes,
            "producer_owned_bytes": 0,
            "functions": function_rows,
            "relocation_order": owner_relocs,
            "relocation_count": len(owner_relocs),
            "sha256": sha(blob),
            "complete_partition": True,
        })

    p_exatt = image.program_image[
        segment_base + 0x000A:segment_base + 0x119E
    ]
    main06 = image.program_image[
        segment_base + 0x11C7:segment_base + 0x2280
    ]
    combined = p_exatt + main06
    return {
        "kind": "th03-main-exatt-family-target-boundary-review",
        "artifact": "th03-main",
        "target_sha256": sha(target),
        "segment": SEGMENT,
        "p_exatt_start": 0x000A,
        "p_exatt_end": 0x119E,
        "p_exatt_bytes": len(p_exatt),
        "generic_exatt_gap_start": 0x119E,
        "generic_exatt_gap_end": 0x11C7,
        "main06_start": 0x11C7,
        "main06_end": 0x2280,
        "main06_bytes": len(main06),
        "owner_count": len(owners),
        "function_count": sum(owner["function_count"] for owner in owners),
        "owned_bytes": len(combined),
        "function_bytes": sum(owner["function_bytes"] for owner in owners),
        "producer_owned_bytes": 0,
        "relocation_count": sum(owner["relocation_count"] for owner in owners),
        "sha256": sha(combined),
        "owners": owners,
        "observed_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pass": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = review()
        text = json.dumps(result, indent=2) + "\n"
        if args.output:
            output = args.output if args.output.is_absolute() else ROOT / args.output
            output = output.resolve()
            if not output.is_relative_to(ROOT / ".analysis"):
                raise ValueError("target review exports belong under .analysis/")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text)
        print(
            "th03-main-exatt-review: PASS; "
            f"{result['owner_count']} owners / {result['function_count']} functions / "
            f"{result['owned_bytes']} owned bytes / "
            f"{result['relocation_count']} relocations"
        )
        if args.output:
            print(f"output: {args.output}")
        return 0
    except (OSError, KeyError, ValueError) as error:
        print(f"th03-main-exatt-review: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
