"""Seven original cplx2 FAR bodies and fully audited atan(complex)."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_atan_partial import SOURCE,verify
class OriginalComplexAtanPartial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_seven_complete_functions_and_actual_atan_math(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,1891,1889))
        self.assertEqual(r['original_complete_FAR_function_bodies'],7)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],1881)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        src=SOURCE.read_bytes()
        self.assertIn(b'@atan$qm7complex proc far',src)
        atan=src.split(b'public @atan$qm7complex',1)[1].split(
            b'@atan$qm7complex endp',1)[0]
        self.assertIn(b'call @abs$qm7complex',atan)
        self.assertIn(b'call _log',atan)
        self.assertIn(b'call @arg$qm7complex',atan)
        self.assertIn(b'call @$bnew$qui',atan)
        self.assertIn(b'fsubrp st(1),st(0)',atan)
    def test_297_true_fixups_and_original_frame4_not_normalized(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],297)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],295)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],261)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),261)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],12)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_without_unearned_crt_credit(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
