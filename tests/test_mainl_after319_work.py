"""Scoped Borland stdiobuf overflow original-member/linked-product evidence."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from build_th03_mainl_after319_work import PREFIX, WORK
from review_th03_mainl_after319_work import review
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import parse_omf


class OriginalStdiobufOverflow(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).is_file(),
                         '320-source original Japanese native vectors absent')
    def test_full_member_and_decoded_japanese_product(self):
        record = review('stdiobuf-overflow')
        self.assertEqual((record['original_CRT_members'],
                          record['native_source_members'],
                          record['untouched_vendor_members']), (893, 320, 573))
        self.assertEqual((record['added_CODE_bytes'],
                          record['source_CRT_CODE_bytes']), (342, 105180))
        self.assertEqual(record['original_MZ_relocations'], 677)
        self.assertEqual(record['native_rounds'], 2)
        self.assertTrue(record['complete_original_CODE_DATA_equal'])
        self.assertTrue(record['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(record['original_literal_FIXUPP_equal'])
        self.assertFalse(record['source_acceptance'])
        self.assertFalse(record['original_cold_rebuilt'])
        profile = record['profiles']['sdboflow']
        self.assertEqual((profile['CODE_bytes'], profile['DATA_bytes'],
                          profile['BSS_bytes']), (342, 0, 0))
        self.assertEqual(profile['publics'], [(0, '@stdiobuf@overflow$qi')])
        self.assertEqual(profile['imports'], [
            '@streambuf@setp$qnct1', '@streambuf@setg$qnct1t1', '__fputc'])
        self.assertEqual([x[1] for x in profile['relocation_sites_targets']],
                         [142, 214, 273, 307])

    @unittest.skipUnless((ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).is_file(),
                         'native original member evidence absent')
    def test_all_bytes_and_logical_fixups_but_not_literal_record_order(self):
        receipt = json.loads(
            (ROOT / (PREFIX + 'stdiobuf-overflow-build.json')).read_text())
        original = (WORK / 'vendor/sdboflow.obj').read_bytes()
        group = [r.data.hex() for r in parse_omf(original) if r.name == 'GRPDEF']
        self.assertEqual(group, ['08ff02ff03'])
        for round_record in receipt['rounds']:
            assembled = (ROOT / round_record['outputs']['sdboflow']['path']).read_bytes()
            self.assertEqual(payload(assembled), payload(original))
            self.assertEqual([r.data.hex() for r in parse_omf(assembled)
                              if r.name == 'GRPDEF'], group)
            self.assertEqual(
                sorted(tuple(sorted(f.items())) for f in literal_fields(assembled)),
                sorted(tuple(sorted(f.items())) for f in literal_fields(original)))
            self.assertNotEqual(literal_fields(assembled), literal_fields(original))
            self.assertFalse(
                round_record['literal_omf_fixupp_equal_by_member']['sdboflow'])
