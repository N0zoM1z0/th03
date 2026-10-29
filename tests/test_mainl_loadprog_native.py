"""Program loader callback ABI, path DATA and real emitted field order."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_loadprog_native import verify, REPORT, BASE, DS, DATA_BASE


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private loader pair absent')
class LoadProgramNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_loader_keeps_native_order_and_combined_source_providers(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['source_CODE_bytes'], row['source_initialized_DATA_bytes'], row['procedures']), (2, 871, 40, 3))
        self.assertEqual(len(row['native_fields']), 32)
        self.assertNotEqual([f['site'] for f in row['native_fields']], [f['site'] for f in row['original_literal_native_fields']])
        self.assertEqual(len(row['far_calls']), 14)
        self.assertEqual(row['equivalent_near_constructor_frame_sites'], [633, 754])
        self.assertEqual((row['normal_library_members'], row['untouched_current_library_members'], row['source_CRT_providers_in_selected_library']), (893, 890, 9))
        self.assertEqual([p['size'] for p in row['owners'][0]['procedures']], [132, 137, 602])
        self.assertTrue(row['whole_EXE_MAP_equal'])
        self.assertFalse(row['source_padding_added'])

    def test_equal_corrupted_near_callback_cannot_hide_native_body(self):
        image = bytearray(self.target.program_image)
        image[BASE + 0x33C] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_suffix_table_requires_all_semantic_native_bytes(self):
        image = bytearray(self.target.program_image)
        image[DS * 16 + DATA_BASE + 18] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_indirect_far_callback_offset_does_not_gain_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=BASE + 792)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
