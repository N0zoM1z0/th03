"""Original far string and error output CRT sources plus native MAINL link."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_posttimecvt_work import PREFIX
from review_th03_mainl_posttimecvt_work import review

class NativeAfterTimeConversion(unittest.TestCase):
    def check(self,mode,n,total):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['all_ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_extdefs_publics_groups_equal'])
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_member_programs']),(893,n,893-n))
        self.assertEqual(r['cumulative_source_CODE_bytes'],total)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_timecvt_near_frame_gap_open'])
        self.assertTrue(r['prior_fopen_FIXUPP_order_open'])
        self.assertTrue(r['prior_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'strlwr-build.json')).is_file(),
                         'native strlwr pair absent')
    def test_strlwr(self):
        self.check('strlwr',49,25485)
        r=review('strlwr')
        q=r['actual_original_source_profiles']['strlwr']
        self.assertEqual(q['CODE_bytes'],38)
        self.assertEqual(q['public'],[[0,'_strlwr']])
        self.assertEqual(q['ordered_fields'],[])

    @unittest.skipUnless((ROOT/(PREFIX+'strlwr-strncat-build.json')).is_file(),
                         'native bounded concatenation pair absent')
    def test_strncat(self):
        self.check('strlwr-strncat',50,25590)
        q=review('strlwr-strncat')['actual_original_source_profiles']['strncat']
        self.assertEqual(q['CODE_bytes'],105)
        self.assertEqual(q['imports'],['_strlen','_movmem'])
        self.assertEqual([f['site'] for f in q['ordered_fields']],[71,31,15])

    @unittest.skipUnless((ROOT/(PREFIX+'strlwr-strncat-perror-build.json')).is_file(),
                         'native perror with original DATA pair absent')
    def test_perror_real_initialized_strings(self):
        self.check('strlwr-strncat-perror',51,25735)
        q=review('strlwr-strncat-perror')['actual_original_source_profiles']['perror']
        self.assertEqual(q['CODE_bytes'],145)
        self.assertEqual(q['DATA_bytes'],19)
        self.assertEqual(len(q['ordered_fields']),17)
        self.assertEqual(q['imports'],
                         ['__streams','_fputs','__sys_errlist','__sys_nerr','_errno'])
        self.assertEqual(review('strlwr-strncat-perror')['original_initialized_DATA_bytes'],19)
