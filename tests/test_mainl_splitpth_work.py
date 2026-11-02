"""Full DOS splitpath/fnsplit CODE and both original symbolic switch tables."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_splitpth_work import REPORT
from review_th03_mainl_splitpth_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'original native path splitting pair absent')
class OriginalPathSplit(unittest.TestCase):
    def test_entire_850_code_and_two_real_lookup_tables(self):
        r=review()
        self.assertEqual((r['original_splitpth_CODE_bytes'],
                          r['native_CODE_bytes']),(850,850))
        self.assertTrue(r['entire_native_CODE_raw_equal'])
        self.assertEqual(r['original_executable_instruction_region_sizes'],
                         [92,122,546,46])
        self.assertEqual(r['original_source_CODE_tables_bytes'],44)
        self.assertEqual(r['original_table_switch_relocation_words'],11)
        self.assertEqual(r['original_far_public_offsets'],[230,804])
        self.assertEqual(r['original_literal_OMF_fields'],20)
        self.assertTrue(r['all_native_ordered_fixups_equal'])
        self.assertEqual((r['original_library_members'],r['simultaneous_source_modules'],
                          r['unchanged_vendor_program_records']),(893,47,846))
        self.assertEqual(r['joint_exact_original_source_CODE_bytes'],24627)
        self.assertTrue(r['complete_Japanese_EXE_raw_equal'])
        self.assertTrue(r['complete_original_MAP_equal'])
        self.assertEqual((r['original_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertTrue(r['inherited_fopen_OMF_gap_open'])
        self.assertTrue(r['inherited_fclose_frame_gap_open'])
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
