"""Original FAR setjmp/longjmp exception-aware CPU register image."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after458_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after458_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='exception-aware-setjmp-longjmp-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
PUBLICS=[(0,'_setjmp'),(71,'_longjmp')]

class OriginalSetjmpLongjmp(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native setjmp/longjmp receipt absent')
    def test_complete_original_code_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,666,227))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (214,178811))
        self.assertEqual((r['profiles']['setjmp']['CODE_bytes'],
                          r['profiles']['setjmp']['DATA_bytes']),(214,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original setjmp OMF unavailable')
    def test_real_context_image_flags_and_unwind_targets(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['setjmp']['index']]
        self.assertEqual(m.name,'setjmp')
        orig=original_library_member(m)
        P=payload(orig); F=literal_fields(orig)
        self.assertEqual(len(P),214)
        self.assertEqual(len(F),4)
        self.assertEqual(code_publics(orig,1),PUBLICS)
        self.assertEqual(externs(orig),['__Local_unwind','__CurrExcContext',
                                       '__Global_unwind'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {55:(2,2),134:(2,3),157:(2,2),184:(2,1)})
        self.assertEqual((P[1,5],P[1,0x62],P[1,0xd1]),(0x9c,0xfa,0xcf))
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['setjmp']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertEqual(code_publics(made,1),PUBLICS)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['setjmp'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
