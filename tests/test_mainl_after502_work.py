"""Original low-level Borland DOS __rtl_read/__read two FAR APIs."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after502_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after502_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-rtl-read-two-far-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalLowLevelRead(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native low-level DOS read receipt absent')
    def test_entire_original_member_and_two_native_mainl_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,710,183))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(78,186653))
        self.assertEqual((r['profiles']['reada']['CODE_bytes'],
                          r['profiles']['reada']['DATA_bytes']),(78,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS read OMF absent')
    def test_real_int21h_and_literal_error_descriptor_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['reada']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),78)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(original,1),
                         [(0,'__rtl_read'),(50,'__read')])
        self.assertEqual(externs(original),['__IOERROR','__openfd'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual([(f['site'],f['location_type'],f['frame_method'],
                           f['frame'],f['target_method'],f['target'])
                          for f in sorted(F,key=lambda f:f['site'])],
                         [(12,1,1,1,2,2),(44,1,0,1,2,1)])
        self.assertEqual(bytes(P[1,i] for i in (35,36)),bytes.fromhex('cd21'))
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['reada']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(round['literal_omf_fixupp_equal_by_member']['reada'])
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
