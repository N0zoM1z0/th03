"""Original DOS small file/string CRT sources with full Japanese MAINL normal link."""
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_postopen_work import PREFIX
from review_th03_mainl_postopen_work import review

class NativeSmallCrt(unittest.TestCase):
    def check(self,mode,source_count,code_bytes):
        r=review(mode)
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['all_ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_extdefs_publics_groups_equal'])
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_member_programs']),
                         (893,source_count,893-source_count))
        self.assertEqual(r['cumulative_source_CODE_bytes'],code_bytes)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_fopen_FIXUPP_order_open'])
        self.assertTrue(r['prior_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'clearerr-build.json')).is_file(),
                         'clearerr 41-native-source pair not present')
    def test_clearerr(self):
        self.check('clearerr',41,22187)

    @unittest.skipUnless((ROOT/(PREFIX+'clearerr-rewind-build.json')).is_file(),
                         'clearerr/rewind 42-native-source pair not present')
    def test_rewind_and_clearerr(self):
        self.check('clearerr-rewind',42,22227)
        r=review('clearerr-rewind')
        self.assertEqual(r['actual_original_source_profiles']['clearerr']['CODE_bytes'],17)
        self.assertEqual(r['actual_original_source_profiles']['rewind']['CODE_bytes'],40)
        self.assertEqual([q['site'] for q in
            r['actual_original_source_profiles']['rewind']['ordered_fields']],[17])

    @unittest.skipUnless((ROOT/(PREFIX+'clearerr-rewind-remove-build.json')).is_file(),
                         'native DOS remove source pair not present')
    def test_remove(self):
        self.check('clearerr-rewind-remove',43,22255)

    @unittest.skipUnless((ROOT/(PREFIX+'clearerr-rewind-remove-rename-build.json')).is_file(),
                         'native DOS rename source pair not present')
    def test_rename(self):
        self.check('clearerr-rewind-remove-rename',44,22286)
        r=review('clearerr-rewind-remove-rename')
        self.assertEqual(r['actual_original_source_profiles']['rename']['CODE_bytes'],31)
        self.assertEqual(r['actual_original_source_profiles']['remove']['CODE_bytes'],28)
