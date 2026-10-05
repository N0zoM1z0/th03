"""Negative controls for complete, unnormalized owned-extent comparison."""
import struct
import unittest

from test_pc98 import synthetic_mz, synthetic_mz_with_relocations
from replay_th03_main_exact_units import compare_extent
from lib.pc98 import parse_mz


class MainExactOracleTests(unittest.TestCase):
    def test_equal_payload_can_have_different_header_size(self):
        a = synthetic_mz_with_relocations(((2, 0),))
        b = bytearray(a[:32] + bytes(16) + a[32:])
        struct.pack_into("<H", b, 8, 3)
        struct.pack_into("<H", b, 2, len(b))
        result = compare_extent(a, bytes(b), 0, 64)
        self.assertTrue(result["raw_equal"])
        self.assertTrue(result["relocations_equal"])
        self.assertNotEqual(result["target_file_offset"], result["candidate_file_offset"])

    def test_last_owned_byte_is_not_omitted(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 15] ^= 1
        result = compare_extent(a, bytes(b), 0, 16)
        self.assertFalse(result["raw_equal"])
        self.assertEqual(result["differing_bytes"], 1)

    def test_relocated_word_values_are_never_masked(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 2] ^= 1
        result = compare_extent(a, bytes(b), 0, 16)
        self.assertFalse(result["raw_equal"])
        self.assertTrue(result["relocations_equal"])

    def test_relocation_order_and_duplicates_are_not_sets(self):
        a = synthetic_mz_with_relocations(((2, 0), (4, 0), (4, 0)))
        b = synthetic_mz_with_relocations(((4, 0), (2, 0), (4, 0)))
        c = synthetic_mz_with_relocations(((2, 0), (4, 0), (2, 0)))
        for changed in (b, c):
            self.assertTrue(compare_extent(a, changed, 0, 16)["raw_equal"])
            self.assertFalse(compare_extent(a, changed, 0, 16)["relocations_equal"])

    def test_outside_bytes_do_not_receive_owned_extent_credit(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 40] ^= 1
        self.assertTrue(compare_extent(a, bytes(b), 0, 16)["raw_equal"])

    def test_split_relocation_and_out_of_bounds_are_rejected(self):
        a = synthetic_mz()
        for start, size in ((0, 3), (3, 8), (0, 65), (-1, 8), (0, 0)):
            with self.assertRaises(ValueError):
                compare_extent(a, a, start, size)

    def test_invalid_container_is_rejected(self):
        a = synthetic_mz()
        b = bytearray(a)
        struct.pack_into("<H", b, 2, 600)
        self.assertFalse(parse_mz(bytes(b)).valid)
        with self.assertRaises(ValueError):
            compare_extent(a, bytes(b), 0, 16)


if __name__ == "__main__":
    unittest.main()
