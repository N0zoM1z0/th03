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
