"""Original fstreambase setbuf virtual dispatch and ios success/failure paths."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after520_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after520_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='fstreambase-virtual-setbuf-ios-state'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalFstreamSetbuf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.exists():raise unittest.SkipTest('native fstream setbuf receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['fssbuf']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_complete_source_two_original_mainl_links(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,728,165))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(91,194292))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_real_virtual_filebuf_and_both_native_ios_calls(self):
        P=payload(self.original);F=literal_fields(self.original)
        self.assertEqual(len(P),91)
        self.assertEqual(code_publics(self.original,1),
                         [(0,'@fstreambase@setbuf$qnci')])
        self.assertEqual(externs(self.original),
                         ['@ios@clear$qi','@ios@setstate$qi'])
        self.assertEqual({f['site']:(f['target_method'],f['target'])
                          for f in F},{60:(2,1),78:(2,2)})
        source=(ROOT/'src/mainl/crt/fssbuf.asm').read_bytes()
        for x in (b'call dword ptr [bx+4]',b'call @ios@clear$qi',
                  b'call @ios@setstate$qi',b'or ax,dx'):
            self.assertIn(x,source)
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        for row in self.receipt['rounds']:
            obj=(ROOT/row['outputs']['fssbuf']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(obj)),expected)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['fssbuf'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
