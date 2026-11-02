"""Complete native DOS xx + seven CRT sources in one original MAINL carrier."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_xx_crt_combo_work import REPORT
from review_th03_mainl_xx_crt_combo_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private eight-source native link absent')
class NativeSourceIntegration(unittest.TestCase):
    def test_eight_exact_native_members_with_real_original_exe_and_map(self):
        r=review()
        self.assertEqual((r['source_member_count'],r['original_library_member_count'],
                          r['unchanged_original_member_programs']), (8,893,885))
        self.assertEqual((r['original_native_xx_CODE_bytes'],
                          r['native_xx_ordered_fields']),(12622,187))
        self.assertTrue(r['native_xx_full_CODE_equal'])
        self.assertTrue(r['all_original_CRT_native_members_equal'])
        self.assertEqual((r['original_native_CRT_CODE_bytes'],
                          r['combined_native_source_CODE_bytes']),(329,12951))
        self.assertEqual((r['original_decoded_EXE_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertTrue(r['whole_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual(r['repeated_native_link_rounds'],2)
        self.assertTrue(r['source_builds_independently_repeated'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
