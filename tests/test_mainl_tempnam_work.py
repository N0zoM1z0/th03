"""Original tempnam DOS path generation, actual CODE/DATA and full EXE."""
from pathlib import Path
import unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_tempnam_work import REPORT
from review_th03_mainl_tempnam_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native tempnam pair absent')
class TempnamOriginal(unittest.TestCase):
    def test_full_395_code_6_data_and_one_MKNAME_frame_gap(self):
        r=review()
        self.assertEqual((r['original_CODE_bytes'],r['source_CODE_bytes']),(395,395))
        self.assertEqual((r['original_initialized_DATA_bytes'],r['source_DATA_bytes']),(6,6))
        self.assertTrue(r['native_CODE_raw_equal'])
        self.assertTrue(r['native_DATA_raw_equal'])
        self.assertEqual(r['ordered_original_FIXUPP_fields'],14)
        self.assertTrue(r['logical_fields_equal'])
        self.assertFalse(r['original_native_OMF_equal'])
        self.assertEqual((r['only_native_frame_gap_at'],
                          r['original_near_frame'],r['source_near_frame']),(309,5,0))
        self.assertEqual((r['original_893_member_CRT'],r['simultaneous_source_members'],
                          r['untouched_original_member_programs']),(893,53,840))
        self.assertEqual(r['cumulative_original_source_CODE_bytes'],27366)
        self.assertTrue(r['whole_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
