"""Verified original 666-byte qsort recursive structure is not source acceptance."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_qsort_core import review

class OriginalCoreBlueprint(unittest.TestCase):
    def test_actual_recursive_core_calls_and_original_omf(self):
        r=review()
        self.assertEqual((r['original_qsort_CODE_bytes'],r['private_swap_CODE_bytes'],
                          r['recursive_core_CODE_bytes'],r['far_public_CODE_bytes']),
                         (756,46,666,44))
        self.assertEqual((r['recursive_core_instruction_count'],
                          r['original_Omf_fixup_count'],r['recursive_core_fixup_count']),
                         (242,29,25))
        self.assertEqual(len(r['near_swap_call_sites']),6)
        self.assertEqual(r['recursive_call_sites'],[0x299,0x2ae])
        self.assertEqual([x['site'] for x in r['math_call_sites']],
                         [0x85,0xa0,0x264,0x287])
        self.assertEqual(len(r['far_comparator_call_sites']),7)
        self.assertEqual(r['branch_count'],30)
        self.assertEqual(len(r['original_core_branch_targets']),30)
        self.assertFalse(r['original_source_core_recovered'])
        self.assertEqual((r['complete_qsort'],r['source_acceptance'],
                          r['accepted_source_bytes'],r['original_cold_rebuilt']),
                         (False,False,0,False))
