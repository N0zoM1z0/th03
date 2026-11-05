"""Complete source-owned streambuf destructor with real far buffer cleanup."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after440_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after440_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'streambuf-base-destructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalStreambufBaseDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound destructor receipt missing')
    def test_complete_original_source_and_two_native_rounds(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 648, 245))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (153, 174844))
        self.assertEqual((r['profiles']['stbdtr']['CODE_bytes'],
                          r['profiles']['stbdtr']['DATA_bytes']), (153, 52))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'original streambuf destructor OMF missing')
    def test_real_far_delete_reference_rtti_and_seventeen_fixups(self):
        _, _, _, members, _, _ = retained()
        member = members[NATIVE['stbdtr']['index']]
        self.assertEqual(member.name, 'stbdtr')
        original = original_library_member(member)
        P = payload(original)
        F = literal_fields(original)
        self.assertEqual(len(P), 205)
        self.assertEqual(len(F), 17)
        self.assertEqual(code_publics(original, 1), [(0, '@streambuf@$bdtr$qv')])
        self.assertEqual(externs(original), NATIVE['stbdtr']['imports'])
        self.assertEqual(bytes(P[2, i] for i in range(52)),
                         bytes.fromhex('5d00') + bytes(50))
        self.assertIn(b'streambuf\0', bytes(P[1, i] for i in range(153)))
        fields = {(f['segment'], f['site']): f for f in F}
        self.assertEqual((fields[(1, 37)]['target_method'],
                          fields[(1, 37)]['target'], fields[(1, 37)]['addend']),
                         (0, 2, 8))
        self.assertEqual((fields[(1, 55)]['target_method'], fields[(1, 55)]['target']),
                         (2, 2))
        self.assertEqual((fields[(1, 83)]['target_method'], fields[(1, 83)]['target']),
                         (2, 1))
        self.assertEqual((fields[(2, 8)]['target_method'],
                          fields[(2, 8)]['target'], fields[(2, 8)]['addend']),
                         (0, 1, 0))
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        r = json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made = (ROOT / row['outputs']['stbdtr']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)), expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['stbdtr'])
            exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__':
    unittest.main()
