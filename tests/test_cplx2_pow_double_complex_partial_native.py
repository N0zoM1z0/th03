"""Fourteen original complex FAR bodies, including signed-base scalar^complex."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_pow_double_complex_partial import SOURCE,verify
class OriginalScalarPowerComplexPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_fourteenth_complete_complex_power_and_typed_pi(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,3532,3530))
        self.assertEqual(r['original_complete_FAR_function_bodies'],14)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],3522)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        body=SOURCE.read_bytes().split(b'public @pow$qdm7complex',1)[1].split(
            b'@pow$qdm7complex endp',1)[0]
        for piece in (b'call _fabs',b'call _log',
                      b'call @$bmul$qm7complext1',
                      b'call near ptr @exp$qm7complex',
                      b'jmp near ptr pow_scalar_return',
                      b'fld qword ptr DGROUP:complex_pi'):
            self.assertIn(piece,body)
        self.assertNotIn(b'fstp qword ptr [bp-0ah]\n    fwait\n    fld qword ptr [bp+0ah]',body)
        self.assertIn(b'dq 3.141592653589793115997963468544185161590576171875',
                      SOURCE.read_bytes())
    def test_original_omf_and_real_typed_data(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],546)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],544)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],473)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),473)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],28)
        self.assertEqual(r['original_DATA_implicit_unmaterialized_prefix_bytes'],16)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_rounds_and_zero_complete_source_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
