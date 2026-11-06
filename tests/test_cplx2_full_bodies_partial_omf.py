"""All 22 original complex FAR bodies plus CRT init, without fake OBJ credit."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_full_body_partial_omf import SOURCE,verify
class OriginalComplexAllBodies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_all_far_publics_and_complete_code_alignment(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,5598,5596))
        self.assertEqual((r['original_complete_FAR_function_bodies'],
                          r['original_member_publics_total']),(22,22))
        self.assertTrue(r['all_22_original_FAR_public_bodies_reconstructed'])
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],5588)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        source=SOURCE.read_bytes()
        self.assertEqual(source.count(b'public @$brsh$qm7istreamm7complex'),2)
        istream=source.split(b'@$brsh$qm7istreamm7complex proc far',1)[1].split(
            b'@$brsh$qm7istreamm7complex endp',1)[0]
        for statement in (b'call @istream@$brsh$qmc',
                          b'call @istream@$brsh$qmd',
                          b'call @istream@putback$qc',
                          b'call @ios@clear$qi',
                          b'call N_SCOPY@'):
            self.assertIn(statement,istream)
        self.assertIn(b'complex_zero_initializer proc far',source)
        self.assertIn(b'dw 2001h',source)
        self.assertIn(b'dd complex_zero_initializer',source)
    def test_original_data_initdata_all_symbolic_fixups(self):
        r=self.r
        self.assertEqual((r['original_OMF_fixups_total'],
                          r['native_OMF_fixups_total']),(860,858))
        self.assertEqual((r['original_fixup_count_in_prefix'],
                          r['exact_matching_original_fixups_site_target_addend']),
                         (859,857))
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],734)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),734)
        self.assertEqual(r['imported_near_target_frame5_vs_code_frame0_sites'],[5561])
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],47)
        self.assertEqual(r['original_DATA_implicit_unmaterialized_prefix_bytes'],16)
        self.assertEqual(r['original_INITDATA_bytes'],6)
        self.assertEqual((r['original_INITDATA_function_offset'],
                          r['native_INITDATA_function_offset']),(5575,5573))
        self.assertTrue(r['original_INITDATA_symbolic_target_equal_after_two_local_call_shifts'])
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_stable_native_rounds_and_no_unearned_full_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
