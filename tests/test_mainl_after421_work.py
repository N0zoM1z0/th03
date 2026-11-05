"""Eight exact original stream, DOS file and NEC/IBM sound CRT leaves."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after421_work import (PREFIX, WORK, NATIVE, MODES,
                                              retained, original_library_member, scope)
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after421_work import review
from lib.pc98 import parse_mz
MODE = 'eight-stream-dos-sound-leaves'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalEightStreamDosSound(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound eight CRT leaves receipt absent')
    def test_native_original_code_all_eight_and_whole_japanese_link(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 615, 278))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (496, 169240))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertEqual(len(r['profiles']), 8)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound individual CRT pairs absent')
    def test_each_member_exact_and_only_two_literal_record_order_gaps(self):
        _, _, _, members, carry, _ = retained()
        names = MODES[MODE]
        self.assertEqual(len(names), 8)
        self.assertFalse(set(names) & set(carry[0][0]))
        literal_exact = set(names) - {'ostwrite', 'ccomsond'}
        self.assertEqual(len(literal_exact), 6)
        receipt = json.loads(RECEIPT.read_text())
        for name in names:
            orig = original_library_member(members[NATIVE[name]['index']])
            P = payload(orig)
            F = literal_fields(orig)
            self.assertEqual(len(P), NATIVE[name]['code'])
            self.assertEqual(members[NATIVE[name]['index']].name, name)
            self.assertEqual(len(F), NATIVE[name]['fields'])
            for record in receipt['rounds']:
                with self.subTest(member=name, round=record['round']):
                    made = (ROOT / record['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made), P)
                    self.assertEqual(scope(name, made), scope(name, orig))
                    self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                            for f in literal_fields(made)),
                                     sorted(tuple(f[k] for k in KEYS) for f in F))
                    self.assertEqual(literal_fields(made) == F, name in literal_exact)
                    self.assertEqual(record['literal_omf_fixupp_equal_by_member'][name],
                                     name in literal_exact)
        for record in receipt['rounds']:
            exe = (ROOT / record['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
