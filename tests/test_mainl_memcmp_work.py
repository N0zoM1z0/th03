"""Real forty-byte DOS comparator and two-source MAINL native link."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_memcmp_combo_work import REPORT as BUILD_REPORT
from review_th03_mainl_memcmp_work import review

@unittest.skipUnless((ROOT/BUILD_REPORT).is_file(),'private native two-source pair absent')
class MemcmpNativeReconstruction(unittest.TestCase):
    def test_real_memcmp_and_memcpy_native_link(self):
        r=review()
        self.assertTrue(r['complete'])
        self.assertEqual(r['original_and_candidate_memcmp_CODE_bytes'],[40,40])
        self.assertEqual(r['native_memcmp_ordered_fixups'],[0,0])
        self.assertEqual(r['original_memcmp_OMF_GROUP'],'08ff03ff02')
        self.assertEqual(r['source_member_indices'],[260,261])
        self.assertEqual(r['replaced_members'],['memcmp','memcpy'])
        self.assertEqual((r['all_original_library_members'],
                          r['unchanged_original_member_programs']),(893,891))
        self.assertEqual((r['full_decoded_EXE_bytes'],
                          r['full_decoded_MZ_relocations']),(67372,677))
        self.assertTrue(r['whole_decoded_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual(r['deterministic_complete_rounds'],2)
        self.assertEqual((r['source_acceptance'],
                          r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

if __name__=='__main__': unittest.main()
