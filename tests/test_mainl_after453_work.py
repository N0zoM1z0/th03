"""Original filebuf::close including virtual flush and DOS release."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after453_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after453_work import review
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='filebuf-close-flush-and-descriptor'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFilebufClose(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native close receipt missing')
    def test_both_complete_original_source_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,661,232))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (174,177672))
        self.assertEqual((r['profiles']['fsbclose']['CODE_bytes'],
                          r['profiles']['fsbclose']['DATA_bytes']),(174,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS close OMF missing')
    def test_original_virtual_overflow_call_and_literal_far_close(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsbclose']['index']]
        self.assertEqual(m.name,'fsbclose')
        orig=original_library_member(m)
        P=payload(orig); F=literal_fields(orig)
        self.assertEqual(len(P),174)
        self.assertEqual(len(F),1)
        self.assertEqual(code_publics(orig,1),[(0,'@filebuf@close$qv')])
        self.assertEqual(externs(orig),['_close'])
        self.assertEqual((F[0]['segment'],F[0]['site'],F[0]['target_method'],F[0]['target']),
                         (1,125,2,1))
        self.assertEqual(bytes(P[1,i] for i in (96,97,98)),bytes.fromhex('ff5f18'))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fsbclose']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fsbclose'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
