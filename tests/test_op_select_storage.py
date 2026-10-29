"""Natural state alignment and complete initialized selection storage proof."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_select_storage import verify, REPORT, DS, DATA


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected producer/link pair absent')
class SelectionStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_state_and_data_from_two_real_selected_links(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual(row['initialized_data_bytes'], 227)
        self.assertEqual(len(row['native_DATA_fields']), 9)
        self.assertEqual(len(row['literals']), 16)
        self.assertEqual(row['native_CODE_bytes'], 2858)
        self.assertEqual(row['native_CODE_fields'], 272)
        self.assertEqual(row['BSS_alignment_gaps'], [1, 11])
        self.assertEqual(row['bss_bytes'], 23)
        self.assertEqual(row['BSS_raw_byte_credit'], 0)
        self.assertEqual(row['selected_compile_link_rounds'], 2)
        self.assertEqual(row['context_objects_reused'], 29)
        self.assertFalse(row['source_only_cold_rebuild_claimed'])
        self.assertFalse(row['legacy_dummy_padding_accepted'])

    def test_equal_corrupted_data_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[DS * 16 + DATA + 77] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_nine_far_pointer_mz_entries_keep_literal_emission_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if DS * 16 + DATA <= r.linear < DS * 16 + DATA + 227]
        self.assertEqual(len(slots), 9)
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
