"""Whole far-heap source, sparse CS storage and offset-only native fields."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_farheap_native import verify, REPORT, BASE


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private far-heap native pair absent')
class FarHeapNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_heap_member_preserves_all_bodies_and_native_fields(self):
        row = self.check()
        self.assertEqual((row['source_CODE_bytes'], row['file_DATA_bytes'], row['procedures']), (1103, 12, 14))
        self.assertEqual(len(row['native_fields']), 49)
        self.assertTrue(row['all_49_ordered_native_fields_equal_original'])
        self.assertEqual((row['normal_library_members'], row['untouched_library_members']), (893, 892))
        self.assertEqual((row['initialized_CS_state_bytes'], row['uninitialized_CS_scratch_file_bytes']), (6, 6))
        self.assertFalse(row['CS_scratch_initializer_added'])
        self.assertFalse(row['source_padding_added'])
        self.assertTrue(row['whole_EXE_MAP_equal'])
        self.assertTrue(row['full_raw_vector_repeated'])
        owner, = row['owners']
        self.assertEqual(owner['size'], 1115)
        self.assertEqual(sum(p['size'] for p in owner['procedures']), 1103)

    def test_equal_corrupted_scratch_cannot_hide_actual_repeated_link_bytes(self):
        image = bytearray(self.target.program_image)
        image[BASE + 6] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_equal_corrupted_heap_call_cannot_hide_native_fixup_resolution(self):
        image = bytearray(self.target.program_image)
        image[BASE + 0x69] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_cs_state_offset_does_not_gain_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=BASE + 15)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
