"""Complete tiny-driver names, widths, segment/group and public-address checks.

Resolve OMF name indices rather than treating one assembler's LNAMES ordering
as physical layout. The target comparison and cold object comparison stay raw.
"""

from lib.omf import parse_omf
from verify_th03_zun_driver_hybrid import (RESIDENT_PROCS, COMMAND_PROCS,
                                         SCATTERED_PROCS, PUBLICS, index,
                                         map_boundaries)


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
    segments, groups, publics = [], [], {}
    for rec in records:
        data, kind = rec.data, rec.record_type
        need(kind not in {0x99, 0x91, 0x8C, 0xB4}, "unexpected wide/external driver record")
        if kind == 0x98:
            need(len(data) >= 6 and data[0] == 0x48, "WORD/public/USE16 segment required")
            n, at = index(data, 3)
            cls, at = index(data, at)
            overlay, at = index(data, at)
            need(at == len(data) and name(overlay) == "", "segment overlay/tail drift")
            segments.append(dict(name=name(n), cls=name(cls), size=int.from_bytes(data[1:3], "little")))
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
            need((group, segment) == (1, 1), "public outside tiny CODE group")
            while at < len(data):
                size = data[at]
                at += 1
                need(size > 0 and at + size + 2 < len(data), "truncated public")
                symbol = data[at:at + size].decode("ascii")
                at += size
                offset = int.from_bytes(data[at:at + 2], "little")
                typ, at = index(data, at + 2)
                need(symbol not in publics and typ == 0, "duplicate/typed public")
                publics[symbol] = offset
    need(segments == [dict(name="_TEXT", cls="CODE", size=0x1180),
                      dict(name="_DATA", cls="DATA", size=0)], "complete tiny segment layout drift")
    need(groups == [dict(name="DGROUP", members=[1, 2])], "tiny group membership/order drift")
    need(publics == public_contract(), "complete 55-procedure public ABI drift")
    return dict(segments=segments, groups=groups, publics=publics,
                use16=True, word_alignment=True, omf_records=len(records))


def review(raw_obj, raw_map):
    result = object_layout(raw_obj)
    result["map_public_tables"] = len(map_boundaries(raw_map, public_contract()))
    return result
