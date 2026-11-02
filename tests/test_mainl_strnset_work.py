"""Complete Borland strnset source,two far FIXUPPs and 16-source MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strnset_work import REPORT
from review_th03_mainl_strnset_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native original strnset pair unavailable')
class StrnsetSource(unittest.TestCase):
    def test_exact_bounded_setmem_strlen_and_whole_original_mainl(self):
        r=review()
        self.assertEqual(r['original_and_native_CODE_bytes'],[58,58])
        self.assertEqual(r['original_public'],'_strnset')
        self.assertEqual(r['original_exports'],['_strlen','_setmem'])
        self.assertEqual(r['ordered_native_FIXUPPs'],2)
        self.assertTrue(r['literal_fields_raw_equal'])
        self.assertEqual((r['original_library_members'],
                          r['reconstructed_source_members'],
                          r['unchanged_member_program_records']), (893,16,877))
        self.assertEqual(r['cumulative_naturally_compiled_CODE_bytes'],14114)
        self.assertEqual((r['source_linked_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertTrue(r['complete_Japanese_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']), (False,0,False))
