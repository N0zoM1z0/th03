"""Complete original native strtok state, ordered relocations and 10-source link."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_strtok_work import REPORT
from review_th03_mainl_strtok_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'private 10-source native pair absent')
class StrtokSource(unittest.TestCase):
    def test_original_tok_state_and_merged_mainl(self):
        r=review()
        self.assertEqual((r['original_strtok_CODE_bytes'],
                          r['candidate_strtok_CODE_bytes']), (203,203))
        self.assertEqual(r['literal_native_strtok_FIXUPPs'],12)
        self.assertTrue(r['literal_FIXUPPs_raw_equal'])
        self.assertTrue(r['original_and_native_CODE_equal'])
        self.assertEqual((r['original_BSS_bytes'],r['candidate_BSS_bytes']),(4,4))
        self.assertEqual(r['original_GRPDEF'],'08ff02ff03')
        self.assertEqual((r['original_library_members'],r['source_member_count'],
                          r['untouched_original_member_programs']),(893,10,883))
        self.assertEqual(r['combined_source_CODE_bytes'],13262)
        self.assertTrue(r['original_decoded_EXE_raw_equal'])
        self.assertTrue(r['original_MAP_raw_equal'])
        self.assertEqual((r['original_MZ_relocation_count'],r['whole_EXE_bytes']),
                         (677,67372))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
