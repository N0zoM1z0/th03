"""Large original signed long parser, two callbacks and twelve-source native linker."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strtol_work import REPORT
from review_th03_mainl_strtol_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'retained native signed parser pair absent')
class SignedLongParser(unittest.TestCase):
    def test_complete_original_native_signed_long_code_and_product(self):
        r=review()
        self.assertEqual((r['source_CODE_bytes'],r['original_CODE_bytes']),(290,290))
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertEqual((r['source_private_near_callbacks'],r['original_public_offset']),
                         (2,56))
        self.assertEqual(r['original_import_order'],
                         ['_errno','__ctype','__scantol'])
        self.assertEqual(r['original_literal_FIXUPPs'],7)
        self.assertTrue(r['ordered_native_FIXUPPs_equal'])
        self.assertEqual((r['original_library_members'],r['real_source_members'],
                          r['untouched_original_member_programs']),(893,12,881))
        self.assertEqual(r['cumulative_source_CODE_bytes'],13783)
        self.assertTrue(r['complete_Japanese_EXE_raw_equal'])
        self.assertTrue(r['complete_MAP_raw_equal'])
        self.assertEqual((r['Japanese_EXE_file_bytes'],r['MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['fully_repeated_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
