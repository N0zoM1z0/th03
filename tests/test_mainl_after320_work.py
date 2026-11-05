"""Complete original Borland filebuf::open, with scoped native raw evidence."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after320_work import PREFIX, WORK
from build_th03_mainl_display_work import literal_fields, payload
from review_th03_mainl_after320_work import review


class OriginalFilebufOpen(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'filebuf-open-build.json')).exists(),
                         'local native original-source receipts absent')
    def test_complete_open_source_and_japanese_link(self):
        r = review('filebuf-open')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 321, 572))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (346, 105526))
        p = r['profiles']['fsbopen']
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (346, 0, 0))
        self.assertEqual(p['publics'], [(0, '@filebuf@open$qnxcii')])
        self.assertEqual(p['imports'], ['_lseek', '_open',
                                        '@streambuf@setp$qnct1',
                                        '@streambuf@setg$qnct1t1'])
        self.assertEqual([f[1] for f in p['relocation_sites_targets']],
                         [122, 176, 293, 327])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'filebuf-open-build.json')).exists(),
                         'native raw OBJ pair unavailable')
    def test_entire_native_payload_and_literal_fixup_order_gap(self):
        record = json.loads((ROOT / (PREFIX + 'filebuf-open-build.json')).read_text())
        original = (WORK / 'vendor/fsbopen.obj').read_bytes()
        expected_fields = literal_fields(original)
        self.assertEqual([f['site'] for f in expected_fields],
                         [327, 293, 176, 122])
        for row in record['rounds']:
            made = (ROOT / row['outputs']['fsbopen']['path']).read_bytes()
            actual_fields = literal_fields(made)
            self.assertEqual(payload(made), payload(original))
            self.assertEqual([f['site'] for f in actual_fields],
                             [122, 176, 293, 327])
            self.assertEqual(sorted(tuple(sorted(f.items())) for f in actual_fields),
                             sorted(tuple(sorted(f.items())) for f in expected_fields))
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['fsbopen'])


if __name__ == '__main__':
    unittest.main()
