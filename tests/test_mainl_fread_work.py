"""Whole original 437-byte DOS fread, real near core and linked Japanese MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_fread_work import REPORT
from review_th03_mainl_fread_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),
                     'native 28-source fread round pair unavailable')
class FreadCompleteNativeSource(unittest.TestCase):
    def test_complete_original_buffered_fread_and_joint_link(self):
        r=review()
        self.assertEqual((r['original_fread_CODE_bytes'],
                          r['source_fread_CODE_bytes']),(437,437))
        self.assertTrue(r['all_437_native_CODE_bytes_equal'])
        self.assertEqual((r['private_buffered_read_near_bytes'],
                          r['public_fread_far_bytes'],
                          r['public_fread_offset']),(283,154,283))
        self.assertEqual(r['private_return_pop_bytes'],10)
        self.assertEqual(r['literal_ordered_FIXUPP_count'],4)
        self.assertTrue(r['all_original_ordered_FIXUPPs_equal'])
        self.assertEqual(r['original_import_order'],
                         ['__fgetc','__rtl_read','N_LXMUL@','N_PADD@'])
        self.assertEqual((r['original_library_members'],r['reconstructed_source_members'],
                          r['untouched_original_member_programs']),(893,28,865))
        self.assertEqual(r['simultaneous_exact_source_CODE_bytes'],18702)
        self.assertTrue(r['whole_original_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['complete_Japanese_decoded_EXE_bytes'],r['MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
