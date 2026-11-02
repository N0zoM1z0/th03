"""Native original quicksort BSS size helper, not a fake complete qsort."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_qsort_swap import review
from probe_th03_mainl_qsort_swap import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'original native qsort helper output absent')
class QsortSwap(unittest.TestCase):
    def test_exact_near_swap_and_original_field(self):
        r=review()
        self.assertEqual((r['original_qsort_CODE_bytes'],r['original_qsort_FIXUPPs']),
                         (756,29))
        self.assertEqual((r['exactly_recovered_swap_CODE_bytes'],
                          r['exact_swap_BSS_fixup_site'],r['original_BSS_bytes']),
                         (46,9,6))
        self.assertTrue(r['native_source_swap_exact'])
        self.assertTrue(r['native_swap_FIXUPP_equal'])
        self.assertEqual(r['separate_native_rounds'],2)
        self.assertTrue(r['only_bounded_swap_claimed'])
        self.assertEqual((r['complete_qsort'],r['source_acceptance'],
                          r['accepted_source_bytes'],r['original_cold_rebuilt']),
                         (False,False,0,False))
