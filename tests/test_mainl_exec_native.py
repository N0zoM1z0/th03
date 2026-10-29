"""DOS copied continuation, uninitialized work storage and combined CRT linking."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_exec_native import verify, REPORT, BASE


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private overlay native pair absent')
class ExecNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_overlay_and_reused_farheap_coexist_in_normal_library(self):
        row = self.check()
        self.assertEqual((row['source_CODE_bytes'], row['file_DATA_bytes'], row['procedures']), (671, 262, 2))
        self.assertEqual(len(row['native_fields']), 21)
        self.assertEqual([f['site'] for f in row['equivalent_DGROUP_frame_changes']], [371, 397, 482, 560])
        self.assertEqual((row['copied_continuation_bytes'], row['copy_region_bytes'], row['copy_relative_entry_offset']), (97, 352, 255))
        self.assertEqual((row['initialized_CS_bytes'], row['uninitialized_CS_file_bytes']), (5, 257))
        self.assertFalse(row['source_work_buffer_initializer_added'])
        self.assertEqual((row['normal_library_members'], row['untouched_current_library_members'], row['source_CRT_providers_in_selected_library']), (893, 891, 8))
        self.assertTrue(row['reused_natural_farheap'])
        self.assertTrue(row['whole_EXE_MAP_equal'])
        self.assertFalse(row['source_padding_added'])

    def test_equal_corrupted_work_storage_cannot_hide_real_native_links(self):
        image = bytearray(self.target.program_image)
        image[BASE] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_copied_transfer_uses_the_original_relative_mz_entry(self):
        image = bytearray(self.target.program_image)
        image[BASE + 0x14D] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_dgroup_startup_word_reference_is_not_a_segment_immediate(self):
        extra = replace(self.target.relocations[0], segment=0, offset=BASE + 0x379)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
