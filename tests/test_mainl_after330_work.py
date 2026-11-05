"""Original 13-API locale character classification module, whole native link."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after330_work import PREFIX, WORK, NATIVE, original_library_member, retained
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after330_work import review

PUBLICS = [
    (0, '___isctype'), (46, '_isalnum'), (68, '_isascii'),
    (91, '_isalpha'), (113, '_iscntrl'), (135, '_isdigit'),
    (157, '_isgraph'), (179, '_islower'), (201, '_isprint'),
    (245, '_ispunct'), (267, '_isspace'), (289, '_isupper'),
    (311, '_isxdigit'),
]


class OriginalBorlandIsctype(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'locale-isctype-family-build.json')).is_file(),
                         'source-bound original 342-member CRT native receipts absent')
    def test_complete_thirteen_api_char_classification_family(self):
        r = review('locale-isctype-family')
        p = r['profiles']['is']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 342, 551))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (333, 112039))
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (333, 0, 0))
        self.assertEqual(p['publics'], PUBLICS)
        self.assertEqual(p['imports'], ['__pLocale'])
        self.assertEqual(p['relocation_sites_targets'], [
            (1, 19, 1, 2, True, 2, 1, 0),
        ])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'locale-isctype-family-build.json')).is_file(),
                         'raw source-produced native isctype OBJ/EXE rounds absent')
    def test_original_complete_333_code_and_literal_dgroup_frame(self):
        _, _, _, members, _, _ = retained()
        original = original_library_member(members[NATIVE['is']['index']])
        receipt = json.loads((ROOT / (PREFIX + 'locale-isctype-family-build.json')).read_text())
        expect_fields = literal_fields(original)
        self.assertEqual(expect_fields, [{
            'segment': 1, 'site': 19, 'location_type': 1, 'width': 2,
            'segment_relative': True, 'frame_method': 1, 'frame': 1,
            'target_method': 2, 'target': 1, 'addend': 0,
        }])
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                made = (ROOT / row['outputs']['is']['path']).read_bytes()
                self.assertEqual(payload(made), payload(original))
                self.assertEqual(literal_fields(made), expect_fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['is'])
                self.assertFalse(row['original_program_equal_by_member']['is'])
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['is']['index']].program_records)
                self.assertEqual([r.data.hex() for r in parse_omf(made)
                                  if r.name == 'GRPDEF'], ['08ff03ff02'])
                exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations), 677)


if __name__ == '__main__':
    unittest.main()
