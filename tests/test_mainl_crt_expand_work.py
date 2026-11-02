"""Complete original counted copy and overlap-safe move source CRT candidates."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_crt_expand_work import review

class NativeCrtExpansion(unittest.TestCase):
    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-expand-strncpy-build.json').is_file(),
                         'private strncpy source pair missing')
    def test_counted_copy_native_source(self):
        x=review('strncpy')
        self.assertEqual((x['source_members'],x['unchanged_original_program_records']),(13,880))
        self.assertEqual(x['new_module_CODE_bytes'],{'strncpy':49})
        self.assertEqual(x['source_built_total_CODE_bytes'],13832)
        self.assertTrue(x['native_CODE_and_ordered_fields_equal'])
        self.assertTrue(x['original_decoded_Japanese_EXE_raw_equal'])
        self.assertTrue(x['original_complete_MAP_raw_equal'])
        self.assertEqual(x['complete_native_rounds'],2)
        self.assertEqual((x['source_acceptance'],x['added_accepted_bytes'],
                          x['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-expand-strncpy-movmem-build.json').is_file(),
                         'private overlap move source pair missing')
    def test_counted_copy_and_original_overlap_safe_move(self):
        x=review('strncpy-movmem')
        self.assertEqual((x['source_members'],x['unchanged_original_program_records']),(14,879))
        self.assertEqual(x['new_module_CODE_bytes'],{'strncpy':49,'movmem':119})
        self.assertEqual(x['source_built_total_CODE_bytes'],13951)
        self.assertTrue(x['native_CODE_and_ordered_fields_equal'])
        self.assertTrue(x['original_decoded_Japanese_EXE_raw_equal'])
        self.assertTrue(x['original_complete_MAP_raw_equal'])
        self.assertEqual((x['original_EXE_file_bytes'],x['original_MZ_relocations']),(67372,677))
        self.assertEqual(x['complete_native_rounds'],2)
        self.assertEqual((x['source_acceptance'],x['added_accepted_bytes'],
                          x['original_cold_rebuilt']),(False,0,False))
