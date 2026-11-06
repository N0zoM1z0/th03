"""Original DOS create/newcreate FAR pair with original DOSERROR ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after513_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after513_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-create-newcreate-two-far-apis'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosCreate(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS create receipt absent')
    def test_two_full_original_native_link_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,721,172))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(100,187986))
        self.assertEqual((r['profiles']['doscreat']['CODE_bytes'],
                          r['profiles']['doscreat']['DATA_bytes']),(100,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS creator OMF missing')
    def test_native_core_two_far_apis_and_doserror_fixup(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['doscreat']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),100)
        self.assertEqual(code_publics(orig,1),
                         [(40,'__dos_creat'),(70,'__dos_creatnew')])
        self.assertEqual(externs(orig),['__DOSERROR'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(len(F),1)
        self.assertEqual((F[0]['site'],F[0]['location_type'],F[0]['width'],
                          F[0]['segment_relative'],F[0]['frame_method'],
                          F[0]['target_method'],F[0]['target']),
                         (32,1,2,False,0,2,1))
        self.assertEqual(bytes(P[1,i] for i in (15,16)),bytes.fromhex('cd21'))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['doscreat']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['doscreat'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
