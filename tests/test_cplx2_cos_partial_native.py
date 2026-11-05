"""Eight original complex FAR bodies, semantic cos and exact symbolic OMF."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_cos_partial import SOURCE,verify
class OriginalComplexCosPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_eight_full_far_math_bodies_and_original_cos(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,2124,2122))
        self.assertEqual(r['original_complete_FAR_function_bodies'],8)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],2114)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        cos=SOURCE.read_bytes().split(b'public @cos$qm7complex',1)[1].split(
            b'@cos$qm7complex endp',1)[0]
        for operation in (b'call _exp',b'call _sin',b'call _cos',
                          b'fstp tbyte ptr',b'fld tbyte ptr',
                          b'call @$bnew$qui'):
            self.assertIn(operation,cos)
    def test_all_337_original_symbolic_fields_except_two_local_calls(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],337)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],335)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],295)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),295)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],12)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_and_no_false_ownership(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
