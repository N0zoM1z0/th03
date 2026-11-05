"""Source-bound original Borland srand/rand with persistent 32-bit seed."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after495_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after495_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='original-srand-rand-lcg-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalRand(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native srand/rand receipt absent')
    def test_complete_source_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,703,190))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(62,185749))
        self.assertEqual((r['profiles']['rand']['CODE_bytes'],
                          r['profiles']['rand']['DATA_bytes']),(62,4))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original rand member absent')
    def test_true_32bit_lcg_and_only_single_frame_difference(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['rand']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),66)
        self.assertEqual(code_publics(raw,1),[(0,'_srand'),(21,'_rand')])
        self.assertEqual(externs(raw),['N_LXMUL@'])
        self.assertEqual(bytes(P[2,i] for i in range(4)),b'\x01\x00\x00\x00')
        self.assertEqual(len(F),8)
        self.assertEqual(NEAR_FRAME_GAPS,{'rand':{38:1}})
        originals={f['site']:f for f in F}
        self.assertEqual(set(originals),{10,15,25,29,38,48,51,54})
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['rand']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            actual={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(actual),set(originals))
            for site,old in originals.items():
                now=actual[site]
                if site==38:
                    self.assertEqual((old['frame_method'],old['frame']),(5,None))
                    self.assertEqual((now['frame_method'],now['frame']),(0,1))
                    for key in set(old)-{'frame_method','frame'}:self.assertEqual(old[key],now[key])
                else:self.assertEqual(old,now)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
