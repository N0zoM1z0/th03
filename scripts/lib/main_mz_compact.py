"""Standard minimal DOS MZ container serializer for a retained source-native EXE.

No Japanese target bytes, object patches, opcode arrays or post-linked code
changes are used. Convert the *native* MZ load program and ordered relocation
records to the smallest paragraph-aligned DOS header permitted by their count.
The original TLINK file is never modified in place.
"""
import struct

from lib.pc98 import parse_mz

MZ_FIXED_HEADER_BYTES = struct.calcsize('<14H')
MZ_RELOCATION_BYTES = struct.calcsize('<HH')
MZ_PARAGRAPH = 16
MZ_PAGE = 512


def compact_mz(native_exe: bytes) -> bytes:
    """Re-encode one native DOS MZ with a minimal relocation-table header.

    This intentionally does not solve code differences. The complete program
    image and relocation contents are read only from native_exe, and none of
    the original game's target bytes are available to this function.
    """
    original = parse_mz(native_exe)
    h = original.header
    relocations = original.relocations
    if (h.magic != 0x5A4D or h.overlay_number != 0 or
            h.number_of_relocations != len(relocations) or
            h.relocation_table_offset < MZ_FIXED_HEADER_BYTES or
            h.header_paragraphs * MZ_PARAGRAPH > len(native_exe)):
        raise ValueError('nonstandard/invalid original native DOS MZ container')
    first_word_after_relocs = h.relocation_table_offset + len(relocations) * MZ_RELOCATION_BYTES
    if first_word_after_relocs > h.header_paragraphs * MZ_PARAGRAPH:
        raise ValueError('native MZ relocation table exceeds header allocation')
    header_length = MZ_FIXED_HEADER_BYTES + len(relocations) * MZ_RELOCATION_BYTES
    if header_length % MZ_PARAGRAPH:
        raise ValueError('reconstructed relocation count does not end on a DOS paragraph')
    new_file_size = header_length + len(original.program_image)
    pages, trailing = divmod(new_file_size, MZ_PAGE)
    if trailing:
        pages += 1
    if pages > 0xFFFF or new_file_size > MZ_PAGE * 0xFFFF:
        raise ValueError('cannot represent compact size in DOS MZ page fields')

    # All fourteen words come from the native emitted MZ and the DOS
    # specification: four size/layout fields are derived from the native
    # image and relocation count, never from a target reference EXE.
    fixed = struct.pack(
        '<14H',
        h.magic, trailing, pages, len(relocations),
        header_length // MZ_PARAGRAPH,
        h.minimum_extra_allocation, h.maximum_extra_allocation,
        h.initial_relative_ss, h.initial_sp, h.checksum,
        h.initial_ip, h.initial_relative_cs,
        MZ_FIXED_HEADER_BYTES, h.overlay_number,
    )
    table = b''.join(struct.pack('<HH', row.offset, row.segment) for row in relocations)
    result = fixed + table + original.program_image

    # Verify the independent DOS parser, not a target game data comparison.
    checked = parse_mz(result)
    if (checked.program_image != original.program_image or
            checked.relocations != relocations or
            checked.header.header_paragraphs != header_length // MZ_PARAGRAPH or
            checked.header.relocation_table_offset != MZ_FIXED_HEADER_BYTES or
            len(result) != new_file_size):
        raise AssertionError('semantic MZ reserialization failed its own roundtrip')
    return result
