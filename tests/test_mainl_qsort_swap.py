"""A real 46-byte near helper recovered from the larger original qsort boss."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_mainl_qsort_swap import REPORT
from review_th03_mainl_qsort_swap import review

@unittest.skipUnless((ROOT/REPORT).exists(),'native original qsort helper pair absent')
class QsortNearSwap(unittest.TestCase):
    def test_bounded_original_swap_not_fake_whole_qsort(self):
        r=review()
        self.assertEqual((r['original_boss_CODE_bytes'],
                          r['native_recovered_helper_CODE_bytes']),(756,46))
        self.assertTrue(r['native_helper_raw_equal'])
        self.assertEqual((r['original_helper_near_return_pop_bytes'],
                          r['original_qsort_BSS_bytes'],r['ordered_prefix_fixups']),
                         (8,6,1))
        self.assertTrue(r['prefix_FIXUPP_raw_equal'])
        self.assertEqual(r['verified_native_rounds'],2)
        self.assertFalse(r['complete_qsort'])
        self.assertFalse(r['whole_qsort_source_exact'])
        self.assertFalse(r['whole_qsort_linked'])
        self.assertEqual((r['source_acceptance'],
                          r['published_accepted_source_bytes_added']),(False,0))
