"""Full original cplx2 5598-byte source-link and 860 symbolic OMF audit."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after514_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after514_work import review
from probe_th03_cplx2_full_code_exact_native import compare as scoped_proof
from build_th03_mainl_display_work import payload
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='cplx2-all-original-functions-and-initdata'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFullComplexModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reviewed=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['cplx2']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_full_original_crt_member_two_complete_native_mainl_links(self):
        r=self.reviewed
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,722,171))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(5598,193584))
        self.assertEqual((r['profiles']['cplx2']['CODE_bytes'],
                          r['profiles']['cplx2']['DATA_bytes'],
                          r['profiles']['cplx2']['INITDATA_bytes']),(5598,63,6))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_all_22_original_exports_24_imports_and_860_fields(self):
        r=self.receipt
        orig=self.original
        for row in r['rounds']:
            made=(ROOT/row['outputs']['cplx2']['path']).read_bytes()
            p=scoped_proof(orig,made)
            self.assertTrue(p['original_CODE_bytes_equal'])
            self.assertEqual((p['original_OMF_fixups_total'],
                              p['native_OMF_fixups_total']),(860,860))
            self.assertEqual(p['exact_matching_symbolic_fixup_sites_targets_addends'],860)
            self.assertEqual(p['original_location_frame4_native_target_frame5_count'],734)
            self.assertEqual(p['imported_near_target_frame5_vs_code_frame0_sites'],[5561])
            self.assertEqual(p['same_CODE_direct_FAR_CALLs_recovered'],[800,985])
            self.assertEqual(len(code_publics(made,1)),22)
            self.assertEqual(len(externs(made)),24)
            self.assertEqual([rec.data.hex() for rec in parse_omf(made)
                              if rec.name=='GRPDEF'],['0aff02ff03'])
            self.assertTrue(row['library_comparison']['contextual_members_unchanged']==171)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['cplx2'])
            self.assertFalse(row['original_program_equal_by_member']['cplx2'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
