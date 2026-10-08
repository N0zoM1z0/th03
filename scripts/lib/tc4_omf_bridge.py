"""Fail-closed OMF record-framing calibration for TH03 Ellen's natural TC4 OBJ.

TC4 4.02 produces original 1078 CODE bytes and correct ordered fixup
descriptors but places the far SE-call fixup at relative location 1001
inside its 0..1024 LEDATA/FIXUPP record. The historical MZ relocation
order requires a record boundary at 1000, not at 1024.

Reframing *only* those two LEDATA and their adjacent FIXUPP records moves
the unchanged far-call fixup descriptor to the following record and
rebases its 10-bit data-record offset from 1001 to 1, while all three
following FIXUPP descriptor offsets increase by 24 to retain their actual
CODE locations. It never substitutes
game instructions, changes a symbol, edits a target-relative offset in
CODE, omits a fixup, or alters the comparison oracle.

This is a documented, reproducible OMF producer calibration; it is not
a claim that TC4 without this bridge emitted the historical record layout.
"""

from __future__ import annotations

from .omf import parse_omf


def _record(record_type: int, payload: bytes) -> bytes:
    length = len(payload) + 1
    if length > 0xFFFF:
        raise ValueError("OMF record overflow")
    prefix = bytes([record_type, length & 0xFF, length >> 8])
    checksum = (-sum(prefix + payload)) & 0xFF
    return prefix + payload + bytes([checksum])


def reframe_ellen_tc4_fixupp(raw: bytes) -> bytes:
    """Split pinned TC4 Ellen LEDATA at 1000 preserving every CODE byte.

    The contract deliberately matches exactly two adjacent LEDATA/FIXUPP
    pairs, with the far-call fixup as the *first* subrecord of the first
    FIXUPP (the original TC4 enumeration). This is not a generic OMF
    rearranger. An unexpected compiler output fails rather than guessing.
    """
    original = parse_omf(raw)
    segment = 4
    left_code_prefix = bytes((segment, 0, 0))
    right_code_prefix = bytes((segment, 0, 4))
    matches = [
        i for i, r in enumerate(original)
        if r.record_type == 0xA0
        and len(r.data) == 3 + 1024
        and r.data[:3] == left_code_prefix
    ]
    if len(matches) != 1:
        raise ValueError("expected one original Ellen TC4 CODE LEDATA 0..1024")
    i = matches[0]
    if i + 3 >= len(original):
        raise ValueError("Ellen CODE FIXUPP sequence truncated")
    first_data, first_fix, second_data, second_fix = original[i:i+4]
    if (
        [r.record_type for r in (first_data, first_fix, second_data, second_fix)]
        != [0xA0, 0x9C, 0xA0, 0x9C]
        or second_data.data[:3] != right_code_prefix
        or len(second_data.data) != 3 + 54
    ):
        raise ValueError("Ellen direct TC4 must emit exactly two adjacent LEDATA/FIXUPP pairs")

    first_code = first_data.data[3:]
    second_code = second_data.data[3:]
    if (
        len(first_code + second_code) != 1078
        or first_code[1000:1005] != b"\x9a\0\0\0\0"
    ):
        raise ValueError("Ellen far SE-call instruction has moved from offset 1000")
    first_subrecord = bytes.fromhex("cf e9 56 15")
    if not first_fix.data.startswith(first_subrecord):
        raise ValueError("original TC4 far-call FIXUPP must lead the first record")
    if len(first_fix.data) <= len(first_subrecord) or not second_fix.data:
        raise ValueError("Ellen producer lost its other fixups")

    # The original second LEDATA began at 1024. Its three compiler-emitted
    # FIXUPP descriptors use 10-bit offsets relative to that LEDATA, not
    # absolute CODE positions. After moving its origin to 1000, each must
    # be rebased by +24. This preserves each exact target/frame descriptor.
    # Reject changes to the compiler's original suffix instead of trying
    # to infer an unknown FIXUPP subrecord dialect.
    original_second_fixups = bytes.fromhex(
        "c4 24 16 01 19 c4 13 16 01 18 c4 0a 16 01 02"
    )
    if second_fix.data != original_second_fixups:
        raise ValueError("Ellen subsequent TC4 FIXUPP descriptors differ from pinned shape")
    rebased_second_fixups = bytearray()
    for cursor in range(0, len(original_second_fixups), 5):
        item = original_second_fixups[cursor:cursor+5]
        if item[0] != 0xC4 or item[1] > (0xFF - 24):
            raise ValueError("Ellen second-record fixup offset out of range")
        rebased_second_fixups.extend((item[0], item[1] + 24))
        rebased_second_fixups.extend(item[2:])

    # TC4's FIXUPP subrecord encodes the *16-bit operand* starting at
    # 1001; after moving LEDATA origin to 1000, the relative location is 1.
    # All target/frame methods and indices remain byte-for-byte identical.
    migrated_subrecord = bytes.fromhex("cc 01 56 15")
    framed = [
        _record(0xA0, left_code_prefix + first_code[:1000]),
        _record(0x9C, first_fix.data[len(first_subrecord):]),
        _record(0xA0, bytes((segment, 0xE8, 0x03)) + first_code[1000:] + second_code),
        _record(0x9C, migrated_subrecord + bytes(rebased_second_fixups)),
    ]
    old_group = original[i:i+4]
    rebuilt = (
        raw[:old_group[0].offset]
        + b"".join(framed)
        + raw[old_group[-1].offset + 3 + old_group[-1].length:]
    )
    verified = parse_omf(rebuilt)
    if len(verified) != len(original):
        raise ValueError("OMF record count unexpectedly changed")
    if (
        b"".join([verified[i].data[3:], verified[i+2].data[3:]])
        != first_code + second_code
        or len(verified[i].data[3:]) != 1000
        or len(verified[i+2].data[3:]) != 78
        or verified[i+1].data != first_fix.data[4:]
        or verified[i+3].data != migrated_subrecord + bytes(rebased_second_fixups)
    ):
        raise ValueError("OMF reframing modified original compiler code or FIXUPP descriptors")
    return rebuilt


def validate_ellen_omf_recipe(producer: dict) -> str:
    """Permit exactly Ellen's pinned physical TC4 producer."""
    recipe = producer.get("tc4_omf_reframe")
    if recipe != "ellen-ledata-1000":
        raise ValueError("unknown compiler OMF record-framing recipe")
    if (
        producer.get("object") != "ex_ellen"
        or producer.get("object_path") != "obj/th03/ex_ellen.obj"
        or producer.get("wrapper") != "th03/ex_ellen.cpp"
        or producer.get("source") != "src/main/player/exatt_ellen.cpp"
        or producer.get("translator_comment", "TC86 Borland C++ 4.02")
           != "TC86 Borland C++ 4.02"
    ):
        raise ValueError("unexpected Ellen TC4 OMF producer identity")
    return producer["wrapper"]
