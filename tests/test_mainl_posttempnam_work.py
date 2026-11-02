"""True DOS chdir/unlink and natural BCC tmpnam/ftime in Japanese MAINL."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_posttempnam_work import PREFIX
from review_th03_mainl_posttempnam_work import review

class OriginalDOSLeafCRT(unittest.TestCase):
    def check(self,mode,count,total):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['all_ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_extdefs_publics_groups_equal'])
        self.assertEqual((r['original_CRT_members'],r['native_source_modules'],
                          r['untouched_original_member_programs']),
                         (893,count,893-count))
        self.assertEqual(r['cumulative_source_CODE_bytes'],total)
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['entire_MAP_raw_equal'])
        self.assertEqual((r['original_EXE_file_bytes'],
                          r['original_MZ_relocations']),(67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['prior_strftime_near_frame_gap_open'])
        self.assertTrue(r['prior_tempnam_near_frame_gap_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'dirs-build.json')).is_file(),
                         'native chdir/unlink pair absent')
    def test_real_dos_chdir_and_unlink(self):
        self.check('dirs',55,27422)
        r=review('dirs')
        self.assertEqual(set(r['actual_original_source_profiles']),
                         {'chdir','unlink'})
        for n in ('chdir','unlink'):
            q=r['actual_original_source_profiles'][n]
            self.assertEqual(q['CODE_bytes'],28)
            self.assertEqual(q['imports'],['__IOERROR'])
            self.assertEqual([f['site'] for f in q['ordered_fields']],[22])

    @unittest.skipUnless((ROOT/(PREFIX+'dirs-tmpnam-build.json')).is_file(),
                         'natural BCC tmpnam pair absent')
    def test_natural_Pascal_tmpnam(self):
        self.check('dirs-tmpnam',56,27445)
        q=review('dirs-tmpnam')['actual_original_source_profiles']['tmpnam']
        self.assertEqual(q['CODE_bytes'],23)
        self.assertEqual(q['imports'],['__TMPNAM','__tmpnum'])
        self.assertEqual([f['site'] for f in q['ordered_fields']],[17,13])
        self.assertEqual(q['ordered_fields'][0]['frame_method'],5)

    @unittest.skipUnless((ROOT/(PREFIX+'dirs-tmpnam-ftime-build.json')).is_file(),
                         'natural far BCC ftime pair absent')
    def test_natural_far_ftime(self):
        self.check('dirs-tmpnam-ftime',57,27467)
        q=review('dirs-tmpnam-ftime')['actual_original_source_profiles']['ftime']
        self.assertEqual(q['CODE_bytes'],22)
        self.assertEqual(q['imports'],['__ftime'])
        self.assertEqual([f['site'] for f in q['ordered_fields']],[12])
