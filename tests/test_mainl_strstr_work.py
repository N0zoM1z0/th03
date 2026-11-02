"""Complete original substring search and nine-source MAINL native link."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strstr_work import REPORT
from review_th03_mainl_strstr_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private 9-source link not retained')
class StrstrSource(unittest.TestCase):
    def test_natural_strstr_and_original_mainl(self):
        r=review()
        self.assertTrue(r['complete'])
        self.assertEqual((r['source_CODE_bytes'],r['total_source_CODE_bytes']),
                         (108,13059))
        self.assertTrue(r['original_and_candidate_CODE_equal'])
        self.assertTrue(r['original_and_candidate_literal_fields_equal'])
        self.assertEqual((r['original_library_members'],len(r['nine_source_members']),
                          r['unchanged_member_programs']),(893,9,884))
        self.assertEqual((r['complete_EXE_bytes'],r['MZ_relocations']),(67372,677))
        self.assertTrue(r['exact_whole_Japanese_EXE'])
        self.assertTrue(r['exact_whole_Japanese_MAP'])
        self.assertEqual(r['native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
