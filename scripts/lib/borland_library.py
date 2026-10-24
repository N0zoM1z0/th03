"""Read normal OMF libraries without rewriting their members or dictionaries.

TLIB's A3 member-name comment is library bookkeeping, and its checksum is not
maintained in the pinned vendor library. Every other module record must retain
its standalone checksum. A3/THEADR identity records never supply program bytes.
"""

from dataclasses import dataclass
import re
import struct

from lib.omf import parse_omf


def need(value, message):
    if not value:
        raise ValueError(message)


@dataclass(frozen=True)
class LibraryMember:
    name: str
    program_records: bytes


def is_member_name(kind, data):
    return kind == 0x88 and data[:2] == b"\x00\xa3"


def object_program_records(raw):
    records = parse_omf(raw)
    return b"".join(raw[r.offset:r.offset + r.length + 3] for r in records
                    if r.record_type != 0x80 and not is_member_name(r.record_type, r.data))


def library_members(raw):
    need(len(raw) >= 16 and raw[0] == 0xF0, "OMF library header required")
    page = struct.unpack_from("<H", raw, 1)[0] + 3
    need(16 <= page <= 32768 and page & (page - 1) == 0, "invalid library page size")
    dictionary, blocks = struct.unpack_from("<IH", raw, 3)
    need(page <= dictionary <= len(raw) and dictionary + blocks * 512 <= len(raw),
         "library dictionary out of bounds")
    cursor = page
    members = []
    names = set()
    while cursor < dictionary and raw[cursor] == 0x80:
        name = None
        program = []
        first = True
        while True:
            need(cursor + 3 <= dictionary, "truncated member record header")
            kind = raw[cursor]
            size = struct.unpack_from("<H", raw, cursor + 1)[0]
            end = cursor + size + 3
            need(size >= 1 and end <= dictionary, "member record exceeds library body")
            data = raw[cursor + 3:end - 1]
            frame = raw[cursor:end]
            metadata = is_member_name(kind, data)
            need(metadata or sum(frame) & 255 == 0, "member record checksum failed")
            need(first or kind != 0x80, "nested THEADR in member")
            if metadata:
                need(name is None and len(data) >= 3 and len(data) == 3 + data[2],
                     "ambiguous TLIB member name")
                name = data[3:].decode("ascii")
                need(re.fullmatch(r"[a-zA-Z0-9_@$]{1,8}", name), "unsafe member filename")
            elif kind != 0x80:
                program.append(frame)
            first = False
            cursor = end
            if kind in (0x8A, 0x8B):
                break
        need(name is not None and name.casefold() not in names, "missing/duplicate member name")
        names.add(name.casefold())
        members.append(LibraryMember(name, b"".join(program)))
        next_page = (cursor + page - 1) // page * page
        need(not any(raw[cursor:next_page]), "nonzero inter-member padding")
        cursor = next_page
    need(cursor + 3 <= dictionary and raw[cursor] == 0xF1, "missing library terminator")
    end = cursor + struct.unpack_from("<H", raw, cursor + 1)[0] + 3
    need(end == dictionary and not any(raw[cursor + 3:end]), "invalid library terminator")
    return members


def compare_members(original, candidate, replacements):
    """Check literal order, untouched context, and each fresh source producer."""
    need([m.name for m in candidate] == [m.name for m in original], "library member order changed")
    need(set(replacements) <= {m.name for m in original}, "replacement is not an original member")
    for before, after in zip(original, candidate):
        expected = (object_program_records(replacements[before.name])
                    if before.name in replacements else before.program_records)
        need(after.program_records == expected, "library program records changed: " + before.name)
    return dict(member_count=len(original), replaced_members=sorted(replacements),
                contextual_members_unchanged=len(original) - len(replacements),
                ordered_members_equal=True, fresh_producers_equal=True)
