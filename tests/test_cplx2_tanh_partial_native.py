"""Twenty original complex FAR math bodies, complete native x87 tanh and OMF."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_tanh_partial import SOURCE,verify
class OriginalComplexTanhPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_twentieth_tanh_and_x87_denominator(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,5091,5089))
        self.assertEqual(r['original_complete_FAR_function_bodies'],20)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],5081)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        s=SOURCE.read_bytes()
        self.assertEqual(s.count(b'public @tanh$qm7complex'),2)
        b=s.split(b'@tanh$qm7complex proc far',1)[1].split(
            b'@tanh$qm7complex endp',1)[0]
        for op in (b'call _sin',b'call _cos',b'call _exp',
                   b'fstp tbyte ptr [bp-3eh]',
                   b'fld tbyte ptr [bp-3eh]',
                   b'fst qword ptr [bp-5ah]',
                   b'fst qword ptr [bp-62h]',
                   b'fld dword ptr DGROUP:complex_tan_factor',
                   b'call @$bnew$qui'):
            self.assertIn(op,b)
    def test_original_809_fixups_and_real_typed_data(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],809)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],807)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],703)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),703)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],40)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_and_correct_credit_boundary(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
