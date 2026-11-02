"""Full original 974 CODE/1 DATA/1 BSS putc and 46-source DOS MAINL link."""
from pathlib import Path
import unittest,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_putc_work import REPORT
from review_th03_mainl_putc_work import review

@unittest.skipUnless((ROOT/REPORT).exists(),'private full native putc source pair not available')
class OriginalPutsWriter(unittest.TestCase):
    def test_original_974_byte_buffered_output_and_OMF(self):
        r=review()
        self.assertEqual((r['original_putc_CODE_bytes'],r['native_CODE_bytes']),(974,974))
        self.assertTrue(r['exact_literal_CODE_equal'])
        self.assertEqual((r['original_DATA_bytes'],r['native_DATA_bytes'],
                          r['original_BSS_bytes'],r['native_BSS_bytes']),(1,1,1,1))
        self.assertTrue(r['initialized_DATA_raw_equal'])
        self.assertEqual(r['original_public_function_sizes'],[32,395,24,523])
        self.assertEqual(r['original_literal_FIXUPPs'],29)
        self.assertTrue(r['all29_ordered_fields_equal'])
        self.assertEqual(r['original_internal_far_call_frame_method'],5)
        self.assertTrue(r['restored_TARGET_frame_at_CODE_21'])
        self.assertEqual((r['original_library_members'],r['source_modules'],
                          r['unchanged_vendor_member_programs']),(893,46,847))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],23777)
        self.assertTrue(r['whole_original_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_equal'])
        self.assertEqual((r['original_Japanese_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['repeated_native_rounds'],2)
        self.assertTrue(r['previous_fopen_OMF_gap_open'])
        self.assertTrue(r['previous_fclose_near_frame_gap_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
