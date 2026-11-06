"""Original istream::do_get buffered-byte and FAR underflow callback ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after503_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after503_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='istream-virtual-underflow-do-get-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalIstreamDoGet(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native do_get receipt absent')
    def test_entire_original_member_and_two_native_mainl_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,711,182))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(158,186811))
        self.assertEqual((r['profiles']['istdget']['CODE_bytes'],
                          r['profiles']['istdget']['DATA_bytes']),(158,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original streambuf OMF absent')
    def test_true_vtable_underflow_and_literal_far_setstate(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['istdget']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),158)
        self.assertEqual(code_publics(original,1),[(0,'@istream@do_get$qv')])
        self.assertEqual(externs(original),['@ios@setstate$qi'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual(len(F),1)
        self.assertEqual((F[0]['site'],F[0]['location_type'],F[0]['width'],
                          F[0]['frame_method'],F[0]['target_method'],F[0]['target']),
                         (133,3,4,5,2,1))
        self.assertEqual(bytes(P[1,i] for i in (68,69,70)),
                         bytes.fromhex('ff5f0c'))
        r=json.loads(RECEIPT.read_text())
        for round in r['rounds']:
            made=(ROOT/round['outputs']['istdget']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(round['literal_omf_fixupp_equal_by_member']['istdget'])
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
