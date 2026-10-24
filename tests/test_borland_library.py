"""Independent format/ownership controls for the native TLIB review."""

from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.borland_library import compare_members, library_members


def record(kind, data):
    raw = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return raw + bytes([-sum(raw) & 255])


def obj(name, code):
    filename = (name + ".asm").encode()
    return (record(0x80, bytes([len(filename)]) + filename)
            + record(0xA0, b"\x01\0\0" + code) + record(0x8A, b"\0"))


def library(entries):
    raw = bytearray(16)
    raw[0] = 0xF0
    struct.pack_into("<H", raw, 1, 13)
    struct.pack_into("<IH", raw, 3, 512, 1)
    for name, module in entries:
        head_end = 3 + struct.unpack_from("<H", module, 1)[0]
        metadata = bytearray(record(0x88, b"\x00\xa3" + bytes([len(name)]) + name.encode()))
        metadata[-1] ^= 1  # The one permitted vendor dictionary comment exception.
        raw += module[:head_end] + metadata + module[head_end:]
        raw += bytes(-len(raw) % 16)
    size = 512 - len(raw) - 3
    raw += b"\xf1" + struct.pack("<H", size) + bytes(size)
    return bytes(raw) + bytes(512)


class BorlandLibraryTests(unittest.TestCase):
    def setUp(self):
        self.a = obj("a", b"\x90\xcb")
        self.b = obj("b", b"\x31\xc0\xcb")
        self.original = library_members(library([("a", self.a), ("b", self.b)]))

    def test_context_and_actual_source_replacement_pass(self):
        replacement = obj("a", b"\x40\xcb")
        candidate = library_members(library([("a", replacement), ("b", self.b)]))
        result = compare_members(self.original, candidate, {"a": replacement})
        self.assertEqual(result["contextual_members_unchanged"], 1)
        self.assertEqual(result["replaced_members"], ["a"])

    def test_same_member_set_in_different_order_fails(self):
        reordered = library_members(library([("b", self.b), ("a", self.a)]))
        with self.assertRaisesRegex(ValueError, "order changed"):
            compare_members(self.original, reordered, {})

    def test_valid_checksum_cannot_hide_context_code_change(self):
        changed = library_members(library([("a", self.a), ("b", obj("b", b"\x90\xcb"))]))
        with self.assertRaisesRegex(ValueError, "records changed: b"):
            compare_members(self.original, changed, {})

    def test_source_replacement_must_be_consumed_literally(self):
        with self.assertRaisesRegex(ValueError, "records changed: a"):
            compare_members(self.original, self.original, {"a": obj("a", b"\x40\xcb")})

    def test_bad_code_checksum_is_not_library_metadata(self):
        raw = bytearray(library([("a", self.a)]))
        raw[raw.index(b"\x90\xcb")] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum failed"):
            library_members(bytes(raw))

    def test_duplicate_names_and_truncated_dictionary_fail(self):
        with self.assertRaisesRegex(ValueError, "duplicate member"):
            library_members(library([("a", self.a), ("A", self.a)]))
        with self.assertRaisesRegex(ValueError, "dictionary out of bounds"):
            library_members(library([("a", self.a)])[:-1])


if __name__ == "__main__":
    unittest.main()
