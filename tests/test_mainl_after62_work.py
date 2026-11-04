"""Regression coverage for original Japanese MAINL incremental CRT source."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after62_work import PREFIX
from review_th03_mainl_after62_work import review

class NativeAfter62(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'sprintf-build.json')).is_file(),
                         'original scoped sprintf native output not retained')
    def test_sprintf_vsprintf_complete_original_link(self):
        r=review('sprintf')
        self.assertTrue(r['complete'])
        self.assertEqual(r['native_source_members'],63)
        self.assertEqual(r['untouched_vendor_members'],830)
        self.assertEqual(r['added_CODE_bytes'],144)
        self.assertEqual(r['source_CRT_CODE_bytes'],28743)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertEqual(r['profiles']['sprintf']['publics'],
                         [[69,'_sprintf'],[107,'_vsprintf']])
        self.assertEqual(r['original_MZ_relocations'],677)
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'sprintf-io-build.json')).is_file(),
                         'source-equivalent medium CRT native link not retained')
    def test_three_original_sources_in_one_link(self):
        r=review('sprintf-io')
        self.assertEqual((r['native_source_members'],r['added_CODE_bytes'],
                          r['source_CRT_CODE_bytes']),(65,791,29390))
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual(r['profiles']['setvbuf']['DATA_bytes'],4)
        self.assertEqual(r['profiles']['write']['CODE_bytes'],358)
