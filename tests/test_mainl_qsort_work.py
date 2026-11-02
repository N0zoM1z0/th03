"""The entire 756-byte original Borland qsort boss and original Japanese MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_qsort_work import REPORT
from review_th03_mainl_qsort_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private complete qsort source link absent')
class QsortWholeNativeSource(unittest.TestCase):
    def test_full_original_recursive_sort_and_normal_link(self):
        r=review()
        self.assertEqual((r['original_qsort_CODE_bytes'],r['source_qsort_CODE_bytes']),
                         (756,756))
        self.assertTrue(r['all_native_qsort_CODE_bytes_equal'])
        self.assertEqual((r['qsort_private_near_swap_bytes'],
                          r['qsort_recursive_sort_core_bytes'],
                          r['qsort_far_public_bytes']),(46,666,44))
        self.assertEqual(r['original_far_public_offset'],712)
        self.assertEqual(r['original_sorted_ordered_fields'],29)
        self.assertTrue(r['all29_literal_native_FIXUPPs_equal'])
        self.assertEqual(r['original_and_native_BSS_bytes'],[6,6])
        self.assertEqual(r['original_import_order'],['N_LXMUL@','N_LDIV@'])
        self.assertEqual((r['original_CRT_members'],r['exact_source_CRT_members'],
                          r['untouched_original_program_records']),(893,17,876))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],14870)
        self.assertEqual((r['complete_decoded_Japanese_EXE_bytes'],
                          r['original_MZ_relocation_entries']),(67372,677))
        self.assertTrue(r['actual_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual(r['complete_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
