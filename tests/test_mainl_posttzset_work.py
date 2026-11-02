"""Exact original far comparator array search and native DOS getenv source CRT."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_posttzset_work import PREFIX
from review_th03_mainl_posttzset_work import review

class OriginalNativePostTZ(unittest.TestCase):
    def check(self,mode,count,code):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['all_ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_extdefs_publics_groups_equal'])
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_member_programs']),
                         (893,count,893-count))
        self.assertEqual(r['cumulative_source_CODE_bytes'],code)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['parent_tzset_full_literal_OMF_equal'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'lsearch-build.json')).is_file(),
                         'native lsearch original link not retained')
    def test_original_real_202_byte_lsearch_lfind(self):
        self.check('lsearch',59,28413)
        q=review('lsearch')['actual_original_source_profiles']['lsearch']
        self.assertEqual(q['CODE_bytes'],202)
        self.assertEqual(q['public'],[[117,'_lsearch'],[160,'_lfind']])
        self.assertEqual(q['imports'],['_movmem'])
        self.assertEqual([f['site'] for f in q['ordered_fields']],[84])
        self.assertEqual(q['ordered_fields'][0]['frame_method'],5)

    @unittest.skipUnless((ROOT/(PREFIX+'lsearch-getenv-build.json')).is_file(),
                         'native environment source original link not retained')
    def test_getenv_real_far_environment_vector(self):
        self.check('lsearch-getenv',60,28525)
        q=review('lsearch-getenv')['actual_original_source_profiles']['getenv']
        self.assertEqual(q['CODE_bytes'],112)
        self.assertEqual(q['public'],[[0,'_getenv']])
        self.assertEqual(q['imports'],['__environ'])
        self.assertEqual([f['site'] for f in q['ordered_fields']],[35])
        self.assertEqual(q['ordered_fields'][0]['frame_method'],5)
