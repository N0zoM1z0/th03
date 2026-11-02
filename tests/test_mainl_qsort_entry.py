"""Do not conflate exact original qsort swap/front-end with recursive sorter."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_qsort_entry import review
from probe_th03_mainl_qsort_entry import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'private qsort partial source pair absent')
class QsortFrontEnd(unittest.TestCase):
    def test_real_near_helper_and_far_wrapper_with_symbolic_core_edge(self):
        r=review()
        self.assertEqual((r['original_qsort_CODE_bytes'],r['original_qsort_native_fields'],
                          r['original_live_BSS_bytes']), (756,29,6))
        self.assertEqual((r['helper_literal_CODE_bytes'],r['public_wrapper_CODE_bytes'],
                          r['wrapper_literal_equal_bytes']), (46,44,42))
        self.assertEqual((r['symbolic_original_near_CALL_bytes'],
                          r['original_core_not_reconstructed_bytes']), (2,666))
        self.assertEqual(r['native_BSS_fixup_count_recovered'],4)
        self.assertEqual(r['original_fixup_sites'],[9,721,735,738])
        self.assertEqual(r['original_near_call_target'],46)
        self.assertTrue(r['two_actual_TASM_rounds_equal'])
        self.assertTrue(r['only_bounded_codegen_claimed'])
        self.assertEqual((r['complete_qsort'],r['source_acceptance'],
                          r['added_accepted_bytes'],r['original_cold_rebuilt']),
                         (False,False,0,False))
