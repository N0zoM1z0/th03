"""Complete original ostream(streambuf*) constructor including RTTI and thunk."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after422_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after422_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'ostream-streambuf-constructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalOstreamStreambufConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'original ostream native receipt absent')
    def test_complete_boss_and_two_native_japanese_links(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 616, 277))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (266, 169506))
        self.assertEqual((r['profiles']['ostctr2']['CODE_bytes'],
                          r['profiles']['ostctr2']['DATA_bytes']), (266, 20))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'source-built ostream constructor OBJ absent')
    def test_original_rtti_adjustor_and_all_thirteen_fixups(self):
        _, _, _, members, _, _ = retained()
        original = original_library_member(members[NATIVE['ostctr2']['index']])
        P = payload(original)
        F = literal_fields(original)
        self.assertEqual(len(P), 286)
        self.assertEqual(len(F), 13)
        self.assertEqual(code_publics(original, 1),
                         [(0, '@ostream@$bctr$qn9streambuf')])
        self.assertEqual(externs(original), NATIVE['ostctr2']['imports'])
        self.assertEqual(bytes(P[1, i] for i in range(134, 142)),
                         bytes.fromhex('8bdc36834704fcea'))
        self.assertEqual(bytes(P[2, i] for i in range(20)),
                         bytes.fromhex('9200000000000000000000000400080086000000'))
        self.assertEqual([(f['segment'], f['site'], f['target_method'],
                           f['target'], f['addend']) for f in F if f['segment'] == 2],
                         [(2, 16, 0, 1, 134), (2, 8, 2, 6, 0), (2, 0, 0, 1, 146)])
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            blob = (ROOT / row['outputs']['ostctr2']['path']).read_bytes()
            self.assertEqual(payload(blob), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(blob)), expected)
            self.assertNotEqual(literal_fields(blob), F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['ostctr2'])
            exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
