"""Complete native CRT ownership, shared entry ABI and the DOS error DATA map."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_crt_native import verify


@unittest.skipUnless((build.WORK / 'owned/fbrk.obj').is_file(), 'private CRT pair absent')
class CRTNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_source_members_keep_near_far_entries_and_aliases_separate(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['procedures'], row['source_CODE_bytes'],
                          row['source_initialized_DATA_bytes']), (8, 13, 628, 93))
        self.assertEqual(sum(len(m['fields']) for m in row['native_modules']), 39)
        self.assertEqual((row['near_to_far_shim_entries'], row['distinct_far_body_entries']), (3, 3))
        self.assertTrue(row['aliases_add_no_procedures'])
        fbrk, = [o for o in row['owners'] if o['unit_id'].endswith('-fbrk')]
        self.assertEqual([p['size'] for p in fbrk['procedures']], [142, 67, 143])
        self.assertEqual(fbrk['procedures'][0]['callee_pop_bytes'], 4)
        self.assertEqual(row['natural_far_calls'], [dict(site=0x3EBC, symbol='_setblock', target=0x8E5A)])
        self.assertEqual((row['DOS_error_map_entries'], row['reused_cold_rounds'],
                          row['retained_full_raw_outputs']), (89, 2, 938))
        self.assertFalse(row['native_rebuild_required'])
        self.assertFalse(row['source_padding_added'])

    def test_equal_corrupted_heap_far_call_cannot_hide_native_field_mismatch(self):
        image = bytearray(self.target.program_image)
        image[0x3EBC] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_named_error_map_requires_all_native_data_bytes(self):
        image = bytearray(self.target.program_image)
        image[0xE3F * 16 + 0xE90 + 87] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_near_pointer_word_field_does_not_gain_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x3F12)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
