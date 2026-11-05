"""Source-bound original Japanese 11-method Borland string I/O and typed RTTI."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after330_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after330_work import review

PUB = [
    (0, '@string@read_file$qm7istream'),
    (69, '@string@read_string$qm7istream'),
    (138, '@string@read_line$qm7istream'),
    (292, '@string@read_to_delim$qm7istreamc'),
    (361, '@string@read_token$qm7istream'),
    (427, '@$brsh$qm7istreamm6string'),
    (455, '@$blsh$qm7ostreammx6string'),
    (517, '@getline$qm7istreamm6string'),
    (545, '@getline$qm7istreamm6stringc'),
    (576, '@TStringRef@read_to_delim$qm7istreamc'),
    (805, '@TStringRef@read_token$qm7istream'),
]


class OriginalStringIOBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'stringio-boss-build.json')).is_file(),
                         'local 342-source native evidence is absent')
    def test_all_eleven_full_methods_and_native_image(self):
        r = review('stringio-boss')
        p = r['profiles']['stringio']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 342, 551))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (1466, 113172))
        self.assertEqual((p['TEXT_bytes'], p['TEXTC_bytes'], p['CODE_bytes'],
                          p['DATA_bytes'], p['BSS_bytes']), (110, 1356, 1466, 0, 0))
        self.assertEqual(p['publics'], PUB)
        self.assertEqual(len(p['imports']), 20)
        self.assertEqual(len(p['relocation_sites_targets']), 50)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'stringio-boss-build.json')).is_file(),
                         'original/source native OBJ pair absent')
    def test_all_rtti_code_original_fixups_and_both_ordered_mz_rounds(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['stringio']['index']]
        self.assertEqual(m.name, 'stringio')
        original = original_library_member(m)
        receipt = json.loads((ROOT / (PREFIX + 'stringio-boss-build.json')).read_text())
        orig_fields = literal_fields(original)
        self.assertEqual(len(orig_fields), 50)
        relocs = {(f['segment'], f['site']): f for f in orig_fields}
        # Original native same-segment direct far calls to the full scanners.
        self.assertEqual([(relocs[4, i]['target_method'],
                           relocs[4, i]['target'], relocs[4, i]['addend'])
                          for i in (52, 121, 273, 344, 410)],
                         [(0, 4, 576)] * 4 + [(0, 4, 805)])
        self.assertEqual((relocs[4, 1264]['target'], relocs[4, 1264]['addend']),
                         (1, 33))
        self.assertEqual((relocs[4, 1280]['target'], relocs[4, 1280]['addend']),
                         (4, 1300))
        for row in receipt['rounds']:
            with self.subTest(native_round=row['round']):
                made = (ROOT / row['outputs']['stringio']['path']).read_bytes()
                self.assertEqual(payload(original), payload(made))
                fs = literal_fields(made)
                sorted_fs = lambda vv: sorted(vv, key=lambda f:(f['segment'], f['site']))
                self.assertEqual(sorted_fs(orig_fields), sorted_fs(fs))
                self.assertNotEqual(orig_fields, fs)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['stringio'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                self.assertEqual([r.data.hex() for r in parse_omf(made)
                                  if r.name == 'GRPDEF'], ['0aff02ff03'])
                mz_bytes = (ROOT / row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(mz_bytes, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
                mz = parse_mz(mz_bytes)
                self.assertTrue(mz.valid)
                self.assertEqual(len(mz.relocations), 677)


if __name__ == '__main__':
    unittest.main()
