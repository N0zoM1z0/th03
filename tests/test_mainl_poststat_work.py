"""Exact native FILE input and DOS status wrappers in normal source MAINL."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_poststat_work import PREFIX
from review_th03_mainl_poststat_work import review

class PostStatOriginalCRT(unittest.TestCase):
    def check(self,mode,count,total):
        r=review(mode)
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['all_ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_extdefs_publics_groups_equal'])
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_member_programs']),
                         (893,count,893-count))
        self.assertEqual(r['cumulative_source_CODE_bytes'],total)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_fopen_FIXUPP_order_open'])
        self.assertTrue(r['prior_fclose_near_frame_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'fgets-build.json')).is_file(),
                         'original native fgets pair absent')
    def test_far_buffer_fgets(self):
        self.check('fgets',37,21429)
        entry=review('fgets')['actual_original_source_profiles']['fgets']
        self.assertEqual(entry['CODE_bytes'],154)
        self.assertEqual(entry['pub'],[[0,'_fgets']])
        self.assertEqual(entry['externs'],['__fgetc'])
        self.assertEqual(len(entry['ordered_fields']),1)
        self.assertEqual(entry['ordered_fields'][0]['site'],79)

    @unittest.skipUnless((ROOT/(PREFIX+'fgets-gets-build.json')).is_file(),
                         'original native stdin gets pair absent')
    def test_global_stdin_gets(self):
        self.check('fgets-gets',38,21564)
        entry=review('fgets-gets')['actual_original_source_profiles']['gets']
        self.assertEqual(entry['CODE_bytes'],135)
        self.assertEqual(entry['externs'],['__streams','__fgetc'])
        self.assertEqual(len(entry['ordered_fields']),6)

    @unittest.skipUnless((ROOT/(PREFIX+'fgets-gets-fstat-build.json')).is_file(),
                         'original native fstat pair absent')
    def test_DOS_device_flags_fstat(self):
        self.check('fgets-gets-fstat',39,21711)
        entry=review('fgets-gets-fstat')['actual_original_source_profiles']['fstat']
        self.assertEqual(entry['CODE_bytes'],147)
        self.assertEqual(len(entry['ordered_fields']),4)
