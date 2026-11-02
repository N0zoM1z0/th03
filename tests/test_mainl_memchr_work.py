"""Four real DOS CRT source providers and complete Japanese MAINL native link."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_memchr_combo_work import REPORT
from review_th03_mainl_memchr_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private source CRT pair absent')
class MemchrSource(unittest.TestCase):
    def test_complete_native_memchr_and_four_source_carrier(self):
        r=review()
        self.assertEqual(r['original_and_candidate_memchr_CODE_bytes'],[37,37])
        self.assertEqual(r['native_memchr_ordered_fixups'],[0,0])
        self.assertEqual(r['original_memchr_OMF_GROUP'],'08ff03ff02')
        self.assertEqual(r['source_member_indices'],[259,260,261,292])
        self.assertEqual(r['replaced_members'],['memchr','memcmp','memcpy','strcmp'])
        self.assertEqual((r['original_library_members'],r['unchanged_original_member_programs']),
                         (893,889))
        self.assertEqual((r['decoded_EXE_bytes'],r['MZ_relocations']),(67372,677))
        self.assertTrue(r['whole_decoded_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual(r['deterministic_complete_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
