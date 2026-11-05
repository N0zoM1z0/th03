"""Nine original complex FAR bodies, real cosh and exact symbolic OMF audit."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_cosh_partial import SOURCE,verify

class OriginalComplexCoshPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_complete_ninth_cosh_and_previous_eight(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,2358,2356))
        self.assertEqual(r['original_complete_FAR_function_bodies'],9)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],2348)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        segment=SOURCE.read_bytes().split(b'public @cosh$qm7complex',1)[1].split(
            b'@cosh$qm7complex endp',1)[0]
        for op in (b'call _exp',b'call _sin',b'call _cos',
                   b'fstp tbyte ptr',b'fld tbyte ptr',
                   b'fld qword ptr es:[bx+8]',b'call @$bnew$qui'):
            self.assertIn(op,segment)
    def test_all_377_original_fixups_and_frame_mode_gap(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],377)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],375)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],329)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),329)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_tasm_rounds_without_false_source_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
