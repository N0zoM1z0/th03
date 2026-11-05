"""Original 5-API 1379-byte Borland string find/substring boss and native link."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after351_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after351_work import review

PUBS = [(0, '@string@substring$qnxcui'),
        (181, '@string@substring$xqnxcui'),
        (402, '@string@find$xqmx6stringui'),
        (473, '@string@find_index$xqnxcuimui'),
        (684, '@string@find_case_index$xqnxcuimui')]


class OriginalFind1Boss(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'string-find-boss-build.json')).is_file(),
                         'original native 398-member find1 receipt unavailable')
    def test_complete_five_api_original_and_two_exact_links(self):
        r = review('string-find-boss')
        p = r['profiles']['find1']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 398, 495))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (1379, 128772))
        self.assertEqual((p['TEXT_bytes'], p['TEXTC_bytes'], p['CODE_bytes'],
                          p['DATA_bytes'], p['BSS_bytes']), (83, 1296, 1379, 0, 0))
        self.assertEqual(p['publics'], PUBS)
        self.assertEqual(p['imports'], NATIVE['find1']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']), 52)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'string-find-boss-build.json')).is_file(),
                         'both original source-bound native OBJ/EXE rounds unavailable')
    def test_entire_52_literal_original_fixupp_frames_rtti_and_mz_order(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['find1']['index']]
        self.assertEqual(m.name, 'find1')
        original = original_library_member(m)
        orig_payload = payload(original)
        fields = literal_fields(original)
        self.assertEqual(len(fields), 52)
        self.assertEqual(code_publics(original, 4), PUBS)
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name == 'GRPDEF'], ['0aff02ff03'])
        self.assertEqual([f['site'] for f in fields if f['segment'] == 1],
                         [81, 55, 45, 35, 29, 19, 9])
        for start, end, expected_count in ((0, 1024, 38), (1024, 1296, 7)):
            positions = [f['site'] for f in fields
                         if f['segment'] == 4 and start <= f['site'] < end]
            self.assertEqual(len(positions), expected_count)
            self.assertEqual(positions, sorted(positions, reverse=True))
        for site, addend in ((12, 9), (193, 19), (414, 29), (485, 69)):
            f = next(f for f in fields if f['segment'] == 4 and f['site'] == site)
            self.assertEqual((f['target_method'], f['target'], f['addend']), (0, 1, addend))
        self.assertEqual(bytes(orig_payload[4, i] for i in (51, 272)), b'\xff\xff')
        receipt = json.loads((ROOT / (PREFIX + 'string-find-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(native_round=row['round']):
                made = (ROOT / row['outputs']['find1']['path']).read_bytes()
                self.assertEqual(payload(made), orig_payload)
                self.assertEqual(literal_fields(made), fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['find1'])
                self.assertFalse(row['original_program_equal_by_member']['find1'])
                self.assertNotEqual(object_program_records(made), m.program_records)
                exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations), 677)


if __name__ == '__main__':
    unittest.main()
