"""Real native code/data/OMF fields and full Japanese MAINL after scanner."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_postscanner_work import review
from build_th03_mainl_postscanner_work import PREFIX

class NativeCrtAfterScanner(unittest.TestCase):
    def check(self,mode,count,total,extra_data):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_member_count'],r['native_source_member_count'],
                          r['unchanged_original_member_programs']),
                         (893,count,893-count))
        self.assertEqual(r['joint_native_source_CODE_bytes'],total)
        self.assertEqual(r['freshly_recovered_initialized_DATA_bytes'],extra_data)
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['ordered_literal_FIXUPPs_equal'])
        self.assertTrue(r['native_group_and_publics_equal'])
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['original_MAP_raw_equal'])
        self.assertEqual((r['whole_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['reproducible_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['full_cold_replay']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'strrchr-build.json')).is_file(),
                         'private source-only strrchr round pair absent')
    def test_strrchr_original_far_strlen_and_reverse_scan(self):
        self.check('strrchr',24,17845,0)
        o=review('strrchr')['original_and_source_profiles']['strrchr']
        self.assertEqual(o['CODE_bytes'],77)
        self.assertEqual(o['externs'],['_strlen'])
        self.assertEqual(o['publics'],[[0,'_strrchr']])
        self.assertEqual(len(o['literal_fields']),1)
        self.assertEqual(o['literal_fields'][0]['site'],15)
        self.assertEqual(o['literal_fields'][0]['frame_method'],5)

    @unittest.skipUnless((ROOT/(PREFIX+'strrchr-srchstr-build.json')).is_file(),
                         'private native path resolution source pair absent')
    def test_srchstr_original_322_code_2_data_and_ten_fixups(self):
        self.check('strrchr-srchstr',25,18167,2)
        o=review('strrchr-srchstr')['original_and_source_profiles']['srchstr']
        self.assertEqual(o['CODE_bytes'],322)
        self.assertEqual(o['DATA_bytes'],2)
        self.assertEqual(o['publics'],[[0,'__searchstr']])
        self.assertEqual(len(o['literal_fields']),10)

    @unittest.skipUnless((ROOT/(PREFIX+'strrchr-srchstr-strrev-build.json')).is_file(),
                         'private native source strrev pair absent')
    def test_strrev_original_inplace_far_reversal(self):
        self.check('strrchr-srchstr-strrev',26,18219,2)

    @unittest.skipUnless((ROOT/(PREFIX+'strrchr-srchstr-strrev-strset-build.json')).is_file(),
                         'private native source strset pair absent')
    def test_strset_original_large_model_setmem_chain(self):
        self.check('strrchr-srchstr-strrev-strset',27,18265,2)
