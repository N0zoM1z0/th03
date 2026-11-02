"""Natural BCC4.5 far fputs, real near Pascal FPUTN and 51-source MAINL."""
from pathlib import Path
import unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_fputs_work import REPORT
from review_th03_mainl_fputs_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native fputs 51-source BCC pair absent')
class NaturalFputs(unittest.TestCase):
    def test_original_Pascal_near_FPUTN_and_85_code(self):
        r=review()
        self.assertEqual((r['original_fputs_CODE_bytes'],
                          r['source_fputs_CODE_bytes']),(85,85))
        self.assertTrue(r['all_native_CODE_raw_equal'])
        self.assertEqual(r['original_EXTDEF_order'],['__FPUTN','_strlen'])
        self.assertEqual(r['literal_ordered_FIXUPPs_count'],2)
        self.assertTrue(r['all_native_FIXUPPs_equal'])
        self.assertEqual((r['original_near_pascal_FPUTN_frame_method'],
                          r['original_far_strlen_frame_method']),(5,5))
        self.assertTrue(r['full_original_OMF_equal'])
        self.assertEqual((r['original_893_CRT_members'],r['native_source_members'],
                          r['original_untouched_vendor_programs']),(893,51,842))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],25715)
        self.assertTrue(r['complete_Japanese_EXE_raw_equal'])
        self.assertTrue(r['original_MAP_raw_equal'])
        self.assertEqual((r['original_Japanese_EXE_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_timecvt_near_frame_open'])
        self.assertTrue(r['prior_fopen_FIXUPP_order_open'])
        self.assertTrue(r['prior_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
