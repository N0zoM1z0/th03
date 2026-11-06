"""Original signed Borland 32-bit ldiv quotient/rem restoring-division core."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after512_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after512_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='signed-32bit-quotient-remainder-far-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalSignedLongDivision(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native ldivt receipt absent')
    def test_two_full_original_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,720,173))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(152,187886))
        self.assertEqual((r['profiles']['ldivt']['CODE_bytes'],
                          r['profiles']['ldivt']['DATA_bytes']),(152,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original 32bit divide OMF absent')
    def test_real_restoring_division_and_literal_near_memcopy(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['ldivt']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),152)
        self.assertEqual(code_publics(original,1),[(0,'_ldiv')])
        self.assertEqual(externs(original),['N_SCOPY@'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual(len(F),1)
        self.assertEqual((F[0]['site'],F[0]['location_type'],F[0]['width'],
                          F[0]['segment_relative'],F[0]['frame_method'],
                          F[0]['target_method'],F[0]['target']),
                         (138,1,2,False,0,2,1))
        self.assertEqual(bytes(P[1,i] for i in (59,60)),bytes.fromhex('87f2'))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['ldivt']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['ldivt'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
