"""Fifteen complete complex FAR bodies: original complex^complex power."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_pow_complex_complex_partial import SOURCE,verify
class OriginalComplexPowerOverload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_all_15_bodies_and_new_209_byte_complex_power(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,3741,3739))
        self.assertEqual(r['original_complete_FAR_function_bodies'],15)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],3731)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        body=SOURCE.read_bytes().split(b'public @pow$qm7complext1',1)[1].split(
            b'@pow$qm7complext1 endp',1)[0]
        for inst in (b'fcompp',b'call near ptr @log$qm7complex',
                     b'call @$bmul$qm7complext1',
                     b'call near ptr @exp$qm7complex',
                     b'pow_cc_general:',b'pow_cc_return:'):
            self.assertIn(inst,body)
    def test_original_574_omf_fixups_and_typed_data(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],574)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],572)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],496)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),496)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],28)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_native_two_rounds_without_false_crt_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
