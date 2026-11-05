"""Original fullpath DOS/DBCS algorithm and real native library provenance."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after322_work import (
    PREFIX, WORK, NATIVE, original_library_member, retained, scope)
from build_th03_mainl_display_work import literal_fields, payload
from lib.borland_library import object_program_records
from review_th03_mainl_after322_work import review


class FullpathOriginalNative(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'dos-fullpath-build.json')).is_file(),
                         'local 323-member source-bound receipt unavailable')
    def test_complete_834_byte_algorithm_and_two_native_links(self):
        r = review('dos-fullpath')
        p = r['profiles']['fullpath']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 323, 570))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (834, 106705))
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (834, 0, 0))
        self.assertEqual(p['publics'], [(89, '__fullpath')])
        self.assertEqual(p['imports'], ['__ctype', '_toupper', '__getdcwd',
            '__dos_getdrive', '_free', '_malloc', '_realloc', '_strcpy',
            '_strlen', '___path_isdbcsleadbyte', '___path_issbcs'])
        self.assertEqual(len(p['relocation_sites_targets']), 18)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'dos-fullpath-build.json')).is_file(),
                         'raw fullpath carrier artifacts unavailable')
    def test_library_member_not_assumed_equal_to_standalone_vendor_obj(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['fullpath']['index']]
        self.assertEqual(m.name, 'fullpath')
        original = original_library_member(m)
        vendor = (WORK / 'vendor/fullpath.obj').read_bytes()
        self.assertNotEqual(object_program_records(vendor), m.program_records)
        self.assertEqual(scope('fullpath', vendor), scope('fullpath', original))
        self.assertNotEqual(literal_fields(vendor), literal_fields(original))
        record = json.loads((ROOT / (PREFIX + 'dos-fullpath-build.json')).read_text())
        for row in record['rounds']:
            made = (ROOT / row['outputs']['fullpath']['path']).read_bytes()
            self.assertEqual(payload(original), payload(made))
            self.assertEqual(literal_fields(original), literal_fields(made))
            # Native source-bound TASM timestamp gives the exact original member.
            self.assertEqual(object_program_records(made), m.program_records)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fullpath'])


if __name__ == '__main__':
    unittest.main()
