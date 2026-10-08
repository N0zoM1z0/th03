"""Fail-closed HUD compiler-assembly stitch and OMF FIXUPP order calibration.

The 1478-byte round intro contains two independently pinned natural TC4 C++
functions (688 and 635 bytes) and two exact 155-byte symbolic TASM helpers.
Three distinct physical objects preserve CODE/MAP, but their far relocations
arrive in object order instead of the immutable original TASM's record order.

Merge *compiler-emitted* assembly with the maintained low-level TASM body in
the original function order, then assemble one physical TASM object. The
original TASM writer emits two 1007/471-byte LEDATA/FIXUPP pairs; a scoped
reverse of their self-contained FIXUPP subrecords recovers the original
ordered MZ relocation sites. No instruction bytes, symbols, source semantics
or target comparisons are patched or relaxed.
"""

from __future__ import annotations

import re

from .omf import parse_omf
from .tc4_omf_bridge import _record

SEGMENT_DECL = b"PLAYER_M_TEXT\tsegment byte public use16 'CODE'\r\n"
SEGMENT_END = b"PLAYER_M_TEXT\tends"
LOWLEVEL_DECL = b"PLAYER_M_TEXT segment byte public 'CODE' use16\n"
LOWLEVEL_END = b"PLAYER_M_TEXT ends"
LOWLEVEL_MARKERS = (
    b"HUD_START_SPRITE_STRIP_PUT proc near",
    b"HUD_START_PARTICLE_PIXEL_PUT proc near",
    b"HUD_START_PARTICLE_PIXEL_PUT endp",
)
NATURAL_NAMES = (
    b"_hud_start_anim_update",
    b"_hud_start_anim_render",
)


def stitch_hud_compiler_asm(
    intro_tc4: bytes, render_tc4: bytes, helper_tasm: bytes
) -> bytes:
    """Join two original compiler-generated procedure bodies and full helpers.

    The C++ files are still the semantic sources; this operation does not
    invent machine instructions or load precompiled binary code.
    """
    for label, content in (("state", intro_tc4), ("renderer", render_tc4)):
        if not content.startswith(b"\t.386p\r\n"):
            raise ValueError(f"unexpected TC4-generated {label} header")
        if content.count(SEGMENT_DECL) != 3 or content.count(SEGMENT_END) != 3:
            raise ValueError(f"unreviewed {label} compiler segment layout")
        if b"\r\n\tend\r\n" not in content:
            raise ValueError(f"{label} missing TC4 assembler end")
    if helper_tasm.count(LOWLEVEL_DECL) != 1 or helper_tasm.count(LOWLEVEL_END) != 1:
        raise ValueError("symbolic TASM helper has unexpected code segment")
    if any(helper_tasm.count(tag) != 1 for tag in LOWLEVEL_MARKERS):
        raise ValueError("symbolic TASM helper body was truncated or duplicated")

    # Both original TC4 files have an empty segment, a nonempty procedure
    # segment, and a zero-byte trailing segment. Merge the two *nonempty*
    # procedure bodies in their target order without repeating either
    # compiler header, DATA/BSS group, or module END.
    first = intro_tc4.index(SEGMENT_DECL)
    state_code_start = intro_tc4.index(SEGMENT_DECL, first + len(SEGMENT_DECL))
    state_code_end = intro_tc4.index(SEGMENT_END, state_code_start)
    second = render_tc4.index(SEGMENT_DECL)
    render_code_start = render_tc4.index(SEGMENT_DECL, second + len(SEGMENT_DECL))
    render_code_end = render_tc4.index(SEGMENT_END, render_code_start)
    if (
        NATURAL_NAMES[0] not in intro_tc4[state_code_start:state_code_end]
        or NATURAL_NAMES[1] not in render_tc4[render_code_start:render_code_end]
    ):
        raise ValueError("expected both original compiler-produced functions")

    begin = helper_tasm.index(LOWLEVEL_DECL) + len(LOWLEVEL_DECL)
    stop = helper_tasm.index(LOWLEVEL_END, begin)
    helper_body = helper_tasm[begin:stop].replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    render_body = render_tc4[render_code_start+len(SEGMENT_DECL):render_code_end]
    if len(set(re.findall(rb"@1@\d+", render_body))) < 8:
        raise ValueError("unrecognized TC4J renderer label graph")

    # Compiler-private TASM labels start at @1@ in both independently
    # generated functions. Make *renderer* labels disjoint. No opcode,
    # conditional branch destination or instruction offset changes.
    render_body = re.sub(rb"@1@(\d+)", rb"HUDR_L_\1", render_body)

    # Preserve compiler-generated exported names and all exact external
    # declarations, removing only the two helper EXTDEF declarations whose
    # definitions are now in this same physical object. Never silently
    # rename any other reference.
    render_tail = render_tc4[render_code_end+len(SEGMENT_END):]
    state_tail = intro_tc4[state_code_end:]
    extra = []
    for line in render_tail.splitlines():
        if line.startswith((b"\tpublic\t", b"\tpublic ", b"\textrn\t",
                            b"\textrn ", b"_tone_")):
            if any(x in line for x in (b"HUD_START_SPRITE_STRIP_PUT", b"HUD_START_PARTICLE_PIXEL_PUT")):
                # Exact ABI helpers become local TASM PUBLIC labels.
                continue
            if line not in state_tail and line+b"\r\n" not in extra:
                extra.append(line+b"\r\n")
    if b"\tpublic\t_hud_start_anim_render\r\n" not in extra:
        raise ValueError("TC4 renderer public symbol missing")

    stitched = (
        intro_tc4[:state_code_end]
        + helper_body
        + render_body
        + intro_tc4[state_code_end:]
    )
    end_pos = stitched.rfind(b"\tend\r\n")
    if end_pos < 0:
        raise ValueError("stitched compiler object lost assembler END")
    stitched = stitched[:end_pos] + b"".join(extra) + stitched[end_pos:]
    if (
        stitched.count(b"HUD_START_SPRITE_STRIP_PUT proc near") != 1
        or stitched.count(b"HUD_START_PARTICLE_PIXEL_PUT proc near") != 1
        or stitched.count(b"\tend\r\n") != 1
        or not stitched.startswith(intro_tc4[:state_code_start])
    ):
        raise ValueError("stitched compiler assembly is not one complete module")
    return stitched


def _subrecords(data: bytes) -> list[bytes]:
    """Decode only the FIXUPP subrecord dialect emitted by pinned TASM50."""
    result = []
    cursor = 0
    while cursor < len(data):
        if cursor + 3 > len(data):
            raise ValueError("truncated HUD TASM FIXUPP subrecord")
        # 0x16 = explicit frame/target indexes (5B);
        # 0x56 = threaded frame, explicit target index (4B).
        # Both are self-contained and have no state-setting thread commands.
        size = {0x16: 5, 0x56: 4}.get(data[cursor+2])
        if size is None or cursor + size > len(data) or not(data[cursor] & 0x80):
            raise ValueError("unknown HUD TASM FIXUPP dialect")
        result.append(data[cursor:cursor+size])
        cursor += size
    return result


def reverse_hud_fixupp_order(omf: bytes) -> bytes:
    """Reorder *only* two FIXUPP record subrecords, never executable CODE."""
    records = parse_omf(omf)
    pairs = [
        i for i in range(len(records)-1)
        if records[i].record_type == 0xA0
        and records[i].data[:3] in (b"\x01\0\0", b"\x01\xef\x03")
        and records[i+1].record_type == 0x9C
    ]
    if len(pairs) != 2:
        raise ValueError("expected exactly two HUD PLAYER_M_TEXT LEDATA/FIXUPP pairs")
    starts = [records[i].data[:3] for i in pairs]
    sizes = [len(records[i].data)-3 for i in pairs]
    if starts != [b"\x01\0\0", b"\x01\xef\x03"] or sizes != [1007, 471]:
        raise ValueError("target HUD 1007/471 LEDATA physical layout moved")
    changed: dict[int, bytes] = {}
    descriptor_totals = []
    for pair_idx,count in zip(pairs,(87,57)):
        fix = records[pair_idx+1]
        parsed = _subrecords(fix.data)
        if len(parsed) != count:
            raise ValueError("unexpected HUD FIXUPP descriptor count")
        # Pinned TASM50 emits these record-relative locations ascending.
        # This prevents a second application from silently undoing the
        # exact historic reverse order.
        locations=[((x[0]&3)<<8)|x[1] for x in parsed]
        if locations != sorted(locations) or len(set(locations))!=len(locations):
            raise ValueError("HUD native FIXUPP record is not strictly ascending")
        descriptor_totals.append(len(parsed))
        changed[pair_idx+1] = _record(0x9C,b"".join(reversed(parsed)))

    rebased = b"".join(
        changed.get(i,omf[r.offset:r.offset+3+r.length])
        for i,r in enumerate(records)
    )
    after=parse_omf(rebased)
    if len(records)!=len(after):
        raise ValueError("OMF record count changed")
    for i,(a,b) in enumerate(zip(records,after)):
        if i not in changed and a.data!=b.data:
            raise ValueError("non-FIXUPP OMF record mutated")
        if i in changed and sorted(_subrecords(a.data))!=sorted(_subrecords(b.data)):
            raise ValueError("FIXUPP subrecord locations or targets mutated")
    if descriptor_totals != [87,57]:
        raise ValueError("HUD TASM record count drift")
    return rebased


def validate_hud_stitch_recipe(producer: dict) -> str:
    """Reject any source/object/wrapper substitution or generic byte patch."""
    if (
        producer.get("hud_tc4_stitch") != "hud-roundintro-1478"
        or producer.get("object") != "h_stitch"
        or producer.get("object_path") != "obj/th03/h_stitch.obj"
        or producer.get("wrapper") != "th03/h_stitch.asm"
        or producer.get("source") != "src/main/hud/start_anim.cpp"
        or producer.get("translator_comment") != "Turbo Assembler  Version 5.0"
        or producer.get("wrapper_prefix", "") != ""
    ):
        raise ValueError("unrecognized HUD TC4 compiler source/OMF producer contract")
    return producer["wrapper"]
