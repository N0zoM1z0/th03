"""Whole 916-byte DOS high-address qsort and eighteen native MAINL sources."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_hqsort_work import REPORT
from review_th03_mainl_hqsort_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private original high-sort native pair absent')
class HighAddressSort(unittest.TestCase):
    def test_complete_high_sort_original_code_fields_and_exe(self):
        r=review()
        self.assertEqual((r['original_highsort_CODE_bytes'],
                          r['source_highsort_CODE_bytes']),(916,916))
        self.assertTrue(r['original_native_CODE_equal'])
        self.assertEqual((r['original_near_swap_bytes'],
                          r['original_highsort_recursive_core_bytes'],
                          r['original_far_public_bytes']),(46,826,44))
        self.assertEqual(r['original_far_public_offset'],872)
        self.assertEqual(r['literal_ordered_fixups'],52)
        self.assertTrue(r['all52_native_FIXUPPs_equal'])
        self.assertEqual((r['original_BSS_bytes'],r['source_BSS_bytes']),(6,6))
        self.assertEqual(r['external_original_imports'],
                         ['N_PADD@','N_LXMUL@','N_PADA@','N_PCMP@',
                          'N_PSBA@','N_PSUB@','N_PSBP@','N_LDIV@'])
        self.assertEqual((r['original_CRT_members'],r['original_source_members'],
                          r['untouched_original_member_programs']),(893,18,875))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],15786)
        self.assertEqual((r['original_Japanese_decoded_EXE_file_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertTrue(r['whole_original_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
