"""DOS text-stream CTRL-Z trim/append and original ordered FAR lseek."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after481_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after481_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-text-stream-ctrlz-helpers-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosControlZ(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native ctrl-z proof missing')
    def test_native_source_scope_two_full_original_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,689,204))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(189,183539))
        self.assertEqual((r['profiles']['zapctlz']['CODE_bytes'],
                          r['profiles']['zapctlz']['DATA_bytes']),(189,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS text ctrl-z OMF absent')
    def test_two_near_private_helpers_and_literal_far_lseek(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['zapctlz']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),189)
        self.assertEqual(len(F),1)
        self.assertEqual(code_publics(raw,1),
                         [(64,'__TRIMCTLZ'),(136,'__APPENDCTLZ')])
        self.assertEqual(externs(raw),['_lseek'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual((F[0]['site'],F[0]['location_type'],
                          F[0]['target_method'],F[0]['target'],F[0]['frame_method']),
                         (123,3,2,1,5))
        self.assertEqual((P[1,16],P[1,17]),(0xcd,0x21))
        self.assertEqual((P[1,50],P[1,51]),(0xcd,0x21))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['zapctlz']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(literal_fields(obj),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['zapctlz'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
