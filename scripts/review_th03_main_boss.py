#!/usr/bin/env python3
"""Review the complete TH03 MAIN_03_TEXT boss-attack owner family.

This is target-boundary evidence only.  The immutable MAIN target is the byte
oracle.  Frozen ReC98 labels are used solely as stable names for already
observed PROC starts.  Nine Turbo C++ switch tables are classified explicitly
as producer-owned non-function CODE rather than mis-decoded as functions.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import struct
import sys

import capstone

from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
SEGMENT = 0x0F1F
SEGMENT_START = 0x000A
SEGMENT_END = 0x47EA
MAP_SEGMENT = "MAIN_03_TEXT"

# (name, start, end, return mnemonic, return operand)
# The ends are raw target instruction boundaries.  For the nine update
# functions they stop at the real RETF before compiler-emitted switch data.
OWNERS = (
    {
        "id": "th03-main-boss-shared",
        "character": "shared",
        "start": 0x000A,
        "end": 0x03BF,
        "functions": (
            ("sub_F1FA", 0x000A, 0x0166, "ret", "6"),
            ("sub_F356", 0x0166, 0x01B9, "ret", ""),
            ("sub_F3A9", 0x01B9, 0x0212, "ret", ""),
            ("sub_F402", 0x0212, 0x02C4, "ret", ""),
            ("sub_F4B4", 0x02C4, 0x0322, "retf", ""),
            ("sub_F512", 0x0322, 0x033D, "ret", ""),
            ("sub_F52D", 0x033D, 0x039C, "ret", ""),
            ("sub_F58C", 0x039C, 0x03BF, "ret", ""),
        ),
        "table": None,
    },
    {
        "id": "th03-main-boss-marisa",
        "character": "marisa",
        "start": 0x03BF,
        "end": 0x0956,
        "functions": (
            ("marisa_F5AF", 0x03BF, 0x040E, "retf", "2"),
            ("marisa_F5FE", 0x040E, 0x0495, "ret", ""),
            ("marisa_F685", 0x0495, 0x053D, "ret", ""),
            ("marisa_F72D", 0x053D, 0x05CD, "ret", ""),
            ("marisa_F7BD", 0x05CD, 0x0658, "ret", ""),
            ("gba_boss_update_marisa", 0x0658, 0x0765, "retf", ""),
            ("marisa_F9A6", 0x07B6, 0x0881, "ret", ""),
            ("marisa_FA71", 0x0881, 0x08F8, "ret", "2"),
            ("gba_boss_render_marisa", 0x08F8, 0x0956, "retf", ""),
        ),
        "table": (0x0765, 0x07B6, 1, 20, "gba_boss_update_marisa"),
    },
    {
        "id": "th03-main-boss-mima",
        "character": "mima",
        "start": 0x0956,
        "end": 0x10D8,
        "functions": (
            ("mima_FB46", 0x0956, 0x09A5, "retf", "2"),
            ("mima_FB95", 0x09A5, 0x0A7B, "ret", ""),
            ("mima_FC6B", 0x0A7B, 0x0B81, "ret", ""),
            ("mima_FD71", 0x0B81, 0x0C3B, "ret", ""),
            ("mima_FE2B", 0x0C3B, 0x0CE8, "ret", ""),
            ("gba_boss_update_mima", 0x0CE8, 0x0E12, "retf", ""),
            ("mima_10053", 0x0E63, 0x0F94, "ret", ""),
            ("mima_10184", 0x0F94, 0x1073, "ret", "4"),
            ("gba_boss_render_mima", 0x1073, 0x10D8, "retf", ""),
        ),
        "table": (0x0E12, 0x0E63, 1, 20, "gba_boss_update_mima"),
    },
    {
        "id": "th03-main-boss-yumemi",
        "character": "yumemi",
        "start": 0x10D8,
        "end": 0x1A0E,
        "functions": (
            ("yumemi_102C8", 0x10D8, 0x1134, "retf", "2"),
            ("yumemi_10324", 0x1134, 0x1215, "ret", ""),
            ("yumemi_10405", 0x1215, 0x131F, "ret", ""),
            ("yumemi_1050F", 0x131F, 0x13C5, "ret", ""),
            ("yumemi_105B5", 0x13C5, 0x1479, "ret", ""),
            ("yumemi_10669", 0x1479, 0x151A, "ret", ""),
            ("gba_boss_update_yumemi", 0x151A, 0x168A, "retf", ""),
            ("yumemi_108CA", 0x16DA, 0x1827, "ret", ""),
            ("yumemi_10A17", 0x1827, 0x19BB, "ret", ""),
            ("gba_boss_render_yumemi", 0x19BB, 0x1A0E, "retf", ""),
        ),
        "table": (0x168A, 0x16DA, 0, 20, "gba_boss_update_yumemi"),
    },
    {
        "id": "th03-main-boss-reimu",
        "character": "reimu",
        "start": 0x1A0E,
        "end": 0x21F2,
        "functions": (
            ("reimu_10BFE", 0x1A0E, 0x1A5D, "retf", "2"),
            ("reimu_10C4D", 0x1A5D, 0x1BB0, "ret", ""),
            ("reimu_10DA0", 0x1BB0, 0x1C26, "ret", ""),
            ("reimu_10E16", 0x1C26, 0x1DE1, "ret", ""),
            ("reimu_10FD1", 0x1DE1, 0x1E43, "ret", ""),
            ("gba_boss_update_reimu", 0x1E43, 0x1F6B, "retf", ""),
            ("reimu_111A3", 0x1FB3, 0x20B6, "ret", ""),
            ("reimu_112A6", 0x20B6, 0x21B9, "ret", "4"),
            ("gba_boss_render_reimu", 0x21B9, 0x21F2, "retf", ""),
        ),
        "table": (0x1F6B, 0x1FB3, 0, 18, "gba_boss_update_reimu"),
    },
    {
        "id": "th03-main-boss-ellen",
        "character": "ellen",
        "start": 0x21F2,
        "end": 0x287D,
        "functions": (
            ("ellen_113E2", 0x21F2, 0x2249, "retf", "2"),
            ("ellen_11439", 0x2249, 0x2357, "ret", ""),
            ("ellen_11547", 0x2357, 0x2430, "ret", ""),
            ("ellen_11620", 0x2430, 0x24C6, "ret", ""),
            ("gba_boss_update_ellen", 0x24C6, 0x25D3, "retf", ""),
            ("ellen_11814", 0x2624, 0x2695, "ret", "2"),
            ("ellen_11885", 0x2695, 0x271A, "ret", ""),
            ("ellen_1190A", 0x271A, 0x2811, "ret", "6"),
            ("gba_boss_render_ellen", 0x2811, 0x287D, "retf", ""),
        ),
        "table": (0x25D3, 0x2624, 1, 20, "gba_boss_update_ellen"),
    },
    {
        "id": "th03-main-boss-kotohime",
        "character": "kotohime",
        "start": 0x287D,
        "end": 0x2FAD,
        "functions": (
            ("kotohime_11A6D", 0x287D, 0x28D1, "retf", "2"),
            ("kotohime_11AC1", 0x28D1, 0x2961, "ret", "2"),
            ("kotohime_11B51", 0x2961, 0x29D6, "ret", ""),
            ("kotohime_11BC6", 0x29D6, 0x2A6F, "ret", ""),
            ("kotohime_11C5F", 0x2A6F, 0x2B2A, "ret", ""),
            ("kotohime_11D1A", 0x2B2A, 0x2C58, "ret", ""),
            ("gba_boss_update_kotohime", 0x2C58, 0x2DA4, "retf", ""),
            ("kotohime_11FE4", 0x2DF4, 0x2EB0, "ret", "2"),
            ("kotohime_120A0", 0x2EB0, 0x2F13, "ret", ""),
            ("kotohime_12103", 0x2F13, 0x2F50, "ret", "2"),
            ("gba_boss_render_kotohime", 0x2F50, 0x2FAD, "retf", ""),
        ),
        "table": (0x2DA4, 0x2DF4, 0, 20, "gba_boss_update_kotohime"),
    },
    {
        "id": "th03-main-boss-chiyuri",
        "character": "chiyuri",
        "start": 0x2FAD,
        "end": 0x3A0B,
        "functions": (
            ("chiyuri_1219D", 0x2FAD, 0x3005, "retf", "2"),
            ("chiyuri_121F5", 0x3005, 0x3165, "ret", ""),
            ("chiyuri_12355", 0x3165, 0x3235, "ret", ""),
            ("chiyuri_12425", 0x3235, 0x32A8, "ret", ""),
            ("chiyuri_12498", 0x32A8, 0x34B8, "ret", ""),
            ("gba_boss_update_chiyuri", 0x34B8, 0x371D, "retf", ""),
            ("chiyuri_1295E", 0x376E, 0x3820, "ret", ""),
            ("chiyuri_12A10", 0x3820, 0x38ED, "ret", ""),
            ("chiyuri_12ADD", 0x38ED, 0x3948, "ret", ""),
            ("chiyuri_12B38", 0x3948, 0x39A9, "ret", "2"),
            ("gba_boss_render_chiyuri", 0x39A9, 0x3A0B, "retf", ""),
        ),
        "table": (0x371D, 0x376E, 1, 20, "gba_boss_update_chiyuri"),
    },
    {
        "id": "th03-main-boss-kana",
        "character": "kana",
        "start": 0x3A0B,
        "end": 0x415D,
        "functions": (
            ("kana_12BFB", 0x3A0B, 0x3A5F, "retf", "2"),
            ("kana_12C4F", 0x3A5F, 0x3B47, "ret", ""),
            ("kana_12D37", 0x3B47, 0x3C88, "ret", ""),
            ("kana_12E78", 0x3C88, 0x3D16, "ret", ""),
            ("kana_12F06", 0x3D16, 0x3DF8, "ret", ""),
            ("gba_boss_update_kana", 0x3DF8, 0x3F34, "retf", ""),
            ("kana_13174", 0x3F84, 0x4033, "ret", ""),
            ("kana_13223", 0x4033, 0x410E, "ret", ""),
            ("gba_boss_render_kana", 0x410E, 0x415D, "retf", ""),
        ),
        "table": (0x3F34, 0x3F84, 0, 20, "gba_boss_update_kana"),
    },
    {
        "id": "th03-main-boss-rikako",
        "character": "rikako",
        "start": 0x415D,
        "end": 0x47EA,
        "functions": (
            ("rikako_1334D", 0x415D, 0x41B5, "retf", "2"),
            ("rikako_133A5", 0x41B5, 0x42BA, "ret", ""),
            ("rikako_134AA", 0x42BA, 0x43B4, "ret", ""),
            ("rikako_135A4", 0x43B4, 0x4471, "ret", ""),
            ("gba_boss_update_rikako", 0x4471, 0x458E, "retf", ""),
            ("rikako_137CF", 0x45DF, 0x46C3, "ret", ""),
            ("rikako_138B3", 0x46C3, 0x479B, "ret", ""),
            ("gba_boss_render_rikako", 0x479B, 0x47EA, "retf", ""),
        ),
        "table": (0x458E, 0x45DF, 1, 20, "gba_boss_update_rikako"),
    },
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def expected_keys(count: int) -> tuple[int, ...]:
    if count == 20:
        return tuple(range(0x12)) + (0x80, 0xFF)
    if count == 18:
        return tuple(range(2, 0x12)) + (0x80, 0xFF)
    raise ValueError(f"unsupported switch key count: {count}")


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
    global_cursor = SEGMENT_START

    for owner in OWNERS:
        if owner["start"] != global_cursor:
            raise ValueError(f"owner partition gap before {owner['id']}")
        if owner["end"] <= owner["start"]:
            raise ValueError(f"invalid owner span: {owner['id']}")

        function_rows = []
        occupied = []
        update_instruction_starts: dict[str, set[int]] = {}
        for name, start, end, expected_return, expected_operand in owner["functions"]:
            if not (owner["start"] <= start < end <= owner["end"]):
                raise ValueError(f"function escapes owner: {name}")
            code = image.program_image[segment_base + start:segment_base + end]
            instructions = list(decoder.disasm(code, start))
            if not instructions or sum(ins.size for ins in instructions) != len(code):
                raise ValueError(f"incomplete linear decode: {name}")
            last = instructions[-1]
            if last.address + last.size != end:
                raise ValueError(f"function does not end on instruction boundary: {name}")
            if last.mnemonic != expected_return or last.op_str != expected_operand:
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
            occupied.append((start, end, f"function:{name}"))
            if name.startswith("gba_boss_update_"):
                update_instruction_starts[name] = {ins.address for ins in instructions}

        table_row = None
        if owner["table"] is not None:
            start, end, pad, count, update_name = owner["table"]
            if not (owner["start"] <= start < end <= owner["end"]):
                raise ValueError(f"switch table escapes owner: {owner['id']}")
            raw = image.program_image[segment_base + start:segment_base + end]
            expected_size = pad + (count * 4)
            if len(raw) != expected_size:
                raise ValueError(
                    f"switch table size drifted for {owner['id']}: "
                    f"{len(raw)} != {expected_size}"
                )
            if pad and raw[0] != 0:
                raise ValueError(f"switch alignment byte drifted: {owner['id']}")
            body = raw[pad:]
            keys = struct.unpack_from("<" + ("H" * count), body, 0)
            if keys != expected_keys(count):
                raise ValueError(f"switch keys drifted: {owner['id']}: {keys}")
            destinations = struct.unpack_from("<" + ("H" * count), body, count * 2)
            function = next(row for row in function_rows if row["name"] == update_name)
            function_end = function["segment_offset"] + function["size"]
            instruction_starts = update_instruction_starts[update_name]
            for destination in destinations:
                if not function["segment_offset"] <= destination < function_end:
                    raise ValueError(
                        f"switch destination leaves update body: "
                        f"{owner['id']} -> {destination:04x}"
                    )
                if destination not in instruction_starts:
                    raise ValueError(
                        f"switch destination is not an instruction start: "
                        f"{owner['id']} -> {destination:04x}"
                    )
            table_linear = segment_base + start
            table_relocs = [
                relocation.linear - table_linear
                for relocation in image.relocations
                if table_linear <= relocation.linear < segment_base + end
            ]
            table_row = {
                "kind": "tc4-switch-table",
                "segment_offset": start,
                "payload_offset": table_linear,
                "file_offset": image.header.header_size + table_linear,
                "size": len(raw),
                "alignment_bytes": pad,
                "key_count": count,
                "keys": list(keys),
                "destinations": list(destinations),
                "update_function": update_name,
                "relocation_order": table_relocs,
                "relocation_count": len(table_relocs),
                "sha256": sha(raw),
            }
            occupied.append((start, end, "producer-data:switch-table"))

        occupied.sort()
        cursor = owner["start"]
        for start, end, label in occupied:
            if start != cursor:
                raise ValueError(
                    f"owner partition gap/overlap {owner['id']} before {label}: "
                    f"{cursor:04x} -> {start:04x}"
                )
            cursor = end
        if cursor != owner["end"]:
            raise ValueError(
                f"owner partition does not reach end {owner['id']}: "
                f"{cursor:04x} != {owner['end']:04x}"
            )

        owner_linear = segment_base + owner["start"]
        owner_end_linear = segment_base + owner["end"]
        crossing = [
            relocation.linear
            for relocation in image.relocations
            if relocation.linear < owner_end_linear
            and relocation.linear + 2 > owner_linear
            and not owner_linear <= relocation.linear <= owner_end_linear - 2
        ]
        if crossing:
            raise ValueError(f"relocation crosses owner edge {owner['id']}: {crossing}")
        owner_relocs = [
            relocation.linear - owner_linear
            for relocation in image.relocations
            if owner_linear <= relocation.linear <= owner_end_linear - 2
        ]
        blob = image.program_image[owner_linear:owner_end_linear]
        function_bytes = sum(row["size"] for row in function_rows)
        producer_bytes = table_row["size"] if table_row else 0
        if function_bytes + producer_bytes != len(blob):
            raise ValueError(f"owner byte accounting drifted: {owner['id']}")

        owners.append({
            "id": owner["id"],
            "character": owner["character"],
            "map_segment": MAP_SEGMENT,
            "segment": SEGMENT,
            "owner_start": owner["start"],
            "owner_end": owner["end"],
            "owner_size": len(blob),
            "payload_start": owner_linear,
            "file_offset": image.header.header_size + owner_linear,
            "function_count": len(function_rows),
            "function_bytes": function_bytes,
            "producer_owned_bytes": producer_bytes,
            "functions": function_rows,
            "producer_owned_ranges": ([] if table_row is None else [table_row]),
            "relocation_order": owner_relocs,
            "relocation_count": len(owner_relocs),
            "sha256": sha(blob),
            "complete_partition": True,
        })
        global_cursor = owner["end"]

    if global_cursor != SEGMENT_END:
        raise ValueError(f"MAIN_03_TEXT owner partition ends at {global_cursor:04x}")

    segment_linear = segment_base + SEGMENT_START
    segment_end_linear = segment_base + SEGMENT_END
    segment_blob = image.program_image[segment_linear:segment_end_linear]
    return {
        "kind": "th03-main-boss-target-boundary-review",
        "artifact": "th03-main",
        "target_sha256": sha(target),
        "map_segment": MAP_SEGMENT,
        "segment": SEGMENT,
        "segment_start": SEGMENT_START,
        "segment_end": SEGMENT_END,
        "owner_count": len(owners),
        "function_count": sum(owner["function_count"] for owner in owners),
        "owned_bytes": len(segment_blob),
        "function_bytes": sum(owner["function_bytes"] for owner in owners),
        "producer_owned_bytes": sum(owner["producer_owned_bytes"] for owner in owners),
        "relocation_count": sum(owner["relocation_count"] for owner in owners),
        "sha256": sha(segment_blob),
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
            "th03-main-boss-review: PASS; "
            f"{result['owner_count']} owners / {result['function_count']} functions / "
            f"{result['function_bytes']} function bytes + "
            f"{result['producer_owned_bytes']} producer bytes = "
            f"{result['owned_bytes']} owned bytes / "
            f"{result['relocation_count']} relocations"
        )
        if args.output:
            print(f"output: {args.output}")
        return 0
    except (OSError, KeyError, ValueError) as error:
        print(f"th03-main-boss-review: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
