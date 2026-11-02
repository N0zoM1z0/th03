"""Whole native strcmp source, three-source library and Japanese MAINL link."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strcmp_combo_work import REPORT
from review_th03_mainl_strcmp_work import review

@unittest.skipUnless((ROOT/REPORT).exists(),'private three-source native pair absent')
class StrcmpSource(unittest.TestCase):
    def test_complete_source_and_exact_carrier(self):
        r=review()
        self.assertEqual(r['original_and_candidate_strcmp_CODE_bytes'],[48,48])
        self.assertEqual(r['native_strcmp_ordered_fixups'],[0,0])
        self.assertEqual(r['original_strcmp_OMF_GROUP'],'08ff03ff02')
        self.assertEqual(r['source_member_indices'],[260,261,292])
        self.assertEqual(r['replaced_members'],['memcmp','memcpy','strcmp'])
        self.assertEqual((r['original_library_members'],r['unchanged_original_member_programs']),
                         (893,890))
        self.assertEqual((r['decoded_EXE_bytes'],r['MZ_relocations']),(67372,677))
        self.assertTrue(r['whole_decoded_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual(r['deterministic_complete_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
