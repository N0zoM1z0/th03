"""Six original complex FAR bodies with native asin and precisely audited OMF."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_asin_partial import SOURCE,verify
class SixOriginalComplexFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=verify()
    def test_six_real_far_functions_and_391_byte_asin(self):
        r=self.result
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,1608,1606))
        self.assertEqual(r['original_complete_FAR_function_bodies'],6)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],1598)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        source=SOURCE.read_bytes()
        self.assertIn(b'@asin$qm7complex proc far',source)
        asin=source.split(b'public @asin$qm7complex',1)[1].split(
                  b'@asin$qm7complex endp',1)[0]
        self.assertEqual(asin.count(b'call _sin'),1)
        self.assertEqual(asin.count(b'call _cos'),1)
        self.assertLess(asin.index(b'call _sin'),asin.index(b'call _cos'))
    def test_original_relocation_sites_names_addends_and_frame4_gaps(self):
        r=self.result
        self.assertEqual(r['original_fixup_count_in_prefix'],248)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],246)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],218)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),218)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],12)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_without_complete_member_credit(self):
        r=self.result
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertEqual(bool(r['native_COMENT_clock_record_indices']),
                         not r['raw_native_obj_sha_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
