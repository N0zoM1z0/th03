"""Byte-exact Borland unsigned long parser,private helpers and complete native MAINL."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strtoul_work import REPORT
from review_th03_mainl_strtoul_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'retained private 11-source pair unavailable')
class StrtoulSource(unittest.TestCase):
    def test_original_231_byte_scantol_wrapper_and_exact_link(self):
        r=review()
        self.assertEqual((r['CODE_original_bytes'],r['CODE_source_bytes']),(231,231))
        self.assertTrue(r['all231_CODE_bytes_equal'])
        self.assertEqual((r['private_near_helpers'],r['public_strtoul_offset']),(2,56))
        self.assertEqual(r['original_and_native_imports'],
                         ['_errno','__ctype','__scantol'])
        self.assertEqual(r['ordered_native_fields'],6)
        self.assertTrue(r['literal_fields_exact'])
        self.assertEqual((r['original_library_members'],r['source_members'],
                          r['untouched_original_member_programs']),(893,11,882))
        self.assertEqual(r['exact_joint_source_CODE_bytes'],13493)
        self.assertTrue(r['whole_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['MZ_relocations'],r['native_rounds']),(677,2))
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
