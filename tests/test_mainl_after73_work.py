"""Original native formatting engine source and whole Japanese MAINL product."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after73_work import PREFIX
from review_th03_mainl_after73_work import review

class OriginalNativeFormatter(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'vprinter-build.json')).is_file(),
                         'source-bound original vprinter native rounds not retained')
    def test_complete_original_1243_byte_vprinter_boss(self):
        r=review('vprinter')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,74,819))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1243,32007))
        self.assertEqual((r['profiles']['vprinter']['CODE_bytes'],
                          r['profiles']['vprinter']['DATA_bytes'],
                          r['profiles']['vprinter']['BSS_bytes']), (1243,103,0))
        self.assertEqual(r['profiles']['vprinter']['publics'], [(24,'__VPRINTER')])
        self.assertEqual(r['profiles']['vprinter']['imports'],
                         ['__LONGTOA','__REALCVT'])
        self.assertEqual(len(r['profiles']['vprinter']['relocation_sites_targets']),29)
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'vprinter-collate-build.json')).is_file(),
                         'complete 75-source collate proof unavailable')
    def test_original_six_entry_collate_engine(self):
        r=review('vprinter-collate')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(75,818,32442))
        self.assertEqual((r['profiles']['collate']['CODE_bytes'],
                          r['profiles']['collate']['DATA_bytes'],
                          r['profiles']['collate']['BSS_bytes']),(435,0,0))
        self.assertEqual(len(r['profiles']['collate']['publics']),6)
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])

    @unittest.skipUnless((ROOT/(PREFIX+'vprinter-collate-strxfrm-build.json')).is_file(),
                         'whole 76-source collation proof unavailable')
    def test_collate_strxfrm_two_members_all_native_fixups(self):
        r=review('vprinter-collate-strxfrm')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(76,817,32824))
        self.assertEqual((r['profiles']['_strxfrm']['CODE_bytes'],
                          r['profiles']['_strxfrm']['DATA_bytes']), (382,0))
        self.assertEqual(r['profiles']['_strxfrm']['publics'],
                         [(0,'__strxfrm'),(74,'_LevelTransform')])
        self.assertEqual(len(r['profiles']['_strxfrm']['relocation_sites_targets']),2)
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'vprinter-collate-strxfrm-locale-build.json')).is_file(),
                         'complete 77-source locale native carrier not retained')
    def test_locale_lifecycle_boss_and_exit_registration(self):
        r=review('vprinter-collate-strxfrm-locale')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(77,816,33774))
        self.assertEqual((r['profiles']['locale']['CODE_bytes'],
                          r['profiles']['locale']['DATA_bytes'],
                          r['profiles']['locale']['EXITDATA_bytes']), (950,22,6))
        self.assertEqual(r['profiles']['locale']['publics'],[
            (0,'___initialize_locale'),(181,'___uninitialize_locale'),
            (300,'___set_c_locale')])
        self.assertEqual(len(r['profiles']['locale']['relocation_sites_targets']),113)
        # Original BCC and native TASM differ in FIXUPP order, not their
        # literal fields once paired by raw segment and site.
        from build_th03_mainl_display_work import literal_fields
        from build_th03_mainl_after73_work import WORK
        orig=literal_fields((WORK/'vendor/locale.obj').read_bytes())
        cand=literal_fields((ROOT/'.analysis/work/after73-vprinter-collate-strxfrm-locale-round1-locale.obj').read_bytes())
        self.assertNotEqual(orig,cand)
        by=lambda f:(f['segment'],f['site'])
        self.assertEqual(sorted(orig,key=by),sorted(cand,key=by))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
