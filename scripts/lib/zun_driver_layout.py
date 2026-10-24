"""Complete tiny-driver names, widths, segment/group and public-address checks.

Resolve OMF name indices rather than treating one assembler's LNAMES ordering
as physical layout. The target comparison and cold object comparison stay raw.
"""

import re

from lib.omf import parse_omf
from verify_th03_zun_driver_hybrid import (RESIDENT_PROCS, COMMAND_PROCS,
                                         SCATTERED_PROCS, PUBLICS, index,
                                         map_boundaries)


CONTRIBUTIONS = (("_TEXT", 0, 0x516, 0x48), ("SPR_MASK", 0x520, 0x111, 0x68),
                 ("SPR_PRINT", 0x640, 0x65, 0x68), ("SPR_FMT", 0x6B0, 0x26C, 0x68),
                 ("SPR_CMD", 0x920, 0x169, 0x68), ("SPR_NUM", 0xA90, 0x136, 0x68),
                 ("SPR_EGC", 0xBD0, 0x6C, 0x68), ("SPR_STR", 0xC40, 0x36, 0x68),
                 ("SPR_DATA", 0xC80, 0x500, 0x68))


def need(value, message):
    if not value:
        raise ValueError(message)


def public_contract():
    return dict(start=0x100,
                **{n: a for n, a, _ in (*RESIDENT_PROCS, *COMMAND_PROCS, *SCATTERED_PROCS)},
                **{n: a for n, a in PUBLICS.items() if n != "start"})


def object_layout(raw):
    records = parse_omf(raw)
    names = [None]
    for rec in records:
        if rec.record_type != 0x96:
            continue
        at = 0
        while at < len(rec.data):
            size = rec.data[at]
            at += 1
            need(at + size <= len(rec.data), "truncated OMF name")
            names.append(rec.data[at:at + size].decode("ascii"))
            at += size
    def name(i):
        need(0 < i < len(names), "OMF name index out of bounds")
        return names[i]
    segments, attributes, groups, local_publics = [], [], [], []
    for rec in records:
        data, kind = rec.data, rec.record_type
        need(kind not in {0x99, 0x91, 0x8C, 0xB4}, "unexpected wide/external driver record")
        if kind == 0x98:
            need(len(data) >= 6 and data[0] in (0x48, 0x68), "WORD or PARA/public/USE16 segment required")
            n, at = index(data, 3)
            cls, at = index(data, at)
            overlay, at = index(data, at)
            need(at == len(data) and name(overlay) == "", "segment overlay/tail drift")
            segments.append(dict(name=name(n), cls=name(cls), size=int.from_bytes(data[1:3], "little")))
            attributes.append(data[0])
        elif kind == 0x9A:
            n, at = index(data, 0)
            members = []
            while at < len(data):
                need(data[at] == 0xFF, "non-segment group member")
                member, at = index(data, at + 1)
                members.append(member)
            groups.append(dict(name=name(n), members=members))
        elif kind == 0x90:
            group, at = index(data, 0)
            segment, at = index(data, at)
            need(group == 1 and segment > 0, "public outside tiny CODE group")
            while at < len(data):
                size = data[at]
                at += 1
                need(size > 0 and at + size + 2 < len(data), "truncated public")
                symbol = data[at:at + size].decode("ascii")
                at += size
                offset = int.from_bytes(data[at:at + 2], "little")
                typ, at = index(data, at + 2)
                need(symbol not in [p[0] for p in local_publics] and typ == 0, "duplicate/typed public")
                local_publics.append((symbol, segment, offset))
    segmented = len(segments) == 10
    if segmented:
        expected = [dict(name="_TEXT", cls="CODE", size=0x516), dict(name="_DATA", cls="DATA", size=0)]
        expected += [dict(name=n, cls="CODE", size=size) for n, _, size, _ in CONTRIBUTIONS[1:]]
        need(segments == expected and attributes == [0x48, 0x48] + [0x68] * 8, "native paragraph CODE contribution layout")
        starts = {1: 0, 2: 0x1180, **{i + 3: at for i, (_, at, _, _) in enumerate(CONTRIBUTIONS[1:])}}
        profile = "native-paragraph-contributions"
    else:
        need(segments == [dict(name="_TEXT", cls="CODE", size=0x1180),
                          dict(name="_DATA", cls="DATA", size=0)] and attributes == [0x48, 0x48], "complete tiny segment layout drift")
        starts, profile = {1: 0, 2: 0x1180}, "historical-monolithic"
    need(groups == [dict(name="DGROUP", members=list(range(1, len(segments) + 1)))], "tiny group membership/order drift")
    publics = {}
    for symbol, segment, offset in local_publics:
        need(segment in starts and segments[segment - 1]["cls"] == "CODE"
             and offset < segments[segment - 1]["size"], "public inside initialized CODE contribution")
        publics[symbol] = starts[segment] + offset
    need(publics == public_contract(), "complete 55-procedure public ABI drift")
    return dict(segments=segments, groups=groups, publics=publics,
                use16=True, word_alignment=True, omf_records=len(records), layout_profile=profile,
                segment_attributes=attributes, segment_starts={str(k): v for k, v in starts.items()})


def review(raw_obj, raw_map):
    result = object_layout(raw_obj)
    if result["layout_profile"] == "historical-monolithic":
        result["map_public_tables"] = len(map_boundaries(raw_map, public_contract()))
        return result
    text = raw_map.decode("ascii")
    for name, at, size, attr in (*CONTRIBUTIONS, ("_DATA", 0x1180, 0, 0x48)):
        cls = "DATA" if name == "_DATA" else "CODE"
        need(len(re.findall(rf"(?m)^\s*{at:05X}H\s+{at + size - 1 if size else at:05X}H\s+{size:05X}H\s+{name}\s+{cls}\s*$", text)) == 1,
             "complete MAP paragraph allocation")
        need(len(re.findall(rf"(?m)^\s*0000:{at:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G=DGROUP\s+M=driver\.asm\s+ACBP={attr:02X}\s*$", text)) == 1,
             "literal MAP contribution owner/alignment")
    sections = re.split(r"Address\s+Publics by (?:Name|Value)", text)
    need(len(sections) == 3, "two native MAP public tables")
    for section in sections[1:]:
        rows = {}
        for line in section.splitlines():
            if not line.strip(): continue
            match = re.fullmatch(r"\s*0000:([0-9A-Fa-f]+)\s+(?:idle\s+)?([A-Za-z_][A-Za-z_0-9]*)\s*", line)
            need(match is not None and match[2] not in rows, "exact MAP public grammar/uniqueness")
            rows[match[2]] = int(match[1], 16)
        need(rows == public_contract(), "complete paragraph MAP public ABI")
    result["map_public_tables"] = 2
    gaps = [[a + size, b] for (_, a, size, _), (_, b, _, _) in zip(CONTRIBUTIONS, CONTRIBUTIONS[1:])]
    need(all(b == (a + 15) & ~15 for a, b in gaps), "natural PARA alignment arithmetic")
    result.update(alignment_gaps=gaps, linker_zero_bytes=sum(b - a for a, b in gaps), explicit_gap_fillers=0)
    return result


def resolve_native(raw):
    """Resolve real OMF offsets into a separate comparison image; never edit OBJ.

    CODE contributions precede the empty DATA class in the linked COM. Only
    the observed group/segment-relative WORD/DWORD fixup forms are admitted.
    """
    layout = object_layout(raw)
    starts = {int(k): v for k, v in layout["segment_starts"].items()}
    records = parse_omf(raw)
    need(records[0].name == "THEADR" and records[0].data == b"\x0Adriver.asm"
         and records[-1].name == "MODEND" and records[-1].data == bytes.fromhex("c11001010001"), "native module and COM entry")
    need(all(r.name in {"THEADR", "LNAMES", "SEGDEF", "COMENT", "GRPDEF", "PUBDEF", "LEDATA", "FIXUPP", "FIXUPP32", "MODEND"}
             for r in records), "complete reviewed native record types")
    image, covered, blocks, fixups = bytearray(0x1080), set(), [], []
    block = None
    for rec in records:
        d = rec.data
        if rec.name == "LEDATA":
            segment, pos = index(d, 0)
            offset = int.from_bytes(d[pos:pos + 2], "little"); payload = d[pos + 2:]
            need(segment in starts and layout["segments"][segment - 1]["cls"] == "CODE" and payload
                 and offset + len(payload) <= layout["segments"][segment - 1]["size"], "native initialized segment bounds")
            address = starts[segment] + offset
            need(address >= 0x100, "COM ORG bytes are not file storage")
            extent = set(range(address, address + len(payload)))
            need(not covered & extent, "nonoverlapping initialized native records")
            covered.update(extent); image[address - 256:address - 256 + len(payload)] = payload
            block = (address, len(payload)); blocks.append([address, len(payload)])
        elif rec.name in ("FIXUPP", "FIXUPP32"):
            need(block is not None, "native fixup follows initialized bytes")
            pos = 0
            while pos < len(d):
                need(pos + 3 <= len(d), "complete native fixup")
                loc, low, fd = d[pos:pos + 3]; pos += 3
                width = 4 if rec.name == "FIXUPP32" else 2
                need(loc & 0x80 and (loc >> 2 & 15) == (9 if width == 4 else 1)
                     and fd in (0x14, 0x54), "literal WORD/DWORD offset fixup")
                frame = None
                if fd == 0x14: frame, pos = index(d, pos)
                target, pos = index(d, pos)
                need(target in starts and target != 2 and ((fd == 0x14 and frame == 1)
                     or (fd == 0x54 and frame is None and target == 1)), "native zero-base DGROUP/target frame")
                site = (loc & 3) * 256 + low
                need(site + width <= block[1], "native fixup inside producing record")
                address = block[0] + site
                need(all(address + width <= f["address"] or f["address"] + f["width"] <= address for f in fixups), "nonoverlapping literal fixups")
                addend = int.from_bytes(image[address - 256:address - 256 + width], "little")
                target_address = starts[target] + addend
                relative = not bool(loc & 0x40)
                resolved = (target_address - (address + width) if relative else target_address) & ((1 << (width * 8)) - 1)
                image[address - 256:address - 256 + width] = resolved.to_bytes(width, "little")
                fixups.append(dict(address=address, width=width, fixdat=fd, frame=frame, target=target,
                                   self_relative=relative, target_address=target_address, resolved=resolved))
    expected = set()
    for segment, start in starts.items():
        if segment == 2: continue
        expected.update(range(start + (0x100 if segment == 1 else 0), start + layout["segments"][segment - 1]["size"]))
    need(covered == expected, "complete initialized native contributions")
    segmented = layout["layout_profile"] == "native-paragraph-contributions"
    need(len(fixups) == (206 if segmented else 152), "complete ordered native fixup count")
    need(sum(f["self_relative"] for f in fixups) == (54 if segmented else 0)
         and sum(f["width"] == 4 for f in fixups) == 1, "complete native fixup widths/relative modes")
    return bytes(image), fixups, blocks
