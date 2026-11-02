"""Exact native DOS strncat two strlen calls, movmem and complete native MAINL."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_strncat_work import review
from build_th03_mainl_strncat_work import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'private native 15-source build not available')
class StrncatSource(unittest.TestCase):
    def test_exact_strncat_and_fifteen_source_original_link(self):
        r=review()
        self.assertEqual((r['original_CODE_bytes'],r['source_CODE_bytes']),(105,105))
        self.assertTrue(r['complete_original_native_CODE_equal'])
        self.assertEqual(r['native_original_imports'],['_strlen','_movmem'])
        self.assertEqual(r['original_literal_FIXUPPs'],3)
        self.assertTrue(r['ordered_native_FIXUPPs_exact'])
        self.assertEqual((r['original_CRT_member_count'],r['source_members'],
                          r['unchanged_original_member_programs']),(893,15,878))
        self.assertEqual(r['combined_source_CODE_bytes'],14056)
        self.assertEqual((r['decoded_Japanese_EXE_bytes'],r['MZ_relocations']),(67372,677))
        self.assertTrue(r['entire_original_EXE_equal'])
        self.assertTrue(r['original_MAP_equal'])
        self.assertEqual(r['repeated_complete_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
