"""Original DOS full native strncpy/movmem source plus a real MAINL link."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_crt_expand_work import review

class CumulativeNativeCRT(unittest.TestCase):
    def check(self,mode,count,bytes_total,unchanged):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertEqual((r['native_source_members'],r['unchanged_original_member_programs']),
                         (count,unchanged))
        self.assertEqual(r['cumulative_source_CODE_bytes'],bytes_total)
        self.assertTrue(r['original_and_native_CODE_equal'])
        self.assertTrue(r['ordered_native_FIXUPPs_equal'])
        self.assertTrue(r['original_publics_and_groups_equal'])
        self.assertTrue(r['whole_exe_equal'])
        self.assertTrue(r['whole_map_equal'])
        self.assertEqual((r['original_exe_bytes'],r['original_mz_relocation_count']),
                         (67372,677))
        self.assertEqual((r['deterministic_native_rounds'],r['added_accepted_bytes']),
                         (2,0))

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-expand-strncpy-build.json').is_file(),
                         'private strncpy source pair absent')
    def test_strncpy_counted_zero_filling(self):
        self.check('strncpy',13,13832,880)
        r=review('strncpy')
        self.assertEqual(r['original_and_source_profiles']['strncpy']['CODE_bytes'],49)
        self.assertEqual(r['original_and_source_profiles']['strncpy']['publics'],
                         [[0,'_strncpy']])

    @unittest.skipUnless((ROOT/'.analysis/work/mainl-crt-expand-strncpy-movmem-build.json').is_file(),
                         'private overlap-safe memory source pair absent')
    def test_original_overlap_safe_movmem_and_memmove(self):
        self.check('strncpy-movmem',14,13951,879)
        r=review('strncpy-movmem')
        mov=r['original_and_source_profiles']['movmem']
        self.assertEqual(mov['CODE_bytes'],119)
        self.assertEqual(mov['publics'],[[0,'_movmem'],[82,'_memmove']])
        self.assertEqual(mov['imports'],['N_PCMP@'])
        self.assertEqual(len(mov['literal_fields']),1)
        self.assertEqual(mov['literal_fields'][0]['site'],19)
        self.assertEqual(mov['literal_fields'][0]['frame_method'],0)
