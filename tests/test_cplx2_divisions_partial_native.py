"""Native original-prefix proof for three complete FAR cplx2 division APIs."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_divisions_partial import verify,SOURCE

class ComplexDivisionPartialNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=verify()
    def test_original_three_complete_functions_and_code_692(self):
        self.assertEqual(self.r['verified_original_prefix_CODE_bytes'],692)
        self.assertEqual(self.r['total_original_member_CODE_bytes'],5598)
        self.assertEqual(self.r['original_publics_total'],22)
        self.assertEqual(self.r['complete_division_publics'],[
            (0,'@complex@$brdiv$qm7complex'),
            (166,'@$bdiv$qm7complext1'),
            (405,'@$bdiv$qdm7complex')])
        self.assertTrue(self.r['both_native_partial_obj_original_prefix_exact'])
        self.assertIn(b'EMUL',SOURCE.read_bytes())
        self.assertIn(b'fdiv ',SOURCE.read_bytes())
    def test_original_fixup_sites_targets_and_90_explicit_frame_differences(self):
        self.assertEqual(self.r['original_FIXUPP_count'],97)
        self.assertEqual(self.r['exact_FIXUPP_sites_widths_targets_addends'],97)
        self.assertEqual(self.r['original_frame4_vs_TASM_frame5_count'],90)
        self.assertEqual(len(set(self.r['original_frame4_vs_TASM_frame5_sites'])),90)
        self.assertFalse(self.r['exact_original_raw_FIXUPP_frame_metadata'])
    def test_two_independent_native_runs_and_no_unearned_source_credit(self):
        self.assertEqual(self.r['native_assembly_rounds'],2)
        self.assertEqual(len(self.r['rounds']),2)
        self.assertTrue(self.r['nonvolatile_native_OMF_records_equal'])
        self.assertEqual(bool(self.r['native_build_stamp_COMENT_record_indices']),
                         not self.r['raw_TASM_obj_sha256_equal'])
        self.assertTrue(set(self.r['native_build_stamp_COMENT_record_indices']) <= {2})
        self.assertFalse(self.r['complete_original_member_source'])
        self.assertEqual(self.r['source_linked_CRT_members_added'],0)
        self.assertFalse(self.r['factory_accepted_source_credit'])

if __name__=='__main__':unittest.main()
