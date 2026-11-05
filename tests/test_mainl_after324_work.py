"""Five complete original Borland x86 rotation, multiply and block-copy leaves."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after324_work import PREFIX, WORK, MODES
from build_th03_mainl_display_work import literal_fields, payload
from lib.omf import parse_omf
from review_th03_mainl_after324_work import review

MEMBERS = {
    'crotl': (15, [(0, '__crotl')]),
    'crotr': (15, [(0, '__crotr')]),
    'n_lxmul': (23, [(0, 'N_LXMUL@')]),
    'n_scopy': (28, [(0, 'N_SCOPY@')]),
    'f_scopy': (28, [(0, 'F_SCOPY@'), (0, 'SCOPY@')]),
}


class Original8086Leaves(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'assembler-leaves-build.json')).exists(),
                         'local 329-source native receipts absent')
    def test_all_five_native_members_and_complete_japanese_link(self):
        r = review('assembler-leaves')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 329, 564))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (109, 107774))
        self.assertEqual(set(r['profiles']), set(MEMBERS))
        self.assertEqual(set(MODES['assembler-leaves']), set(MEMBERS))
        for n, (size, public) in MEMBERS.items():
            with self.subTest(member=n):
                p = r['profiles'][n]
                self.assertEqual((p['CODE_bytes'], p['DATA_bytes'],
                                  p['BSS_bytes']), (size, 0, 0))
                self.assertEqual(p['publics'], public)
                self.assertEqual(p['imports'], [])
                self.assertEqual(p['relocation_sites_targets'], [])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'assembler-leaves-build.json')).exists(),
                         'raw original and compiled OBJ programs absent')
    def test_full_original_payloads_and_empty_fixup_inventories(self):
        record = json.loads((ROOT / (PREFIX + 'assembler-leaves-build.json')).read_text())
        for n in MEMBERS:
            original = (WORK / 'vendor' / (n + '.obj')).read_bytes()
            self.assertEqual(literal_fields(original), [])
            self.assertEqual([x.data.hex() for x in parse_omf(original)
                              if x.name == 'GRPDEF'], ['06ff02'])
            for round_record in record['rounds']:
                with self.subTest(member=n, round=round_record['round']):
                    made = (ROOT / round_record['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made), payload(original))
                    self.assertEqual(literal_fields(made), [])
                    self.assertEqual([x.data.hex() for x in parse_omf(made)
                                      if x.name == 'GRPDEF'], ['06ff02'])
                    self.assertTrue(
                        round_record['literal_omf_fixupp_equal_by_member'][n])


if __name__ == '__main__':
    unittest.main()
