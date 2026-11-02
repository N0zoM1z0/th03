"""Exact natural Borland C++ fscanf and whole original MAINL normal linker."""
import unittest,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_fscanf_work import REPORT
from review_th03_mainl_fscanf_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native 32-source fscanf vectors not retained')
class OriginalFscanf(unittest.TestCase):
    def test_natural_variadic_far_stack_wrapper_and_full_product(self):
        r=review()
        self.assertEqual((r['original_fscanf_CODE_bytes'],
                          r['source_fscanf_CODE_bytes']),(40,40))
        self.assertTrue(r['complete_native_CODE_raw_equal'])
        self.assertTrue(r['true_far_stack_varargs'])
        self.assertEqual(r['original_near_callback_imports'],
                         ['__Nfgetc','__Nungetc','__scanner'])
        self.assertEqual(r['original_literal_FIXUPPs'],3)
        self.assertTrue(r['all_ordered_fields_raw_equal'])
        self.assertEqual((r['original_CRT_member_count'],r['native_source_members'],
                          r['unchanged_original_member_programs']),(893,32,861))
        self.assertEqual(r['cumulative_source_CODE_bytes'],19872)
        self.assertTrue(r['full_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_decoded_Japanese_EXE_bytes'],
                          r['MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
