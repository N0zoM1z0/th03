"""Original istream double bounds, x87 EMUL and full linked MAINL parity."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after517_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after517_work import review
from probe_th03_mainl_large_fixups import original_literal_fixups
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='istream-double-bounds-x87-wrapper'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalIstreamDouble(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.is_file():raise unittest.SkipTest('original double stream receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['istedbl']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_complete_source_and_two_native_mainl_rounds(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,725,168))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(124,193939))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_original_long_double_input_and_all_18_symbolic_fields(self):
        P=payload(self.original);F=original_literal_fixups(self.original)
        self.assertEqual(len(P),124)
        self.assertEqual(code_publics(self.original,1),[(0,'@istream@$brsh$qmd')])
        self.assertEqual(len(F),18)
        self.assertEqual(len([f for f in F if f['frame_method']==4]),14)
        source=(ROOT/'src/mainl/crt/istedbl.asm').read_bytes()
        for term in (b'EMUL',b'call @istream@$brsh$qmg',
                     b'fld qword ptr DGROUP:__huge_dble',
                     b'fld tbyte ptr [bp-0ah]',b'fcompp',
                     b'fstsw word ptr [bp-0ch]',b'fwait',
                     b'mov word ptr DGROUP:_errno,22h',
                     b'fstp qword ptr es:[bx]'):
            self.assertIn(term,source)
        orig_names=externs(self.original)
        for row in self.receipt['rounds']:
            obj=(ROOT/row['outputs']['istedbl']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            made=literal_fields(obj)
            self.assertEqual(len(made),18)
            names=externs(obj)
            for f,g in zip(sorted(F,key=lambda f:f['site']),
                           sorted(made,key=lambda f:f['site'])):
                self.assertEqual((f['site'],f['location_type'],f['width'],
                                  f['segment_relative'],f['addend']),
                                 (g['site'],g['location_type'],g['width'],
                                  g['segment_relative'],g['addend']))
                self.assertEqual(orig_names[f['target']-1],names[g['target']-1])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
