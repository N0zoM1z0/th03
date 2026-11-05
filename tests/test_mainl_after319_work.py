"""Source-bound native stdiobuf::overflow(int), including honest OMF gap."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after319_work import MODES, PREFIX, WORK
from build_th03_mainl_display_work import literal_fields, payload
from review_th03_mainl_after319_work import review


class OriginalStdiobufOverflow(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).is_file(),
                         'local source-bound 320-member native vectors absent')
    def test_complete_original_overflow_and_native_link(self):
        r = review('stdiobuf-overflow')
        self.assertEqual(MODES['stdiobuf-overflow'], ('sdboflow',))
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 320, 573))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (342, 105180))
        p = r['profiles']['sdboflow']
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (342, 0, 0))
        self.assertEqual(p['publics'], [(0, '@stdiobuf@overflow$qi')])
        self.assertEqual(p['imports'], ['@streambuf@setp$qnct1',
                                        '@streambuf@setg$qnct1t1', '__fputc'])
        self.assertEqual(len(p['relocation_sites_targets']), 4)
        self.assertEqual([f[1] for f in p['relocation_sites_targets']],
                         [142, 214, 273, 307])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).is_file(),
                         'local native OBJ programs absent')
    def test_original_code_and_four_relocations_without_order_normalization(self):
        receipt = json.loads((ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).read_text())
        original = (WORK / 'vendor/sdboflow.obj').read_bytes()
        want_fixups = literal_fields(original)
        self.assertEqual([f['site'] for f in want_fixups], [307, 273, 214, 142])
        for row in receipt['rounds']:
            made = (ROOT / row['outputs']['sdboflow']['path']).read_bytes()
            got_fixups = literal_fields(made)
            self.assertEqual(payload(made), payload(original))
            self.assertEqual([f['site'] for f in got_fixups], [142, 214, 273, 307])
            self.assertEqual(sorted(tuple(sorted(f.items())) for f in got_fixups),
                             sorted(tuple(sorted(f.items())) for f in want_fixups))
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['sdboflow'])


if __name__ == '__main__':
    unittest.main()
