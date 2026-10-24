"""Negative controls for the live OP comparator, independent of old receipts."""

from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_th03_op_work import compare_mz
from test_pc98 import synthetic_mz_with_relocations


class OpWorkComparisonTests(unittest.TestCase):
    def test_reordered_relocations_fail_even_when_loaded_bytes_match(self):
        original = synthetic_mz_with_relocations(((2, 0), (4, 0)))
        reordered = synthetic_mz_with_relocations(((4, 0), (2, 0)))
        self.assertTrue(compare_mz(original, original)["file_equal"])
        result = compare_mz(reordered, original)
        self.assertTrue(result["program_equal"])
        self.assertTrue(result["relocation_membership_equal"])
        self.assertFalse(result["ordered_relocations_equal"])
        self.assertFalse(result["file_equal"])

    def test_mz_allocation_change_is_not_program_exactness(self):
        original = synthetic_mz_with_relocations(((2, 0),))
        changed = bytearray(original)
        struct.pack_into("<H", changed, 10, 0x11)
        result = compare_mz(bytes(changed), original)
        self.assertTrue(result["program_equal"])
        self.assertTrue(result["ordered_relocations_equal"])
        self.assertFalse(result["header_equal"])
        self.assertFalse(result["file_equal"])

    def test_program_growth_and_byte_changes_are_both_visible(self):
        original = synthetic_mz_with_relocations(((2, 0),))
        changed = bytearray(original)
        changed[-1] ^= 1
        result = compare_mz(bytes(changed), original)
        self.assertFalse(result["program_equal"])
        self.assertTrue(result["program_size_equal"])
        self.assertEqual(result["differing_program_sites"], [63])
        changed.append(0)
        struct.pack_into("<H", changed, 2, len(changed))
        result = compare_mz(bytes(changed), original)
        self.assertFalse(result["program_size_equal"])


if __name__ == "__main__":
    unittest.main()
