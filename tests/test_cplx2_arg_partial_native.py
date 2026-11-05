"""Five cplx2 complex functions, exact arg body and two known local call gaps."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_arg_partial import SOURCE,verify
class OriginalComplexArgPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.proof=verify()
    def test_five_complete_far_bodies_and_original_arg_math(self):
        p=self.proof
        self.assertEqual((p['full_member_original_CODE_bytes'],
                          p['recovered_original_prefix_CODE_bytes'],
                          p['native_source_CODE_bytes']),(5598,1217,1215))
        self.assertEqual(p['original_complete_FAR_function_bodies'],5)
        self.assertEqual(p['equal_CODE_bytes_outside_two_local_FAR_calls'],1209)
        self.assertEqual(p['omitted_symbolic_local_FAR_calls'],[800,985])
        self.assertIn(b'@arg$qm7complex proc far',SOURCE.read_bytes())
        self.assertIn(b'call _atan2',SOURCE.read_bytes())
        self.assertIn(b'complex_arg_zero_real label qword',SOURCE.read_bytes())
    def test_all_original_arg_fixups_except_two_known_calls(self):
        p=self.proof
        self.assertEqual(p['original_fixup_count_in_prefix'],184)
        self.assertEqual(p['exact_matching_original_fixups_site_target_addend'],182)
        self.assertEqual(p['original_location_frame4_native_target_frame5_count'],163)
        self.assertEqual(len(set(p['original_location_frame4_sites'])),163)
        self.assertEqual(p['original_genuine_DATA_bytes_equal'],12)
        self.assertFalse(p['original_Borland_complete_FIXUPP_equality'])
    def test_two_real_native_rounds_and_zero_unearned_credit(self):
        p=self.proof
        self.assertEqual(p['native_TASM_rounds'],2)
        self.assertTrue(p['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(p['native_COMENT_clock_record_indices']),
                         not p['raw_native_obj_sha_equal'])
        self.assertFalse(p['complete_original_member_source'])
        self.assertEqual(p['source_linked_original_CRT_members_added'],0)
        self.assertFalse(p['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
