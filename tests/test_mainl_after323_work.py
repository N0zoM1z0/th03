"""Original Japanese Borland string::insert boss: complete CODE, DATA and RTTI."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after323_work import PREFIX, NATIVE, retained, original_library_member, scope
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from review_th03_mainl_after323_work import review


class OriginalStringInsertBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'string-insert-boss-build.json')).exists(),
                         'local 324-source original insert native receipts absent')
    def test_full_two_code_segment_exception_boss(self):
        r = review('string-insert-boss')
        p = r['profiles']['insert1']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,324,569))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (960,107665))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']), (365,595,960,30,0))
        self.assertEqual(p['publics'], [(0,'@string@insert$quimx6string')])
        self.assertEqual(len(p['imports']),12)
        self.assertEqual(len(p['relocation_sites_targets']),43)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT / (PREFIX + 'string-insert-boss-build.json')).exists(),
                         'raw original code/data vectors absent')
    def test_real_library_object_and_both_independent_source_outputs(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['insert1']['index']])
        record=json.loads((ROOT / (PREFIX + 'string-insert-boss-build.json')).read_text())
        p=scope('insert1',original)
        self.assertEqual(p['DATA_bytes'],30)
        for row in record['rounds']:
            made=(ROOT / row['outputs']['insert1']['path']).read_bytes()
            self.assertEqual(payload(made),payload(original))
            self.assertEqual(scope('insert1',made),p)
            self.assertNotEqual(object_program_records(made),
                                members[NATIVE['insert1']['index']].program_records)
            self.assertNotEqual(literal_fields(made),literal_fields(original))
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['insert1'])

if __name__=='__main__':
    unittest.main()
