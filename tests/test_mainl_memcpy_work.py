"""Single-member native memcpy and complete Japanese MAINL link regression."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_memcpy_work import review
from build_th03_mainl_memcpy_work import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'private native memcpy proof absent')
class MemcpySourceReview(unittest.TestCase):
    def test_original_member_and_actual_product(self):
        r=review()
        self.assertEqual((r['original_member_CODE_bytes'],r['candidate_CODE_bytes'],r['literal_ordered_fields']),
                         (36,36,0))
        self.assertEqual((r['original_library_members'],r['context_members_unchanged'],r['original_member_index']),
                         (893,892,261))
        self.assertTrue(r['whole_decoded_EXE_equal'])
        self.assertTrue(r['whole_MAP_equal'])
        self.assertEqual(r['deterministic_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],r['original_cold_rebuilt']),
                         (False,0,False))
