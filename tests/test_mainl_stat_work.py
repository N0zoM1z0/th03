"""Entire 556 CODE+4 DATA original DOS stat and complete source CRT product."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_stat_work import REPORT
from review_th03_mainl_stat_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native original stat pair not retained')
class NativeStat(unittest.TestCase):
    def test_complete_original_stat_and_original_Japanese_link(self):
        r=review()
        self.assertEqual((r['original_stat_CODE_bytes'],
                          r['exact_original_stat_CODE_bytes']),(556,556))
        self.assertEqual((r['original_stat_DATA_bytes'],
                          r['exact_original_DATA_bytes']),(4,4))
        self.assertTrue(r['raw_CODE_equal'])
        self.assertTrue(r['raw_initialized_DATA_equal'])
        self.assertEqual((r['original_near_helper_bytes'],r['original_public_stat_bytes']),
                         (132,424))
        self.assertEqual(r['original_far_stat_public_offset'],132)
        self.assertEqual(r['literal_ordered_original_OMF_FIXUPPs'],9)
        self.assertTrue(r['literal_fields_raw_equal'])
        self.assertEqual((r['original_CRT_member_count'],r['source_members_in_link'],
                          r['other_original_member_programs_unchanged']),(893,36,857))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],21275)
        self.assertEqual(r['new_original_DATA_bytes'],4)
        self.assertTrue(r['full_japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_japanese_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_fopen_OMF_order_open'])
        self.assertTrue(r['prior_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
