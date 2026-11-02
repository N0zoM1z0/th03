"""Original 153-byte buffered fwrite and 29-source normal Japanese MAINL."""
import sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_fwrite_work import review
from build_th03_mainl_fwrite_work import REPORT

@unittest.skipUnless((ROOT/REPORT).is_file(),'private native fwrite source pair absent')
class FwriteNative(unittest.TestCase):
    def test_real_fwrite_full_omf_and_executable(self):
        r=review()
        self.assertTrue(r['full_native_CODE_equal'])
        self.assertEqual((r['original_CODE_bytes'],r['source_CODE_bytes']),(153,153))
        self.assertEqual((r['original_public'],r['original_literal_FIXUPPs']),
                         ('_fwrite',4))
        self.assertTrue(r['all_native_FIXUPPs_equal'])
        self.assertEqual(r['original_extdef_order'],['__FPUTN','N_LXMUL@','N_PADD@'])
        self.assertEqual((r['original_library_members'],r['full_source_member_count'],
                          r['unchanged_original_member_programs']),(893,29,864))
        self.assertEqual(r['joint_exact_source_CODE_bytes'],18855)
        self.assertTrue(r['entire_original_EXE_raw_equal'])
        self.assertTrue(r['whole_MAP_raw_equal'])
        self.assertEqual((r['original_MZ_relocations'],r['EXE_file_bytes']),(677,67372))
        self.assertEqual(r['repeated_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
