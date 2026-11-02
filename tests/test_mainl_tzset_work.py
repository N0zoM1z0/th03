"""Full original Borland DOS TZ/JST/DST native CODE DATA BSS INIT and linker."""
import unittest,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_tzset_work import REPORT
from review_th03_mainl_tzset_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'real native 58-source tzset pair absent')
class NativeOriginalTimezone(unittest.TestCase):
    def test_complete_original_four_segment_timezone_source_and_japanese_link(self):
        r=review()
        self.assertEqual((r['new_tzset_CODE_bytes'],r['new_tzset_DATA_bytes'],
                          r['new_tzset_BSS_bytes'],r['new_tzset_INITDATA_bytes']),
                         (744,48,8,6))
        self.assertTrue(r['full_original_CODE_raw_equal'])
        self.assertTrue(r['full_original_DATA_raw_equal'])
        self.assertTrue(r['full_original_INITDATA_raw_equal'])
        self.assertEqual(r['original_function_sizes'],[508,236])
        self.assertEqual(r['original_OMF_fixups'],48)
        self.assertTrue(r['complete_literal_ordered_FIXUPPs_equal'])
        self.assertEqual((r['CODE_fixup_count'],r['DATA_fixup_count'],
                          r['INITDATA_fixup_count']),(45,2,1))
        self.assertEqual((r['original_893_CRT_members'],
                          r['simultaneous_source_CRT_members'],
                          r['unchanged_original_vendor_programs']),(893,58,835))
        self.assertEqual(r['cumulative_exact_source_CODE_bytes'],28211)
        self.assertTrue(r['whole_original_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_original_MAP_raw_equal'])
        self.assertEqual((r['original_Japanese_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['independent_native_rounds'],2)
        self.assertTrue(r['predecessor_timecvt_OMF_gap_open'])
        self.assertTrue(r['predecessor_strftime_OMF_gap_open'])
        self.assertTrue(r['predecessor_tempnam_OMF_gap_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
