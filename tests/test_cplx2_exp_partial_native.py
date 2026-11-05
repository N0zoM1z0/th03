"""Ten original cplx2 FAR math functions and exact complex exp source."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_exp_partial import SOURCE,verify

class OriginalComplexExpPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_tenth_exp_body_and_complete_original_code_alignment(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,2564,2562))
        self.assertEqual(r['original_complete_FAR_function_bodies'],10)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],2554)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        exp=SOURCE.read_bytes().split(b'public @exp$qm7complex',1)[1].split(
            b'@exp$qm7complex endp',1)[0]
        self.assertEqual(exp.count(b'call _exp'),1)
        self.assertEqual(exp.count(b'call _sin'),1)
        self.assertEqual(exp.count(b'call _cos'),1)
        self.assertEqual(exp.count(b'call @$bnew$qui'),1)
        self.assertIn(b'fmul qword ptr [bp-10h]',exp)
    def test_all_405_original_fixups_except_known_local_calls(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],405)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],403)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],353)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),353)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_rounds_stable_and_zero_complete_source_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
