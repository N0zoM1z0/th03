"""True original 459-byte DOS open, 20 fields and normal 40-source MAINL."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_open_work import REPORT
from review_th03_mainl_open_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),
                     'original 40-source open native writer pair not retained')
class OriginalOpen(unittest.TestCase):
    def test_full_DOS_open_code_fixups_and_original_japanese_link(self):
        r=review()
        self.assertEqual((r['original_open_CODE_bytes'],
                          r['source_open_CODE_bytes']),(459,459))
        self.assertTrue(r['native_CODE_bytes_exact'])
        self.assertEqual((r['original_private_dos_create_bytes'],
                          r['original_private_truncate_bytes'],
                          r['original_far_open_bytes']),(31,22,406))
        self.assertEqual(r['far_public_open_offset'],53)
        self.assertEqual(r['original_ordered_OMF_FIXUPPs'],20)
        self.assertTrue(r['all_literal_native_fixups_equal'])
        self.assertEqual(r['paired_exit_cleanup_fields_at'],[392,394,398,400])
        self.assertEqual((r['original_CRT_member_count'],r['source_module_count'],
                          r['original_untouched_member_programs']),(893,40,853))
        self.assertEqual(r['simultaneous_exact_original_source_CODE_bytes'],22170)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_original_MAP_equal'])
        self.assertEqual((r['real_decoded_Japanese_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_fopen_OMF_order_gap'])
        self.assertTrue(r['prior_fclose_frame_gap'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
