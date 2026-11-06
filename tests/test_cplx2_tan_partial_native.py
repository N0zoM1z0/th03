"""Nineteen original complex functions including complete x87 complex tangent."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_tan_partial import SOURCE,verify
class OriginalComplexTanPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_nineteenth_tan_and_exact_complex_denominator(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,4781,4779))
        self.assertEqual(r['original_complete_FAR_function_bodies'],19)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],4771)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        s=SOURCE.read_bytes()
        self.assertEqual(s.count(b'public @tan$qm7complex'),2)
        tan=s.split(b'@tan$qm7complex proc far',1)[1].split(
            b'@tan$qm7complex endp',1)[0]
        for op in (b'call _sin',b'call _cos',b'call _exp',
                   b'fstp tbyte ptr',b'fld tbyte ptr',
                   b'fst qword ptr [bp-6ch]',b'fst qword ptr [bp-74h]',
                   b'fld dword ptr DGROUP:complex_tan_factor',
                   b'fdiv qword ptr [bp-3ch]',b'call @$bnew$qui'):
            self.assertIn(op,tan)
        self.assertIn(b'dd 4.0',s)
    def test_original_750_fixups_and_new_typed_float(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],750)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],748)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],649)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),649)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],40)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_tasm_rounds_without_complete_crt_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
