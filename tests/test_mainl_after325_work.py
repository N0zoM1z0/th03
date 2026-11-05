"""Borland string::insert(position, string, offset, count): whole native boss."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after325_work import PREFIX, NATIVE, retained, original_library_member, scope
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from review_th03_mainl_after325_work import review


class OriginalStringBoundedInsert(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'string-insert-range-build.json')).is_file(),
                         'complete original 330-member native rounds absent')
    def test_two_segment_bounded_insert_and_entire_japanese_link(self):
        r = review('string-insert-range')
        p = r['profiles']['insert2']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,330,563))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1036,108810))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']), (365,671,1036,30,0))
        self.assertEqual(p['publics'],[(0,'@string@insert$quimx6stringuiui')])
        self.assertEqual(len(p['imports']),12)
        self.assertEqual(len(p['relocation_sites_targets']),43)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),
                         (2,677))

    @unittest.skipUnless((ROOT / (PREFIX + 'string-insert-range-build.json')).is_file(),
                         'raw original/compiled OBJ pairs absent')
    def test_original_library_code_data_and_all_43_relocations(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['insert2']['index']])
        p=scope('insert2',original)
        record=json.loads((ROOT / (PREFIX + 'string-insert-range-build.json')).read_text())
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT / row['outputs']['insert2']['path']).read_bytes()
                self.assertEqual(payload(made),payload(original))
                self.assertEqual(scope('insert2',made),p)
                self.assertNotEqual(literal_fields(made),literal_fields(original))
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['insert2']['index']].program_records)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['insert2'])


if __name__ == '__main__':
    unittest.main()
