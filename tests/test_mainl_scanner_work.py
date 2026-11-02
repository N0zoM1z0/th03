"""Original 1282-byte 8086 scanner, true format DATA and 23-source MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_scanner_work import REPORT
from review_th03_mainl_scanner_work import review

@unittest.skipUnless((ROOT/REPORT).exists(),
                     'original native 23-source scanner pair absent')
class ScannerWholeNative(unittest.TestCase):
    def test_1282_code_128_data_33_fields_and_joint_link(self):
        r=review()
        self.assertEqual((r['original_scanner_CODE_bytes'],
                          r['native_scanner_CODE_bytes']), (1282,1282))
        self.assertEqual((r['original_scanner_initialized_DATA_bytes'],
                          r['native_initialized_DATA_bytes']),(128,128))
        self.assertTrue(r['literal_native_CODE_equal'])
        self.assertTrue(r['literal_native_DATA_equal'])
        self.assertEqual(r['ordered_original_OMF_FIXUPPs'],33)
        self.assertTrue(r['literal_FIXUPPs_equal'])
        self.assertTrue(r['semantic_ASCII_classifications_exact'])
        self.assertEqual((r['original_8086_instruction_count'],
                          r['symbolic_switch_table_words'],
                          r['original_switch_table_offset']),(523,22,1238))
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_CRT_programs']),(893,23,870))
        self.assertEqual(r['cumulative_source_CODE_bytes'],17768)
        self.assertEqual(r['newly_recovered_initialized_DATA_bytes'],128)
        self.assertTrue(r['entire_original_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_original_MAP_raw_equal'])
        self.assertEqual((r['whole_EXE_file_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']), (False,0,False))
