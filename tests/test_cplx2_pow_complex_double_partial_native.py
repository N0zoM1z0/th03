"""Thirteen native complex FAR functions including full 358-byte pow operator."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_pow_complex_double_partial import SOURCE,verify
class OriginalComplexPowDoublePartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_thirteen_complete_far_bodies_and_pow_zero_base_path(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,3226,3224))
        self.assertEqual(r['original_complete_FAR_function_bodies'],13)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],3216)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        pow_body=SOURCE.read_bytes().split(b'public @pow$qm7complexd',1)[1].split(
            b'@pow$qm7complexd endp',1)[0]
        for code in (b'fcompp',b'call near ptr @arg$qm7complex',
                     b'call @abs$qm7complex',b'call _pow',
                     b'call _sin',b'call _cos',b'call @$bnew$qui',
                     b'jmp near ptr pow_final_return'):
            self.assertIn(code,pow_body)
        self.assertIn(b'pow_stored_result:',pow_body)
        self.assertIn(b'pow_final_return:',pow_body)
    def test_all_492_original_fixups_and_425_frame4_gaps(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],492)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],490)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],425)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),425)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],20)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_native_omf_rounds_and_proof_scope(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
