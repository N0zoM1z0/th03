"""Cumulative real-source DOS CRT routines in original Japanese MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_crt_growth_work import review

class MemoryScope(unittest.TestCase):
    def check_mode(self,mode,count,bytes_total):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertEqual(r['original_library_members'],893)
        self.assertEqual((len(r['replaced_members']),r['untouched_member_programs']),
                         (count,893-count))
        self.assertEqual(r['total_source_CODE_bytes'],bytes_total)
        self.assertTrue(r['all_native_literally_equal'])
        self.assertTrue(r['original_and_native_ordered_fields_equal'])
        self.assertTrue(r['Japanese_decoded_EXE_raw_equal'])
        self.assertTrue(r['Japanese_MAP_raw_equal'])
        self.assertEqual((r['full_EXE_bytes'],r['MZ_relocations']), (67372,677))
        self.assertEqual(r['native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['accepted_source_bytes_added'],
                          r['full_cold_replay']), (False,0,False))

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-growth-memchr-build.json').exists(),
                         'private memchr source pair absent')
    def test_four_source_memchr(self):
        self.check_mode('memchr',4,161)

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-growth-memchr-memset-build.json').exists(),
                         'private memset source pair absent')
    def test_five_source_memset(self):
        self.check_mode('memchr-memset',5,233)
        r=review('memchr-memset')
        self.assertEqual(r['original_and_native_CODE_bytes']['memset'],[72,72])
        self.assertEqual(r['replaced_members'],
                         ['memchr','memcmp','memcpy','memset','strcmp'])

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-growth-memchr-memset-strlen-build.json').exists(),
                         'private strlen source pair absent')
    def test_six_source_strlen(self):
        self.check_mode('memchr-memset-strlen',6,266)
        r=review('memchr-memset-strlen')
        self.assertEqual(r['original_and_native_CODE_bytes']['strlen'],[33,33])
        self.assertEqual(r['replaced_members'],
                         ['memchr','memcmp','memcpy','memset','strcmp','strlen'])

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-growth-memchr-memset-strlen-strchr-build.json').exists(),
                         'private strchr source pair absent')
    def test_seven_source_strchr(self):
        self.check_mode('memchr-memset-strlen-strchr',7,329)
        r=review('memchr-memset-strlen-strchr')
        self.assertEqual(r['original_and_native_CODE_bytes']['strchr'],[63,63])
        self.assertEqual(r['replaced_members'],
                         ['memchr','memcmp','memcpy','memset','strchr','strcmp','strlen'])
