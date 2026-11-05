"""Original istream_withassign destructor, local FAR thunk and typed RTTI."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after426_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after426_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'istream-withassign-destructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalIstreamWithassignDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound destructor receipt absent')
    def test_full_destructor_and_two_original_native_rounds(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 622, 271))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (333, 170673))
        self.assertEqual((r['profiles']['istdtr2']['CODE_bytes'],
                          r['profiles']['istdtr2']['DATA_bytes']), (333, 20))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'native original destructor OBJ absent')
    def test_original_far_self_thunk_three_rtti_types_and_sixteen_fixups(self):
        _, _, _, members, _, _ = retained()
        member = members[NATIVE['istdtr2']['index']]
        self.assertEqual(member.name, 'istdtr2')
        original = original_library_member(member)
        P = payload(original)
        F = literal_fields(original)
        self.assertEqual(len(P), 353)
        self.assertEqual(len(F), 16)
        self.assertEqual(code_publics(original, 1), [(0, '@istream_withassign@$bdtr$qv')])
        self.assertEqual(externs(original), NATIVE['istdtr2']['imports'])
        self.assertEqual(bytes(P[1, i] for i in range(115, 123)),
                         bytes.fromhex('8bdc36834704faea'))
        self.assertEqual(bytes(P[1, i] for i in range(165, 185)),
                         b'istream_withassign\0\0')
        self.assertEqual(bytes(P[1, i] for i in range(251, 255)), b'ios\0')
        self.assertEqual(bytes(P[1, i] for i in range(305, 313)), b'istream\0')
        self.assertEqual(bytes(P[2, i] for i in range(20)),
                         bytes.fromhex('7f00000000000000000000000600080073000000'))
        self.assertIn((1, 123, 0, 1, 0),
                      {(f['segment'], f['site'], f['target_method'], f['target'], f['addend'])
                       for f in F})
        self.assertEqual([(f['segment'], f['site'], f['target_method'], f['target'], f['addend'])
                          for f in F if f['segment'] == 2],
                         [(2, 16, 0, 1, 115), (2, 8, 0, 1, 0), (2, 0, 0, 1, 127)])
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for record in receipt['rounds']:
            made = (ROOT / record['outputs']['istdtr2']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(record['literal_omf_fixupp_equal_by_member']['istdtr2'])
            exe = (ROOT / record['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
