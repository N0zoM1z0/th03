"""Exact original selected CRT fseek/ftell from semantic FILE layout source."""
from pathlib import Path
import unittest,sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_fseek_work import review
from build_th03_mainl_fseek_work import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'native 31-source fseek pair absent')
class OriginalFseek(unittest.TestCase):
    def test_real_original_selected_lib_and_standalone_difference(self):
        r=review()
        self.assertEqual((r['original_selected_CRT_CODE_bytes'],
                          r['source_CODE_bytes']),(492,492))
        self.assertTrue(r['all_native_CODE_bytes_equal'])
        self.assertEqual((r['private_near_buffer_calculator_bytes'],
                          r['far_fseek_bytes'],r['far_ftell_bytes']),(137,130,225))
        self.assertEqual(r['original_far_public_offsets'],[137,267])
        self.assertEqual(r['literal_selected_CRT_FIXUPPs'],6)
        self.assertTrue(r['selected_fields_raw_equal'])
        self.assertEqual(r['selected_member_fixup_sites'],[342,149,239,293,365,409])
        self.assertEqual(r['standalone_original_fixup_sites'],[409,365,342,293,239,149])
        self.assertTrue(r['logical_field_sets_equal_but_order_distinct'])
        self.assertEqual((r['original_library_members'],r['simultaneous_source_members'],
                          r['unchanged_original_member_programs']),(893,31,862))
        self.assertEqual(r['cumulative_source_CODE_bytes'],19832)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['real_Japanese_EXE_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
