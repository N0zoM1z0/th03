"""Complete original DOS scanner/CRT source replacements in actual MAINL."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_native_extension_work import review
from build_th03_mainl_native_extension_work import PREFIX

class NativeCrt(unittest.TestCase):
    def check(self,mode,member_count,total):
        r=review(mode)
        self.assertTrue(r['complete'])
        self.assertEqual(r['original_CRT_member_count'],893)
        self.assertEqual((r['native_source_member_count'],
                          r['unchanged_original_member_programs']),
                         (member_count,893-member_count))
        self.assertEqual(r['joint_native_source_CODE_bytes'],total)
        self.assertTrue(r['complete_native_CODE_equal'])
        self.assertTrue(r['ordered_literal_FIXUPPs_equal'])
        self.assertTrue(r['native_group_and_publics_equal'])
        self.assertTrue(r['entire_Japanese_EXE_raw_equal'])
        self.assertTrue(r['original_MAP_raw_equal'])
        self.assertEqual((r['whole_EXE_bytes'],r['original_MZ_relocations']),
                         (67372,677))
        self.assertEqual(r['reproducible_native_rounds'],2)
        self.assertEqual((r['source_acceptance'],r['added_accepted_bytes'],
                          r['original_cold_rebuilt']),(False,0,False))

    @unittest.skipUnless((ROOT/(PREFIX+'scantol-build.json')).is_file(),
                         'private 19-source native scanner pair absent')
    def test_near_integer_scantol_with_target_frame_fixup(self):
        self.check('scantol',19,16251)
        sc=review('scantol')['original_and_source_profiles']['scantol']
        self.assertEqual(sc['CODE_bytes'],465)
        self.assertEqual(sc['publics'],[[47,'__scantol']])
        self.assertEqual(sc['externs'],['__ctype'])
        self.assertEqual(len(sc['fields']),1)
        self.assertEqual(sc['fields'][0]['site'],95)
        self.assertEqual(sc['fields'][0]['frame_method'],5)
        self.assertEqual(sc['fields'][0]['target_method'],2)
        self.assertEqual(sc['fields'][0]['addend'],1)

    @unittest.skipUnless((ROOT/(PREFIX+'scantol-strspn-build.json')).is_file(),
                         'private 20-source native strspn pair absent')
    def test_span_accept_set(self):
        self.check('scantol-strspn',20,16333)

    @unittest.skipUnless((ROOT/(PREFIX+'scantol-strspn-strcspn-build.json')).is_file(),
                         'private 21-source native strcspn pair absent')
    def test_span_reject_set(self):
        self.check('scantol-strspn-strcspn',21,16406)

    @unittest.skipUnless((ROOT/(PREFIX+'scantol-strspn-strcspn-strpbrk-build.json')).is_file(),
                         'private 22-source native strpbrk pair absent')
    def test_first_matching_character_far_pointer(self):
        self.check('scantol-strspn-strcspn-strpbrk',22,16486)
