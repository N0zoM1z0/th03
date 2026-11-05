"""Original stdiobuf(FILE*) constructor: complete CODE, RTTI, vtable and link."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from build_th03_mainl_after321_work import PREFIX, WORK
from review_th03_mainl_after321_work import review
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import parse_omf


class OriginalStdiobufConstructor(unittest.TestCase):
    @unittest.skipUnless(
        (ROOT / (PREFIX + 'stdiobuf-constructor-build.json')).is_file(),
        '322-source native artifact vectors absent')
    def test_complete_member_and_original_japanese_link(self):
        r = review('stdiobuf-constructor')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 322, 571))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (345, 105871))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        p = r['profiles']['sdbctr']
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (345, 52, 0))
        self.assertEqual(p['publics'], [(0, '@stdiobuf@$bctr$qn4FILE')])
        self.assertEqual(len(p['imports']), 19)
        self.assertEqual(len(p['relocation_sites_targets']), 23)
        self.assertEqual([x[1] for x in p['relocation_sites_targets']
                          if x[0] == 2], [0, *range(8, 52, 4)])

    @unittest.skipUnless(
        (ROOT / (PREFIX + 'stdiobuf-constructor-build.json')).is_file(),
        'native raw original sdbctr outputs missing')
    def test_typed_rtti_and_virtual_dispatch_relocations(self):
        receipt = json.loads(
            (ROOT / (PREFIX + 'stdiobuf-constructor-build.json')).read_text())
        original = (WORK / 'vendor/sdbctr.obj').read_bytes()
        original_fields = literal_fields(original)
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name == 'GRPDEF'], ['08ff02ff03'])
        original_payload = payload(original)
        # The extra zero after 'stdiobuf' is a real RTTI field-alignment byte.
        self.assertEqual(bytes(original_payload[1, i] for i in range(255, 265)),
                         b'stdiobuf\x00\x00')
        self.assertEqual(bytes(original_payload[1, i] for i in range(323, 333)),
                         b'streambuf\x00')
        self.assertEqual(bytes(original_payload[2, i] for i in range(4, 8)),
                         bytes(4))
        for row in receipt['rounds']:
            out = (ROOT / row['outputs']['sdbctr']['path']).read_bytes()
            self.assertEqual(payload(out), original_payload)
            self.assertEqual(
                sorted(tuple(sorted(f.items())) for f in literal_fields(out)),
                sorted(tuple(sorted(f.items())) for f in original_fields))
            self.assertNotEqual(literal_fields(out), original_fields)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['sdbctr'])


if __name__ == '__main__':
    unittest.main()
