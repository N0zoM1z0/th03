"""Entire DOS fclose CODE, original near frame difference and product link."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_fclose_work import REPORT
from review_th03_mainl_fclose_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native fclose pair absent')
class OriginalFclose(unittest.TestCase):
    def test_complete_192_code_and_one_open_native_frame(self):
        r=review()
        self.assertEqual(r['new_fclose_CODE_bytes'],192)
        self.assertTrue(r['all_native_CODE_bytes_equal'])
        self.assertEqual(r['original_public'],'_fclose')
        self.assertEqual(r['original_literal_fixup_count'],5)
        self.assertEqual(r['original_field_sites'],[168,163,112,89,60])
        self.assertTrue(r['literal_logical_fields_equal'])
        self.assertFalse(r['native_original_OMF_equal'])
        self.assertEqual((r['original_MKNAME_frame_method'],
                          r['source_MKNAME_frame_method']),(5,0))
        self.assertTrue(r['parent_fopen_original_OMF_order_still_open'])
        self.assertEqual((r['original_CRT_members'],r['source_modules_in_working_library'],
                          r['untouched_original_CRT_programs']),(893,35,858))
        self.assertEqual(r['cumulative_source_CODE_bytes'],20719)
        self.assertTrue(r['whole_decoded_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['independent_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes']),
                         (False,0))
