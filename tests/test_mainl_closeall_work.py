"""Original 99-byte far fcloseall complete OMF and 34-source MAINL link."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_closeall_work import REPORT
from review_th03_mainl_closeall_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),'native 34-source closeall pair absent')
class OriginalCloseall(unittest.TestCase):
    def test_native_source_exact_and_original_omf_limit_retained(self):
        r=review()
        self.assertEqual(r['newly_recovered_native_CODE_bytes'],99)
        self.assertTrue(r['all_native_CODE_bytes_equal'])
        self.assertEqual(r['original_public'],'_fcloseall')
        self.assertEqual(r['original_ordered_OMF_fields'],3)
        self.assertTrue(r['ordered_FIXUPPs_raw_equal'])
        self.assertEqual(r['original_imports'],['__streams','__nfile','_fclose'])
        self.assertEqual((r['original_CRT_members'],r['working_source_members'],
                          r['unchanged_original_member_programs']),(893,34,859))
        self.assertEqual(r['cumulative_original_source_CODE_bytes'],20527)
        self.assertTrue(r['previous_fopen_native_OMF_order_still_open'])
        self.assertTrue(r['whole_original_Japanese_EXE_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['real_Japanese_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['repeated_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes']),
                         (False,0))
