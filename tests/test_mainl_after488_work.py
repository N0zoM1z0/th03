"""Original DOS intdos/intdosx, native register image and original OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after488_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after488_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-intdos-intdosx-register-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalIntDos(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native intdos receipt missing')
    def test_complete_original_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,696,197))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(146,184690))
        self.assertEqual((r['profiles']['intdos']['CODE_bytes'],
                          r['profiles']['intdos']['DATA_bytes']),(146,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS intdos OMF absent')
    def test_two_far_publics_real_dos_and_literal_fixupps(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['intdos']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),146)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(raw,1),[(0,'_intdos'),(50,'_intdosx')])
        self.assertEqual(externs(raw),['_segread','__IOERROR'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual([(f['site'],f['location_type'],f['target_method'],
                           f['target'],f['frame_method']) for f in sorted(F,key=lambda x:x['site'])],
                         [(14,3,2,1,5),(139,1,2,2,0)])
        self.assertEqual((P[1,87],P[1,88],P[1,90],P[1,91]),(0xcd,0x21,0x9c,0x9c))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['intdos']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['intdos'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
