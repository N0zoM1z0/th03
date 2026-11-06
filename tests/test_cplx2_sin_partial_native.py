"""Sixteen original FAR cplx2 functions with native sine and 614 OMF fields."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_sin_partial import SOURCE,verify
class OriginalComplexSinPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_all_sixteen_publics_and_byte_exact_sin(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,3974,3972))
        self.assertEqual(r['original_complete_FAR_function_bodies'],16)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],3964)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        src=SOURCE.read_bytes()
        self.assertEqual(src.count(b'public @sin$qm7complex'),2)
        body=src.split(b'@sin$qm7complex proc far',1)[1].split(
            b'@sin$qm7complex endp',1)[0]
        self.assertLess(body.index(b'call _cos'),body.index(b'call _sin'))
        self.assertEqual(body.count(b'fmul qword ptr DGROUP:complex_negative_half'),1)
        self.assertIn(b'complex_negative_half label qword',src)
        self.assertIn(b'dq -0.5',src)
    def test_original_614_fixups_and_true_typed_negative_half(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],614)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],612)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],530)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),530)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],36)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_rounds_without_unearned_original_crt_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
