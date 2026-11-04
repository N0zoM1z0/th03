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
