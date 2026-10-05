"""Synthetic negative controls; no game assets or executable fixtures."""
import sys
import struct
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from lib.zun import parse_launcher, DIRECTORY_SIZE


def fixture():
    size = 16
    start = size + DIRECTORY_SIZE
    data = bytearray(b"\0" * size)
    data += struct.pack("<H", 2)
    data += b"-1      -2      " + b" " * (30 * 8)
    data += struct.pack("<33H", 0x100 + start, 0x100 + start + 2,
                        0x100 + start + 4, *([0] * 30))
    data += b"\xe8" + struct.pack("<h", 4)
    data += b"ABCD\xf3\xa4\x58\xb8\x00\x01\x50\xc3"
    return data, size


class DirectoryTests(unittest.TestCase):
    def test_complete_partition(self):
        data, size = fixture()
        result = parse_launcher(data, size)
        self.assertEqual([p["size"] for p in result["payloads"]], [2, 2])
        self.assertEqual(result["helper_offset"], len(data) - 8)

    def test_bad_directory_fields(self):
        for offset, value in [(16, 33), (18 + 16, 0), (18 + 256, 0),
                              (18 + 256 + 6, 1)]:
            data, size = fixture()
            data[offset] = value
            with self.assertRaises(ValueError):
                parse_launcher(data, size)

    def test_overlap_and_bad_call(self):
        data, size = fixture()
        data[18 + 256 + 2:18 + 256 + 4] = data[18 + 256:18 + 256 + 2]
        with self.assertRaisesRegex(ValueError, "partition"):
            parse_launcher(data, size)
        data, size = fixture()
        data[size + DIRECTORY_SIZE - 2] += 1
        with self.assertRaisesRegex(ValueError, "trailing helper"):
            parse_launcher(data, size)

    def test_helper_mutation_and_truncation(self):
        data, size = fixture()
        data[-1] = 0xcb
        with self.assertRaisesRegex(ValueError, "helper"):
            parse_launcher(data, size)
        with self.assertRaises(ValueError):
            parse_launcher(data[:20], size)
