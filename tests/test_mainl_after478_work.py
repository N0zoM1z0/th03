"""Original IBM PIT delay calibration, INITDATA and exact native OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after478_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after478_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ibm-pit-delay-initdata-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalIBMDelayCalibration(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'IBM PIT delay proof absent')
    def test_complete_native_original_and_two_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,686,207))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(188,183034))
        self.assertEqual((r['profiles']['cibmdely']['CODE_bytes'],
                          r['profiles']['cibmdely']['DATA_bytes'],
                          r['profiles']['cibmdely']['INITDATA_bytes']),(188,4,6))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original PIT OMF unavailable')
    def test_calibration_counter_and_symbolic_fourth_segment(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['cibmdely']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),198)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(original,1),[(91,'___ibm_delay')])
        self.assertEqual(externs(original),['___conio_type','N_LXMUL@'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['0aff03ff02'])
        self.assertEqual(bytes(P[2,i] for i in range(4)),bytes.fromhex('52090000'))
        self.assertEqual(bytes(P[4,i] for i in range(6)),bytes.fromhex('011023000000'))
        fields={f['site']:f for f in F if f['segment']==1}
        self.assertEqual(set(fields),{45,64,70,116,119,122})
        self.assertEqual((fields[45]['target_method'],fields[45]['target']),(2,1))
        self.assertEqual((fields[122]['target_method'],fields[122]['target'],
                          fields[122]['frame_method'],fields[122]['frame']),
                         (2,2,0,1))
        init=[f for f in F if f['segment']==4]
        self.assertEqual(len(init),1)
        self.assertEqual((init[0]['site'],init[0]['location_type'],
                          init[0]['target_method'],init[0]['target'],
                          init[0]['addend']),(2,3,0,1,35))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['cibmdely']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['cibmdely'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':
    unittest.main()
