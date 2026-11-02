"""Complete native nested-BCC strset and 27 original DOS source CRT modules."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strset_work import REPORT
from review_th03_mainl_strset_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native source strset pair not retained')
class StrsetSource(unittest.TestCase):
    def test_exact_original_far_strset_nested_call_and_mainl(self):
        r=review()
        self.assertEqual(r['original_and_native_CODE_bytes'],[46,46])
        self.assertEqual(r['original_public'],'_strset')
        self.assertEqual(r['original_exports'],['_strlen','_setmem'])
        self.assertEqual(r['ordered_native_FIXUPPs'],2)
        self.assertTrue(r['literal_fields_raw_equal'])
        self.assertEqual((r['original_library_members'],r['reconstructed_source_members'],
                          r['unchanged_member_program_records']),(893,27,866))
        self.assertEqual(r['cumulative_naturally_compiled_CODE_bytes'],18265)
        self.assertTrue(r['complete_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['original_MZ_relocations'],r['source_linked_EXE_bytes']),
                         (677,67372))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
