"""Original 356-CODE/12-DATA stdiostream destructor and four typed RTTI blocks."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after418_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after418_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'stdiostream-destructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalStdiostreamDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound destructor receipt absent')
    def test_complete_destructor_and_two_native_japanese_links(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 605, 288))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (356, 168062))
        self.assertEqual((r['profiles']['sddtr']['CODE_bytes'],
                          r['profiles']['sddtr']['DATA_bytes']), (356, 12))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'native source-built destructor absent')
    def test_four_rtti_classes_destructor_and_all_fourteen_logical_fixups(self):
        _, _, _, members, _, _ = retained()
        member = members[NATIVE['sddtr']['index']]
        self.assertEqual(member.name, 'sddtr')
        orig = original_library_member(member)
        P = payload(orig)
        F = literal_fields(orig)
        self.assertEqual(len(P), 368)
        self.assertEqual(code_publics(orig, 1), [(0, '@stdiostream@$bdtr$qv')])
        self.assertEqual(externs(orig), NATIVE['sddtr']['imports'])
        self.assertEqual(len(F), 14)
        self.assertEqual(bytes(P[1, i] for i in range(136, 148)), b'stdiostream\0')
        self.assertEqual(bytes(P[1, i] for i in range(212, 222)), b'stdiobuf\0\0')
        self.assertEqual(bytes(P[1, i] for i in range(280, 284)), b'ios\0')
        self.assertEqual(bytes(P[1, i] for i in range(334, 344)), b'streambuf\0')
        self.assertEqual(bytes(P[2, i] for i in range(12)),
                         bytes.fromhex('620000000000000000000000'))
        self.assertEqual([(f['segment'], f['site']) for f in F if f['segment'] == 2],
                         [(2, 8), (2, 0)])
        self.assertEqual([(f['site'], f['target_method'], f['target'], f['addend'])
                          for f in F if f['segment'] == 1 and f['site'] in (128, 148, 164, 222)],
                         [(222, 0, 1, 296), (164, 0, 1, 174),
                          (148, 0, 1, 242), (128, 0, 1, 0)])
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for round_record in receipt['rounds']:
            made = (ROOT / round_record['outputs']['sddtr']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(round_record['literal_omf_fixupp_equal_by_member']['sddtr'])
            exe = (ROOT / round_record['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
