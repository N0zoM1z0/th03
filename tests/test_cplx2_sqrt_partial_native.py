"""Eighteen original complex FAR bodies, x87 complex sqrt and exact OMF fields."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_sqrt_partial import SOURCE,verify
class OriginalComplexSqrtPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_eighteen_far_bodies_including_original_sqrt(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,4429,4427))
        self.assertEqual(r['original_complete_FAR_function_bodies'],18)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],4419)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        src=SOURCE.read_bytes()
        self.assertEqual(src.count(b'public @sqrt$qm7complex'),2)
        body=src.split(b'@sqrt$qm7complex proc far',1)[1].split(
            b'@sqrt$qm7complex endp',1)[0]
        for op in (b'call near ptr @arg$qm7complex',
                   b'fdiv dword ptr DGROUP:complex_two_float',
                   b'call @abs$qm7complex',b'call _sqrt',
                   b'call _sin',b'call _cos',
                   b'call @$bnew$qui'):
            self.assertIn(op,body)
    def test_original_683_fixups_and_x87_frame_semantics_disclosed(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],683)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],681)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],587)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),587)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],36)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_rounds_but_no_complete_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
