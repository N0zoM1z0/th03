"""Original 556-byte fopen product link; its OMF FIXUPP order remains open."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_fopen_work import REPORT
from review_th03_mainl_fopen_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'fopen native pair absent')
class FopenSourceProduct(unittest.TestCase):
    def test_original_four_routines_and_open_FIXUPP_order(self):
        r=review()
        self.assertTrue(r['complete'])
        self.assertEqual(r['original_fopen_CODE_bytes'],556)
        self.assertTrue(r['full_native_CODE_raw_equal'])
        self.assertEqual((r['original_near_mode_parser_bytes'],
                          r['original_near_OPENFP_bytes'],r['original_near_GETFP_bytes'],
                          r['original_far_fopen_bytes']),(212,210,77,57))
        self.assertEqual(r['real_original_pubdef_offsets'],[212,422,499])
        self.assertEqual(r['original_FIXUPP_count'],12)
        self.assertTrue(r['logical_FIXUPP_set_raw_equal'])
        self.assertFalse(r['complete_native_OMF_equal'])
        self.assertFalse(r['ordered_FIXUPPs_raw_equal'])
        self.assertEqual(r['original_fixup_sites'],
                         [464,461,436,387,369,318,274,184,182,178,176,156])
        self.assertEqual((r['original_CRT_members'],r['actual_source_members'],
                          r['untouched_original_member_programs']),(893,33,860))
        self.assertEqual(r['cumulative_source_CODE_bytes'],20428)
        self.assertTrue(r['entire_original_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_original_MAP_raw_equal'])
        self.assertEqual((r['real_japanese_decoded_EXE_file_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes']),
                         (False,0))
