"""67-source original Japanese MAINL CRT error-format module, native-only scope."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after66_work import PREFIX
from review_th03_mainl_after66_work import review

class NativeAfter66(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strerror-build.json')).is_file(),
                         'source-bound original strerror native rounds absent')
    def test_complete_error_format_source_and_full_link(self):
        r=review('strerror')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,67,826))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (176,30391))
        self.assertEqual((r['profiles']['strerror']['CODE_bytes'],
                          r['profiles']['strerror']['DATA_bytes'],
                          r['profiles']['strerror']['BSS_bytes']),(176,26,161))
        self.assertEqual(r['profiles']['strerror']['publics'],
                         [(135,'__strerror'),(157,'_strerror')])
        self.assertEqual(len(r['profiles']['strerror']['relocation_sites_targets']),12)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
