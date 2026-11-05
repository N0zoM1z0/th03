"""Seven original cplx2 FAR x87 function bodies through atan(complex)."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_atan_partial import SOURCE,verify
class SevenOriginalComplexFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.proof=verify()
    def test_complete_seventh_far_atan_283_native_code_bytes(self):
        p=self.proof
        self.assertEqual((p['full_member_original_CODE_bytes'],
                          p['recovered_original_prefix_CODE_bytes'],
                          p['native_source_CODE_bytes']),(5598,1891,1889))
        self.assertEqual(p['original_complete_FAR_function_bodies'],7)
        self.assertEqual(p['equal_CODE_bytes_outside_two_local_FAR_calls'],1881)
        self.assertEqual(p['omitted_symbolic_local_FAR_calls'],[800,985])
        source=SOURCE.read_bytes()
        self.assertIn(b'@atan$qm7complex proc far',source)
        atan=source.split(b'@atan$qm7complex proc far',1)[1].split(
                  b'@atan$qm7complex endp',1)[0]
        self.assertIn(b'call @abs$qm7complex',atan)
        self.assertIn(b'call @arg$qm7complex',atan)
        self.assertIn(b'call _log',atan)
        self.assertIn(b'call @$bnew$qui',atan)
        self.assertIn(b'fdiv dword ptr DGROUP:complex_two_float',atan)
    def test_relocated_targets_and_precise_original_frame_methods(self):
        p=self.proof
        self.assertEqual(p['original_fixup_count_in_prefix'],297)
        self.assertEqual(p['exact_matching_original_fixups_site_target_addend'],295)
        self.assertEqual(p['original_location_frame4_native_target_frame5_count'],261)
        self.assertEqual(len(set(p['original_location_frame4_sites'])),261)
        self.assertEqual(p['original_genuine_DATA_bytes_equal'],12)
        self.assertEqual(p['original_DATA_implicit_unmaterialized_prefix_bytes'],16)
        self.assertFalse(p['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_without_unearned_source_credit(self):
        p=self.proof
        self.assertEqual(p['native_TASM_rounds'],2)
        self.assertTrue(p['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(p['native_COMENT_clock_record_indices']),
                         not p['raw_native_obj_sha_equal'])
        self.assertFalse(p['complete_original_member_source'])
        self.assertEqual(p['source_linked_original_CRT_members_added'],0)
        self.assertFalse(p['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
