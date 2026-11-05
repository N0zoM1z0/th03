"""Original ios() constructor and complete Borland typed RTTI/vtable."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after485_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after485_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-default-constructor-rtti-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalIOSDefaultConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native ios() constructor proof missing')
    def test_full_original_source_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,693,200))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(135,184220))
        self.assertEqual((r['profiles']['stctr1']['CODE_bytes'],
                          r['profiles']['stctr1']['DATA_bytes']),(135,12))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original ios() OMF missing')
    def test_original_rtti_and_real_far_virtual_destructor(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['stctr1']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),147)
        self.assertEqual(len(F),6)
        self.assertEqual(code_publics(original,1),[(0,'@ios@$bctr$qv')])
        self.assertEqual(externs(original),[
            '@$bnew$qui','@__RefDestructorCount$qv','@ios@$bdtr$qv'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual(bytes(P[2,i] for i in range(12)),
                         bytes.fromhex('510000000000000000000000'))
        self.assertEqual(bytes(P[1,i] for i in range(119,123)),b'ios\0')
        refs={(f['segment'],f['site']):f for f in F}
        self.assertEqual((refs[1,39]['target_method'],refs[1,39]['target'],
                          refs[1,39]['addend']),(0,2,8))
        self.assertEqual((refs[2,0]['target_method'],refs[2,0]['target'],
                          refs[2,0]['addend']),(0,1,81))
        self.assertEqual((refs[2,8]['target_method'],refs[2,8]['target']),(2,3))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['stctr1']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
