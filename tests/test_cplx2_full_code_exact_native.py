"""Full original cplx2 CODE with NOSMART direct FAR calls and 860 native fixups."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_full_code_exact_native import SOURCE,verify
class OriginalComplexFullCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_all_5598_original_code_bytes_and_22_public_functions(self):
        r=self.r
        self.assertTrue(r['original_CODE_bytes_equal'])
        self.assertEqual((r['original_CODE_bytes'],r['native_CODE_bytes']),(5598,5598))
        self.assertEqual(r['original_publics_count'],22)
        self.assertTrue(r['all_original_22_FAR_bodies_reconstructed'])
        self.assertEqual(r['same_CODE_direct_FAR_CALLs_recovered'],[800,985])
        source=SOURCE.read_bytes()
        acos=source.split(b'public @acos$qm7complex',1)[1].split(
            b'@acos$qm7complex endp',1)[0]
        self.assertEqual(acos.count(b'NOSMART'),2)
        self.assertEqual(acos.count(b'SMART'),4) # NOSMART contains SMART substring
        self.assertEqual(acos.count(b'call @arg$qm7complex'),2)
    def test_exact_data_init_and_all_860_symbolic_references(self):
        r=self.r
        self.assertTrue(r['original_GROUPDEF_equal'])
        self.assertEqual((r['original_DATA_bytes'],r['original_DATA_implicit_prefix_bytes'],
                          r['original_initialized_DATA_bytes_equal']),(63,16,47))
        self.assertTrue(r['original_INITDATA_bytes_equal'])
        self.assertEqual(r['original_INITDATA_bytes'],6)
        self.assertEqual(r['original_init_routine_CODE_offset'],5575)
        self.assertEqual(r['original_OMF_fixups_total'],860)
        self.assertEqual(r['native_OMF_fixups_total'],860)
        self.assertEqual(r['exact_matching_symbolic_fixup_sites_targets_addends'],860)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],734)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),734)
        self.assertEqual(r['imported_near_target_frame5_vs_code_frame0_sites'],[5561])
        self.assertEqual(r['original_unused_extdef_retained_in_native'],['__turboFloat'])
        self.assertFalse(r['complete_original_raw_FIXUPP_frames_equal'])
    def test_tasm_twice_but_not_pretend_link_acceptance(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['original_raw_Borland_OBJ_equal'])
        self.assertFalse(r['complete_native_MAINL_link_accepted'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
