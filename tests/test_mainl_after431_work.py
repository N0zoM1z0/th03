"""Complete strstreambuf default constructor and symbolic vtable slots."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after431_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after431_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE = 'strstreambuf-default-constructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment', 'site', 'location_type', 'width', 'segment_relative',
        'frame_method', 'frame', 'target_method', 'target', 'addend')

class OriginalStrstreambufConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound native constructor receipt absent')
    def test_entire_original_boss_and_native_two_round_link(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 629, 264))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (250, 172332))
        self.assertEqual((r['profiles']['srbctr1']['CODE_bytes'],
                          r['profiles']['srbctr1']['DATA_bytes']), (250, 52))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'source-linked original OBJ absent')
    def test_correct_vtable_slot_symbols_and_nineteen_original_logical_fixups(self):
        _, _, _, members, _, _ = retained()
        member = members[NATIVE['srbctr1']['index']]
        self.assertEqual(member.name, 'srbctr1')
        original = original_library_member(member)
        P = payload(original)
        F = literal_fields(original)
        self.assertEqual(len(P), 302)
        self.assertEqual(len(F), 19)
        self.assertEqual(code_publics(original, 1),
                         [(0, '@strstreambuf@$bctr$qv')])
        self.assertEqual(externs(original), NATIVE['srbctr1']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(52)),
                         bytes.fromhex('7600')+bytes(50))
        by_site = {(f['segment'], f['site']): f for f in F}
        self.assertEqual((by_site[(2, 28)]['target_method'],
                          by_site[(2, 28)]['target']), (2, 7))
        self.assertEqual((by_site[(2, 32)]['target_method'],
                          by_site[(2, 32)]['target']), (2, 11))
        self.assertEqual((by_site[(1, 170)]['target_method'],
                          by_site[(1, 170)]['addend']), (0, 190))
        expected = sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt = json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made = (ROOT / row['outputs']['srbctr1']['path']).read_bytes()
            self.assertEqual(payload(made), P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             expected)
            self.assertNotEqual(literal_fields(made), F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['srbctr1'])
            exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations), 677)

if __name__ == '__main__': unittest.main()
