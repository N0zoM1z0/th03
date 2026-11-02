"""Whole DOS directory subsystem 517 CODE/9 DATA, 45-source normal MAINL."""
from pathlib import Path
import unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_direct_work import REPORT
from review_th03_mainl_direct_work import review

@unittest.skipUnless((ROOT/REPORT).exists(),'original DOS directory native pair absent')
class DirectoryOriginal(unittest.TestCase):
    def test_four_real_original_directory_functions(self):
        r=review()
        self.assertEqual((r['original_CODE_bytes'],r['native_CODE_bytes']),(517,517))
        self.assertTrue(r['complete_original_CODE_equal'])
        self.assertEqual((r['original_initialized_DATA_bytes'],
                          r['native_DATA_bytes']),(9,9))
        self.assertTrue(r['literal_initialized_DATA_equal'])
        self.assertEqual(r['original_function_sizes'],[311,56,75,75])
        self.assertEqual(r['original_native_ordered_FIXUPPs'],20)
        self.assertTrue(r['literal_original_fixups_equal'])
        self.assertEqual([x[1] for x in r['original_far_pubs']],
                         ['_opendir','_rewinddir','_readdir','_closedir'])
        self.assertEqual((r['original_893_member_library'],r['source_CRT_members'],
                          r['original_vendor_member_programs_unchanged']),(893,45,848))
        self.assertEqual(r['cumulative_source_CODE_bytes'],22803)
        self.assertTrue(r['whole_original_japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['previous_fopen_OMF_order_open'])
        self.assertTrue(r['previous_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
