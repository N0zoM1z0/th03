"""Eleven complete original complex functions with native log semantics."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_log_partial import SOURCE,verify
class OriginalComplexLogPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_complete_log_and_original_prefix_code(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,2708,2706))
        self.assertEqual(r['original_complete_FAR_function_bodies'],11)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],2698)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        log=SOURCE.read_bytes().split(b'public @log$qm7complex',1)[1].split(
            b'@log$qm7complex endp',1)[0]
        self.assertIn(b'call near ptr @arg$qm7complex',log)
        self.assertIn(b'call @abs$qm7complex',log)
        self.assertIn(b'call _log',log)
        self.assertIn(b'call @$bnew$qui',log)
    def test_original_relocations_and_remaining_frame_differences(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],419)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],417)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],364)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),364)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_rounds_without_complete_member_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
