"""Original cplx2 native membership and two byte-exact full MAINL rounds."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after514_work import PREFIX,WORK,NATIVE,retained,original_library_member,scope
from review_th03_mainl_after514_work import review
from probe_th03_cplx2_full_code_exact_native import compare as audit
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='cplx2-all-original-functions-and-initdata'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFullComplexRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.exists():raise unittest.SkipTest('full cplx2 receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['cplx2']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_22_publics_exact_code_data_and_initdata(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,722,171))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(5598,193584))
        self.assertEqual((r['profiles']['cplx2']['CODE_bytes'],
                          r['profiles']['cplx2']['DATA_bytes'],
                          r['profiles']['cplx2']['INITDATA_bytes']),(5598,63,6))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertEqual(len(code_publics(self.original,1)),22)
        self.assertEqual(len(externs(self.original)),24)
        self.assertEqual((ROOT/'src/mainl/crt/cplx2.asm').read_bytes(),
                         (ROOT/'src/mainl/crt/cplx2_complete_code_native.asm').read_bytes())
    def test_original_native_exe_map_and_mz_equality_twice(self):
        r=self.r
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        for row in self.receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(exe),67372)
            self.assertEqual(len(parse_mz(exe).relocations),677)
            obj=(ROOT/row['outputs']['cplx2']['path']).read_bytes()
            self.assertEqual(scope('cplx2',obj),scope('cplx2',self.original))
            self.assertEqual([rec.data.hex() for rec in parse_omf(obj)
                              if rec.name=='GRPDEF'],['0aff02ff03'])
            self.assertEqual(len(code_publics(obj,1)),22)
            self.assertEqual(len(externs(obj)),24)
            self.assertEqual(row['library_comparison']['contextual_members_unchanged'],171)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['cplx2'])
            self.assertFalse(row['original_program_equal_by_member']['cplx2'])
            proof=audit(self.original,obj)
            self.assertTrue(proof['original_CODE_bytes_equal'])
            self.assertEqual(proof['exact_matching_symbolic_fixup_sites_targets_addends'],860)
            self.assertEqual(proof['original_location_frame4_native_target_frame5_count'],734)
            self.assertEqual(proof['imported_near_target_frame5_vs_code_frame0_sites'],[5561])
            self.assertEqual(proof['same_CODE_direct_FAR_CALLs_recovered'],[800,985])
    def test_raw_borland_records_not_claimed_identical(self):
        r=self.r
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
if __name__=='__main__':unittest.main()
