"""Real 1256-byte strftime with 22 +22 genuine CODE table WORDs, 52-source MAINL."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strftime_work import REPORT
from review_th03_mainl_strftime_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native 52-source strftime round pair absent')
class OriginalStrftime(unittest.TestCase):
    def test_all_executable_CODE_tables_DATA_and_exact_product(self):
        r=review()
        self.assertEqual((r['original_strftime_CODE_bytes'],r['source_CODE_bytes']),
                         (1256,1256))
        self.assertEqual((r['original_initialized_DATA_bytes'],r['source_DATA_bytes']),
                         (18,18))
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['complete_initialized_DATA_equal'])
        self.assertEqual((r['real_executable_instruction_bytes'],
                          r['original_instruction_count']),(1168,448))
        self.assertEqual((r['original_CODE_data_table_bytes'],
                          r['original_format_class_words'],
                          r['original_switch_offset_words']),(88,22,22))
        self.assertEqual(r['literal_ordered_original_OMF_fields'],66)
        self.assertTrue(r['literal_ordered_sites_equal'])
        self.assertTrue(r['logical_native_fixups_equal'])
        self.assertTrue(r['literal_other_62_fields_equal'])
        self.assertFalse(r['native_original_OMF_equal'])
        self.assertEqual(r['original_UTOA_TARGET_frame_sites'],[879,811,774,723])
        self.assertEqual((r['original_near_call_frame_method'],
                          r['source_near_call_frame_method']),(5,0))
        self.assertEqual((r['original_CRT_program_count'],r['simultaneous_source_modules'],
                          r['unchanged_original_member_programs']),(893,52,841))
        self.assertEqual(r['cumulative_source_CODE_bytes'],26971)
        self.assertTrue(r['entire_original_Japanese_EXE_equal'])
        self.assertTrue(r['entire_original_MAP_equal'])
        self.assertEqual((r['original_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['repeated_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
