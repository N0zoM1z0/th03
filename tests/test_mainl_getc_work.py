"""Whole four-entry DOS fgetc/getc runtime with exact Japanese MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_getc_work import REPORT
from review_th03_mainl_getc_work import review

@unittest.skipUnless((ROOT/REPORT).is_file(),
                     'retained native getc 30-source pair absent')
class GetcOriginalSource(unittest.TestCase):
    def test_original_485_byte_four_entry_getc_and_complete_link(self):
        r=review()
        self.assertEqual((r['original_getc_CODE_bytes'],
                          r['source_getc_CODE_bytes']),(485,485))
        self.assertTrue(r['all_native_CODE_bytes_equal'])
        self.assertEqual(r['original_8086_instruction_count'],193)
        self.assertEqual((r['original_native_BSS_bytes'],
                          r['source_native_BSS_bytes']),(1,1))
        self.assertEqual(r['original_public_entries'],
                         [(192,'__fgetc'),(217,'__Nfgetc'),
                          (220,'_fgetc'),(469,'_fgetchar')])
        self.assertEqual(r['original_external_imports'],
                         ['__streams','_fflush','_eof','___read'])
        self.assertEqual(r['original_literal_OMF_FIXUPPs'],9)
        self.assertTrue(r['all_nine_original_ordered_FIXUPPs_equal'])
        self.assertTrue(r['near_and_far_ABI_preserved'])
        self.assertEqual(r['near_to_far_public_bridge'],'580e50')
        self.assertEqual((r['original_CRT_members'],r['source_CRT_members'],
                          r['untouched_original_programs']),(893,30,863))
        self.assertEqual(r['total_joint_source_CODE_bytes'],19340)
        self.assertTrue(r['full_original_EXE_raw_equal'])
        self.assertTrue(r['original_MAP_raw_equal'])
        self.assertEqual((r['original_Japanese_EXE_bytes'],r['MZ_relocation_count']),
                         (67372,677))
        self.assertEqual(r['native_repeated_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))
