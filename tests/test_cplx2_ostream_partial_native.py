"""Twenty-one exact original cplx2 FAR bodies including ostream complex."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_cplx2_ostream_partial import SOURCE,verify
class OriginalComplexStreamOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=verify()
    def test_twentyone_native_far_functions_and_stream_float_values(self):
        r=self.r
        self.assertEqual((r['full_member_original_CODE_bytes'],
                          r['recovered_original_prefix_CODE_bytes'],
                          r['native_source_CODE_bytes']),(5598,5269,5267))
        self.assertEqual(r['original_complete_FAR_function_bodies'],21)
        self.assertEqual(r['equal_CODE_bytes_outside_two_local_FAR_calls'],5259)
        self.assertEqual(r['omitted_symbolic_local_FAR_calls'],[800,985])
        source=SOURCE.read_bytes()
        self.assertEqual(source.count(b'public @$blsh$qm7ostreamm7complex'),2)
        body=source.split(b'@$blsh$qm7ostreamm7complex proc far',1)[1].split(
            b'@$blsh$qm7ostreamm7complex endp',1)[0]
        self.assertEqual(body.count(b'call @ostream@outstr$qnxct1'),3)
        self.assertEqual(body.count(b'call @ostream@$blsh$qg'),2)
        self.assertEqual(body.count(b'fstp tbyte ptr'),2)
        for x in (b'complex_out_open db "(",0',
                  b'complex_out_separator db ", ",0',
                  b'complex_out_close db ")",0'):
            self.assertIn(x,source)
    def test_all_symbolic_fields_and_original_string_data(self):
        r=self.r
        self.assertEqual(r['original_fixup_count_in_prefix'],829)
        self.assertEqual(r['exact_matching_original_fixups_site_target_addend'],827)
        self.assertEqual(r['original_location_frame4_native_target_frame5_count'],715)
        self.assertEqual(len(set(r['original_location_frame4_sites'])),715)
        self.assertEqual(r['original_genuine_DATA_bytes_equal'],47)
        self.assertFalse(r['original_Borland_complete_FIXUPP_equality'])
    def test_two_native_omf_rounds_but_not_complete_member(self):
        r=self.r
        self.assertEqual(r['native_TASM_rounds'],2)
        self.assertTrue(r['native_nonvolatile_OMF_rounds_equal'])
        self.assertFalse(r['complete_original_member_source'])
        self.assertEqual(r['source_linked_original_CRT_members_added'],0)
        self.assertFalse(r['formal_Factory_source_credit'])
if __name__=='__main__':unittest.main()
