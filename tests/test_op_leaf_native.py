"""Specific helper ABI, explicit trailer and literal-pool ownership questions."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_leaf_native import verify, CS, PROBE
from lib.op_title_storage import verify as title_storage, DS, DATA


@unittest.skipUnless((ROOT / PROBE).is_file(), 'private scoped sound compilations absent')
class LeafNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_four_complete_functions_and_repeated_pragma_free_emission(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([o['size'] for o in row['owners']], [29, 57, 26, 30])
        self.assertEqual([len(o['native_fields']) for o in row['native_objects']], [3, 4, 0, 1])
        self.assertEqual([len(o['natural_body']['outputs']) for o in row['native_objects'][:2]], [2, 2])
        self.assertFalse(row['legacy_codestrings_accepted'])
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']), 0)

    def test_equal_corrupted_sound_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x4A + 24] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_helper_only_scope_excludes_both_explicit_trailers(self):
        raw = bytearray(self.target.program_image)
        for off in (0x67, 0xA1):
            raw[CS * 16 + off] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        row = verify(ROOT, self.work, bad, bad, self.files)
        self.assertEqual(row['code_bytes'], 142)
        self.assertEqual(row['excluded_tail_extents'], [[CS, 0x67, 1], [CS, 0xA1, 1]])

    def test_title_pool_has_four_complete_literals_and_no_pointer_credit(self):
        row = title_storage(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual(row['CODE_DATA_addends'], [0, 10, 15, 23])
        self.assertEqual([l['text'] for l in row['literals']], ['opwin.bft', 'op.m', 'TL01.PI', 'TL02.PI'])
        self.assertEqual(row['initialized_data_bytes'], 31)
        self.assertFalse(row['following_alignment_accepted'])

    def test_equal_corrupted_title_pool_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[DS * 16 + DATA + 15] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            title_storage(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
