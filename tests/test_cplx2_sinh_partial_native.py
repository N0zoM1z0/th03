"""Seventeen original complex FAR bodies with exact sinh and OMF symbols."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_sinh_partial import SOURCE,verify
class OriginalComplexSinhPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_full_seventeenth_sinh_and_original_code(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,4208,4206))
        self.assertEqual(r['original_complete_FAR_function_bodies'],17)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],4198)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        s=SOURCE.read_bytes()
        self.assertEqual(s.count(b'public @sinh$qm7complex'),2)
        body=s.split(b'@sinh$qm7complex proc far',1)[1].split(
            b'@sinh$qm7complex endp',1)[0]
        for op in (b'call _exp',b'call _sin',b'call _cos',
                   b'fstp tbyte ptr',b'fld tbyte ptr',
                   b'call @$bnew$qui'):
            self.assertIn(op,body)
        self.assertLess(body.index(b'faddp st(1),st(0)'),
                        body.index(b'fsubp st(1),st(0)'))
    def test_original_654_fixups_and_exposed_frame_gap(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],654)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],652)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],564)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),564)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],36)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_without_unearned_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
