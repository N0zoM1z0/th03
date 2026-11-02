"""Full 820-byte DOS/Unix converter, 12 DATA, 48-source original MAINL."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_timecvt_work import REPORT
from review_th03_mainl_timecvt_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'source-only time converter normal link absent')
class OriginalTimeConversion(unittest.TestCase):
    def test_full_DOS_unix_CODE_DATA_and_tracked_near_OMF_gap(self):
        r=review()
        self.assertEqual((r['original_CODE_bytes'],r['source_CODE_bytes']),(820,820))
        self.assertEqual((r['original_initialized_DATA_bytes'],
                          r['source_DATA_bytes']),(12,12))
        self.assertTrue(r['complete_native_CODE_raw_equal'])
        self.assertTrue(r['complete_native_DATA_raw_equal'])
        self.assertEqual(r['original_function_sizes'],[301,519])
        self.assertEqual(r['original_far_public_offsets'],[0,301])
        self.assertEqual(r['literal_native_ordered_FIXUPP_count'],29)
        self.assertTrue(r['logical_ordered_FIXUPPs_equal'])
        self.assertFalse(r['complete_original_OMF_equal'])
        self.assertEqual(r['original_near_TARGET_to_source_CODE_frame_count'],18)
        self.assertEqual((r['original_near_frame'],r['source_near_frame']),(5,0))
        self.assertEqual((r['original_893_library_members'],
                          r['source_members_in_working_CRT'],
                          r['unchanged_original_member_programs']),(893,48,845))
        self.assertEqual(r['combined_exact_source_CODE_bytes'],25447)
        self.assertTrue(r['whole_original_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_exe_bytes'],r['original_mz_relocations']),
                         (67372,677))
        self.assertEqual(r['repeated_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
