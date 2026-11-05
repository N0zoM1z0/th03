"""Original Borland rand/srand seed and 32-bit LCG multiplication ABI."""
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
class OriginalRandLCG(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native original rand receipt unavailable')
    def test_full_original_source_and_two_native_mainl_rounds(self):
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
    @unittest.skipUnless(RECEIPT.is_file(),'original rand OMF absent')
    def test_real_data_seed_and_only_one_imported_near_frame_gap(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['rand']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),66)
        self.assertEqual(len(F),8)
        self.assertEqual(code_publics(original,1),[(0,'_srand'),(21,'_rand')])
        self.assertEqual(externs(original),['N_LXMUL@'])
        self.assertEqual(bytes(P[2,i] for i in range(4)),b'\x01\0\0\0')
        self.assertEqual(NEAR_FRAME_GAPS,{'rand':{38:1}})
        originals={f['site']:f for f in F}
        self.assertEqual(set(originals),{10,15,25,29,38,48,51,54})
        self.assertEqual((originals[38]['target_method'],originals[38]['target']),
                         (2,1))
        self.assertTrue(all(f['target_method']==0 and f['target']==2
                            for site,f in originals.items() if site!=38))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['rand']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            fields={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(fields),set(originals))
            for site,old in originals.items():
                new=fields[site]
                if site==38:
                    self.assertEqual((old['frame_method'],old['frame']),(5,None))
                    self.assertEqual((new['frame_method'],new['frame']),(0,1))
                    keys=set(old)-{'frame_method','frame'}
                    self.assertEqual({k:old[k] for k in keys},{k:new[k] for k in keys})
                else:self.assertEqual(old,new)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
