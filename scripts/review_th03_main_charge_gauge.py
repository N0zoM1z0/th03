#!/usr/bin/env python3
"""Review complete TH03 character charge-shot/gauge CODE owners in MAIN."""

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

# Complete root-carrier CODE contributions from the immutable MAIN target.
# The five owners are character-local modules. Function boundaries come from
# raw contiguous instruction decoding plus real RET/RETF endings; public MAP
# names and the frozen symbolic carrier are corroborating evidence, not the
# boundary oracle.
OWNERS = (
    {
        "id": "th03-main-charge-gauge-chiyuri",
        "character": "chiyuri",
        "segment": 0x1B26,
        "start": 0x0000,
        "size": 0x03F3,
        "map_segment": "MAIN_07_TEXT",
        "functions": (
            ("chiyuri_charge_setup", "sub_1B260", 0x0000, 0x0017, "retf", ""),
            ("chargeshot_add_chiyuri", "chargeshot_add_chiyuri", 0x0017, 0x004B, "retf", "4"),
            ("chargeshot_update_chiyuri", "chargeshot_update_chiyuri", 0x0062, 0x009D, "retf", ""),
            ("chiyuri_chargeshot_private", "chiyuri_chargeshot_1B35F", 0x00FF, 0x0051, "ret", ""),
            ("chargeshot_hittest_chiyuri", "@chargeshot_hittest_chiyuri$qv", 0x0150, 0x0077, "retf", ""),
            ("chargeshot_render_chiyuri", "chargeshot_render_chiyuri", 0x01C7, 0x0065, "retf", ""),
            ("gauge_pattern_chiyuri", "@gauge_pattern_chiyuri$quc", 0x022C, 0x0197, "ret", "2"),
            ("gba_gauge_pattern_pellet_chiyuri", "gba_gauge_pattern_pellet_chiyuri", 0x03C3, 0x0018, "retf", ""),
            ("gba_gauge_pattern_bullet_chiyuri", "gba_gauge_pattern_bullet_chiyuri", 0x03DB, 0x0018, "retf", ""),
        ),
    },
    {
        "id": "th03-main-charge-gauge-ellen",
        "character": "ellen",
        "segment": 0x1B65,
        "start": 0x0003,
        "size": 0x05FA,
        "map_segment": "MAIN_08_TEXT",
        "functions": (
            ("ellen_charge_setup", "sub_1B653", 0x0003, 0x0021, "retf", ""),
            ("chargeshot_add_ellen", "chargeshot_add_ellen", 0x0024, 0x0056, "retf", "4"),
            ("ellen_hyper", "ellen_hyper_1B6CA", 0x007A, 0x0059, "retf", "4"),
            ("chargeshot_update_ellen", "chargeshot_update_ellen", 0x00D3, 0x0183, "retf", ""),
            ("ellen_chargeshot_private", "ellen_chargeshot_1B8A6", 0x0256, 0x005D, "ret", "4"),
            ("chargeshot_hittest_ellen", "@chargeshot_hittest_ellen$qv", 0x02B3, 0x0076, "retf", ""),
            ("chargeshot_render_ellen", "chargeshot_render_ellen", 0x0329, 0x0067, "retf", ""),
            ("gauge_pattern_ellen", "@gauge_pattern_ellen$quc", 0x0390, 0x023D, "ret", "2"),
            ("gba_gauge_pattern_pellet_ellen", "gba_gauge_pattern_pellet_ellen", 0x05CD, 0x0018, "retf", ""),
            ("gba_gauge_pattern_bullet_ellen", "gba_gauge_pattern_bullet_ellen", 0x05E5, 0x0018, "retf", ""),
        ),
    },
    {
        "id": "th03-main-charge-gauge-kana",
        "character": "kana",
        "segment": 0x1BC4,
        "start": 0x000D,
        "size": 0x050B,
        "map_segment": "MAIN_09_TEXT",
        "functions": (
            ("kana_charge_setup", "sub_1BC4D", 0x000D, 0x000F, "retf", ""),
            ("chargeshot_add_kana", "chargeshot_add_kana", 0x001C, 0x0079, "retf", "4"),
            ("chargeshot_update_kana", "chargeshot_update_kana", 0x0095, 0x0123, "retf", ""),
            ("kana_chargeshot_private", "kana_chargeshot_1BDF8", 0x01B8, 0x005A, "ret", ""),
            ("chargeshot_hittest_kana", "@chargeshot_hittest_kana$qv", 0x0212, 0x00A1, "retf", ""),
            ("chargeshot_render_kana", "chargeshot_render_kana", 0x02B3, 0x006F, "retf", ""),
            ("gauge_pattern_kana", "@gauge_pattern_kana$quc", 0x0322, 0x01C6, "ret", "2"),
            ("gba_gauge_pattern_pellet_kana", "gba_gauge_pattern_pellet_kana", 0x04E8, 0x0018, "retf", ""),
            ("gba_gauge_pattern_bullet_kana", "gba_gauge_pattern_bullet_kana", 0x0500, 0x0018, "retf", ""),
        ),
    },
    {
        "id": "th03-main-charge-gauge-kotohime",
        "character": "kotohime",
        "segment": 0x1C15,
        "start": 0x0008,
        "size": 0x02B2,
        "map_segment": "MAIN_10_TEXT",
        "functions": (
            ("kotohime_charge_setup", "sub_1C158", 0x0008, 0x000F, "retf", ""),
            ("chargeshot_add_kotohime", "chargeshot_add_kotohime", 0x0017, 0x0038, "retf", "4"),
            ("chargeshot_update_kotohime", "chargeshot_update_kotohime", 0x004F, 0x004A, "retf", ""),
            ("kotohime_chargeshot_private", "kotohime_chargeshot_1C1E9", 0x0099, 0x0045, "ret", ""),
            ("chargeshot_hittest_kotohime", "@chargeshot_hittest_kotohime$qv", 0x00DE, 0x0067, "retf", ""),
            ("chargeshot_render_kotohime", "chargeshot_render_kotohime", 0x0145, 0x004B, "retf", ""),
            ("gauge_pattern_kotohime", "@gauge_pattern_kotohime$quc", 0x0190, 0x00FA, "ret", "2"),
            ("gba_gauge_pattern_pellet_kotohime", "gba_gauge_pattern_pellet_kotohime", 0x028A, 0x0018, "retf", ""),
            ("gba_gauge_pattern_bullet_kotohime", "gba_gauge_pattern_bullet_kotohime", 0x02A2, 0x0018, "retf", ""),
        ),
    },
    {
        "id": "th03-main-charge-gauge-rikako",
        "character": "rikako",
        "segment": 0x1C40,
        "start": 0x000A,
        "size": 0x0500,
        "map_segment": "MAIN_11_TEXT",
        "functions": (
            ("rikako_charge_setup", "sub_1C40A", 0x000A, 0x000F, "retf", ""),
            ("chargeshot_add_rikako", "chargeshot_add_rikako", 0x0019, 0x007E, "retf", "4"),
            ("rikako_charge_add_private", "rikako_1C497", 0x0097, 0x001D, "retf", "4"),
            ("rikako_hyper", "rikako_hyper_1C4B4", 0x00B4, 0x0011, "retf", ""),
            ("chargeshot_update_rikako", "chargeshot_update_rikako", 0x00C5, 0x0165, "retf", ""),
            ("rikako_chargeshot_private", "rikako_chargeshot_1C62A", 0x022A, 0x0041, "ret", ""),
            ("chargeshot_hittest_rikako", "@chargeshot_hittest_rikako$qv", 0x026B, 0x007D, "retf", ""),
            ("chargeshot_render_rikako", "chargeshot_render_rikako", 0x02E8, 0x0061, "retf", ""),
            ("gauge_pattern_rikako", "@gauge_pattern_rikako$quc", 0x0349, 0x0191, "ret", "2"),
            ("gba_gauge_pattern_pellet_rikako", "gba_gauge_pattern_pellet_rikako", 0x04DA, 0x0018, "retf", ""),
            ("gba_gauge_pattern_bullet_rikako", "gba_gauge_pattern_bullet_rikako", 0x04F2, 0x0018, "retf", ""),
        ),
    },
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def review_owner(image, owner: dict) -> dict:
    segment = owner["segment"]
    owner_start = owner["start"]
    owner_size = owner["size"]
    payload_start = segment * 16 + owner_start
    payload_end = payload_start + owner_size
    if payload_end > len(image.program_image):
        raise ValueError(f"owner exceeds target program image: {owner['id']}")

    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    rows = []
    cursor = owner_start
    for name, source_label, offset, size, expected_return, expected_operand in owner["functions"]:
        if offset != cursor:
            raise ValueError(f"non-contiguous function partition before {name}")
        start = segment * 16 + offset
        code = image.program_image[start:start + size]
        instructions = list(decoder.disasm(code, offset))
        if not instructions or sum(ins.size for ins in instructions) != size:
            raise ValueError(f"incomplete linear decode: {name}")
        last = instructions[-1]
        if last.address + last.size != offset + size:
            raise ValueError(f"function does not end on an instruction boundary: {name}")
        if last.mnemonic != expected_return or last.op_str != expected_operand:
            raise ValueError(
                f"unexpected return for {name}: {last.mnemonic} {last.op_str!r}, "
                f"expected {expected_return} {expected_operand!r}"
            )
        function_relocations = [
            relocation.linear - start
            for relocation in image.relocations
            if start <= relocation.linear < start + size
        ]
        rows.append({
            "name": name,
            "source_label": source_label,
            "segment_offset": offset,
            "payload_offset": start,
            "size": size,
            "instruction_count": len(instructions),
            "first_instruction": instructions[0].mnemonic,
            "last_instruction": last.mnemonic,
            "last_instruction_operand": last.op_str,
            "last_instruction_offset": last.address,
            "relocation_order": function_relocations,
            "relocation_count": len(function_relocations),
            "sha256": sha(code),
        })
        cursor += size
    if cursor != owner_start + owner_size:
        raise ValueError(f"function partition does not cover owner exactly: {owner['id']}")

    crossing = []
    relocations = []
    for relocation in image.relocations:
        if relocation.linear < payload_end and relocation.linear + 2 > payload_start:
            if not payload_start <= relocation.linear <= payload_end - 2:
                crossing.append(relocation.linear)
            else:
                relocations.append(relocation.linear - payload_start)
    if crossing:
        raise ValueError(f"relocation crosses owner edge {owner['id']}: {crossing}")

    blob = image.program_image[payload_start:payload_end]
    return {
        "id": owner["id"],
        "character": owner["character"],
        "map_segment": owner["map_segment"],
        "segment": segment,
        "owner_start": owner_start,
        "owner_size": owner_size,
        "payload_start": payload_start,
        "file_offset": image.header.header_size + payload_start,
        "function_bytes": sum(row["size"] for row in rows),
        "function_count": len(rows),
        "functions": rows,
        "relocation_order": relocations,
        "relocation_count": len(relocations),
        "sha256": sha(blob),
        "complete_partition": True,
    }


def review() -> dict:
    artifact = find_artifact(
        load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
    )
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    if not image.valid:
        raise ValueError("target is not a valid MZ image")

    owners = [review_owner(image, owner) for owner in OWNERS]
    spans = sorted(
        (owner["payload_start"], owner["payload_start"] + owner["owner_size"], owner["id"])
        for owner in owners
    )
    for left, right in zip(spans, spans[1:]):
        if left[1] > right[0]:
            raise ValueError(f"charge/gauge owners overlap: {left[2]} / {right[2]}")

    return {
        "kind": "th03-main-charge-gauge-target-boundary-review",
        "artifact": "th03-main",
        "target_sha256": sha(target),
        "owner_count": len(owners),
        "function_count": sum(owner["function_count"] for owner in owners),
        "owned_bytes": sum(owner["owner_size"] for owner in owners),
        "function_bytes": sum(owner["function_bytes"] for owner in owners),
        "relocation_count": sum(owner["relocation_count"] for owner in owners),
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
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text)
        print(
            "th03-main-charge-gauge-review: PASS; "
            f"{result['owner_count']} owners / {result['function_count']} functions / "
            f"{result['owned_bytes']} bytes / {result['relocation_count']} relocations"
        )
        if args.output:
            print(f"output: {args.output}")
        return 0
    except (OSError, KeyError, ValueError) as error:
        print(f"th03-main-charge-gauge-review: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
