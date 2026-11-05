"""Original strstreambuf underflow, NEC direct GOTOXY, far strnset."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after424_work import (PREFIX, WORK, NATIVE, MODES,
                                            retained, original_library_member, scope)
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after424_work import review
from lib.pc98 import parse_mz
MODE = 'strstreambuf-nec-and-far-string'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalUnderflowAndHardwareLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound native pair absent')
    def test_complete_three_members_and_native_japanese_link(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 620, 273))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (320, 170101))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'native source member vectors absent')
    def test_original_omf_frames_and_literal_nec_hardware_fixups(self):
        _, _, _, members, carry, _ = retained()
        names = MODES[MODE]
        self.assertEqual(len(names), 3)
        self.assertFalse(set(names) & set(carry[0][0]))
        original = {name: original_library_member(members[NATIVE[name]['index']])
                    for name in names}
        self.assertEqual([(name, NATIVE[name]['code'], NATIVE[name]['fields'])
                          for name in names],
                         [('srbuflow', 188, 2), ('cnecgtxy', 74, 4), ('fstrnset', 58, 2)])
        r = json.loads(RECEIPT.read_text())
        for name in names:
            P = payload(original[name])
            F = literal_fields(original[name])
            self.assertEqual(len(P), NATIVE[name]['code'])
            for record in r['rounds']:
                with self.subTest(name=name, round=record['round']):
                    made = (ROOT / record['outputs'][name]['path']).read_bytes()
                    G = literal_fields(made)
                    self.assertEqual(payload(made), P)
                    self.assertEqual(scope(name, made), scope(name, original[name]))
                    self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in G),
                                     sorted(tuple(f[k] for k in KEYS) for f in F))
                    self.assertEqual(G == F, name == 'cnecgtxy')
                    self.assertEqual(record['literal_omf_fixupp_equal_by_member'][name],
                                     name == 'cnecgtxy')
        for record in r['rounds']:
            exe = (ROOT / record['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
