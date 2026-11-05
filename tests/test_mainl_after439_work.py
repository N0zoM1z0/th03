"""Original streambuf default ctor, typed RTTI and 11 virtual slots."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after439_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after439_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'streambuf-base-default-constructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalStreambufBaseConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound native constructor missing')
    def test_complete_original_code_data_and_two_native_rounds(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 647, 246))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (237, 174691))
        self.assertEqual((r['profiles']['stbctr1']['CODE_bytes'],
                          r['profiles']['stbctr1']['DATA_bytes']), (237, 52))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'original streambuf OMF pair missing')
    def test_true_object_layout_rtti_and_all_sixteen_fixups(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['stbctr1']['index']]
        self.assertEqual(m.name, 'stbctr1')
        orig = original_library_member(m)
        P = payload(orig)
        F = literal_fields(orig)
        self.assertEqual(len(P), 289)
        self.assertEqual(len(F), 16)
        self.assertEqual(code_publics(orig, 1), [(0, '@streambuf@$bctr$qv')])
        self.assertEqual(externs(orig), NATIVE['stbctr1']['imports'])
        self.assertEqual(bytes(P[2, i] for i in range(52)),
                         bytes.fromhex('b100') + bytes(50))
        self.assertIn(b'streambuf\0', bytes(P[1, i] for i in range(237)))
        fields = {(f['segment'], f['site']): f for f in F}
        self.assertEqual((fields[(1, 39)]['target_method'],
                          fields[(1, 39)]['target'], fields[(1, 39)]['addend']),
                         (0, 2, 8))
        self.assertEqual((fields[(2, 0)]['target_method'],
                          fields[(2, 0)]['target'], fields[(2, 0)]['addend']),
                         (0, 1, 177))
        self.assertEqual((fields[(2, 28)]['target_method'], fields[(2, 28)]['target']),
                         (2, 8))
        self.assertEqual((fields[(2, 32)]['target_method'], fields[(2, 32)]['target']),
                         (2, 9))
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made = (ROOT / row['outputs']['stbctr1']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)), expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['stbctr1'])
            exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__':
    unittest.main()
