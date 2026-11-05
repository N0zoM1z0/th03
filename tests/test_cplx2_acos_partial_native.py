"""Native partial-proof: three division functions plus complex acos semantics."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_acos_partial import SOURCE,verify
class OriginalComplexAcosPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=verify()
    def test_complete_original_acos_body_with_two_known_far_call_gaps(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,1079,1077))
        self.assertEqual(r['original_complete_FAR_function_bodies'],4)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],1069)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        self.assertEqual(r['original_member_publics_total'],22)
        self.assertIn(b'@acos$qm7complex proc far',SOURCE.read_bytes())
        self.assertIn(b'complex_negative_two',SOURCE.read_bytes())
        self.assertIn(b'complex_two_float',SOURCE.read_bytes())
    def test_exact_remaining_159_fixup_targets_and_genuine_typed_data(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],161)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],159)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],143)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),143)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],12)
        self.assertEqual(r['original_DATA_implicit_unmaterialized_prefix_bytes'],16)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_rounds_but_not_complete_crt_member(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertTrue(set(r['native_COMENT_clock_record_indices']) <= {2})
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
