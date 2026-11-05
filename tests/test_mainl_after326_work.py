"""Two complete original ranged string insert/replace exception bosses."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_after325_work as insert
import build_th03_mainl_after326_work as replace
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from review_th03_mainl_after325_work import review as review_insert
from review_th03_mainl_after326_work import review as review_replace

BOSSES = (
    ('insert2', insert, 'string-insert-range', 671,
     '@string@insert$quimx6stringuiui'),
    ('replace', replace, 'string-replace-boss', 711,
     '@string@replace$quiuimx6stringuiui'),
)


class TwoRangedStringBosses(unittest.TestCase):
    @unittest.skipUnless(
        (ROOT / (insert.PREFIX + 'string-insert-range-build.json')).is_file()
        and (ROOT / (replace.PREFIX + 'string-replace-boss-build.json')).is_file(),
        'two incremental original ranged string member receipts absent')
    def test_two_full_four_segment_bosses_and_331_source_native_product(self):
        r1 = review_insert('string-insert-range')
        r2 = review_replace('string-replace-boss')
        self.assertEqual((r1['native_source_members'], r2['native_source_members']),
                         (330, 331))
        self.assertEqual((r2['original_CRT_members'], r2['native_source_members'],
                          r2['untouched_vendor_members']), (893, 331, 562))
        self.assertEqual((r1['added_CODE_bytes'] + r2['added_CODE_bytes'],
                          r2['source_CRT_CODE_bytes']), (2112, 109886))
        for name, builder, mode, extra, public in BOSSES:
            with self.subTest(member=name):
                r = r1 if name == 'insert2' else r2
                p = r['profiles'][name]
                self.assertEqual((p['TEXT_bytes'], p['TEXTC_bytes'],
                                  p['CODE_bytes'], p['DATA_bytes'],
                                  p['BSS_bytes']), (365, extra, 365+extra, 30, 0))
                self.assertEqual(p['publics'], [(0, public)])
                self.assertEqual(p['imports'], builder.NATIVE[name]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']), 43)
                self.assertEqual(sum(x[0] == 1 for x in p['relocation_sites_targets']), 20)
                self.assertEqual(sum(x[0] == 4 for x in p['relocation_sites_targets']), 23)
                self.assertTrue(r['complete_original_CODE_DATA_equal'])
                self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
                self.assertFalse(r['original_literal_FIXUPP_equal'])
                self.assertFalse(r['original_library_member_program_equal'])
                self.assertFalse(r['source_acceptance'])
                self.assertFalse(r['original_cold_rebuilt'])
                self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                                 (2, 677))

    @unittest.skipUnless(
        (ROOT / (insert.PREFIX + 'string-insert-range-build.json')).is_file()
        and (ROOT / (replace.PREFIX + 'string-replace-boss-build.json')).is_file(),
        'original library members and all four native OBJ rounds unavailable')
    def test_both_original_members_all_code_data_frames_and_rtti(self):
        _, _, _, original_members, _, _ = replace.retained()
        for name, builder, mode, extra, public in BOSSES:
            with self.subTest(member=name):
                original_member = original_members[builder.NATIVE[name]['index']]
                self.assertEqual(original_member.name, name)
                orig = builder.original_library_member(original_member)
                self.assertEqual(object_program_records(orig),
                                 original_member.program_records)
                p = payload(orig)
                self.assertEqual(bytes(p[2, i] for i in range(30)),
                                 b'String reference out of range\0')
                rtti = bytes(p[4, i] for i in range(extra))
                self.assertIn(b'string::lengtherror', rtti)
                self.assertIn(b'string::outofrange', rtti)
                self.assertEqual([x.data.hex() for x in parse_omf(orig)
                                  if x.name == 'GRPDEF'], ['0aff02ff03'])
                fields = {(f['segment'],f['site']): f for f in literal_fields(orig)}
                self.assertEqual(len(fields), 43)
                receipt = json.loads(
                    (ROOT/(builder.PREFIX+mode+'-build.json')).read_text())
                self.assertEqual(len(receipt['rounds']), 2)
                for row in receipt['rounds']:
                    with self.subTest(member=name, round=row['round']):
                        got = (ROOT/row['outputs'][name]['path']).read_bytes()
                        self.assertEqual(payload(got), p)
                        self.assertEqual(
                            {(f['segment'], f['site']):f for f in literal_fields(got)},
                            fields)
                        self.assertNotEqual(object_program_records(got),
                                            original_member.program_records)
                        self.assertNotEqual(literal_fields(got),
                                            literal_fields(orig))
                        self.assertFalse(
                            row['literal_omf_fixupp_equal_by_member'][name])


if __name__=='__main__':
    unittest.main()
