"""Original ostream_withassign default ctor with actual adjustment thunk and RTTI."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after419_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after419_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'ostream-withassign-default-constructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalOstreamWithassignConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound ostream_withassign receipt absent')
    def test_entire_native_constructor_and_original_japanese_link(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 606, 287))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (349, 168411))
        self.assertEqual((r['profiles']['ostctr3']['CODE_bytes'],
                          r['profiles']['ostctr3']['DATA_bytes']), (349, 20))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound constructor native OBJ absent')
    def test_thunk_three_typed_rtti_and_all_sixteen_relocation_fields(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['ostctr3']['index']]
        self.assertEqual(m.name, 'ostctr3')
        orig = original_library_member(m)
        P = payload(orig)
        F = literal_fields(orig)
        self.assertEqual(len(P), 369)
        self.assertEqual(len(F), 16)
        self.assertEqual(code_publics(orig, 1), [(0, '@ostream_withassign@$bctr$qv')])
        self.assertEqual(externs(orig), NATIVE['ostctr3']['imports'])
        self.assertEqual(bytes(P[1, i] for i in range(131, 139)),
                         bytes.fromhex('8bdc36834704fcea'))
        self.assertEqual(bytes(P[1, i] for i in range(181, 201)),
                         b'ostream_withassign\0\0')
        self.assertEqual(bytes(P[1, i] for i in range(267, 271)), b'ios\0')
        self.assertEqual(bytes(P[1, i] for i in range(321, 329)), b'ostream\0')
        self.assertEqual(bytes(P[2, i] for i in range(20)),
                         bytes.fromhex('8f00000000000000000000000400080083000000'))
        self.assertEqual([(f['segment'], f['site'], f['target_method'], f['target'], f['addend'])
                          for f in F if f['segment'] == 2],
                         [(2, 16, 0, 1, 131), (2, 8, 2, 7, 0), (2, 0, 0, 1, 143)])
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for record in receipt['rounds']:
            made = (ROOT / record['outputs']['ostctr3']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(record['literal_omf_fixupp_equal_by_member']['ostctr3'])
            exe = (ROOT / record['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
