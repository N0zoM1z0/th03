"""Twelve complete original complex FAR bodies and typed logarithm base conversion."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_log10_partial import SOURCE,verify

class OriginalComplexLog10Partial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.proof=verify()
    def test_twelve_full_complex_far_bodies_and_original_log10(self):
        p=self.proof
        self.assertEqual((p['full_member_original_CODE_bytes'],
                          p['recovered_original_prefix_CODE_bytes'],
                          p['native_source_CODE_bytes']),(5598,2868,2866))
        self.assertEqual(p['original_complete_FAR_function_bodies'],12)
        self.assertEqual(p['equal_CODE_bytes_outside_two_local_FAR_calls'],2858)
        self.assertEqual(p['omitted_symbolic_local_FAR_calls'],[800,985])
        src=SOURCE.read_bytes()
        log10=src.split(b'public @log10$qm7complex',1)[1].split(
             b'@log10$qm7complex endp',1)[0]
        for term in (b'call near ptr @log$qm7complex',
                     b'fmul qword ptr DGROUP:complex_log10_factor',
                     b'call @$bnew$qui'):
            self.assertIn(term,log10)
        self.assertEqual(log10.count(b'fmul qword ptr DGROUP:complex_log10_factor'),2)
        self.assertIn(b'dq 0.434294481903251816667932416748954',src)
    def test_symbolic_relocations_and_genuine_double_constant(self):
        p=self.proof
        self.assertEqual(p['original_fixup_count_in_prefix'],435)
        self.assertEqual(p['exact_matching_original_fixups_site_target_addend'],433)
        self.assertEqual(p['original_location_frame4_native_target_frame5_count'],377)
        self.assertEqual(len(set(p['original_location_frame4_sites'])),377)
        self.assertEqual(p['original_genuine_DATA_bytes_equal'],20)
        self.assertEqual(p['original_DATA_implicit_unmaterialized_prefix_bytes'],16)
        self.assertFalse(p['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_rounds_and_no_false_complete_member_credit(self):
        p=self.proof
        self.assertEqual(p['native_TASM_rounds'],2)
        self.assertTrue(p['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(p['native_COMENT_clock_record_indices']),
                         not p['raw_native_obj_sha_equal'])
        self.assertFalse(p['complete_original_member_source'])
        self.assertEqual(p['source_linked_original_CRT_members_added'],0)
        self.assertFalse(p['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
