"""Complete original 317-byte Borland C++ string::strip with literal OMF."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after358_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after358_work import review


class OriginalStringStripBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-strip-boss-build.json')).is_file(),
                         'source-bound original 411-member native receipt absent')
    def test_complete_original_string_trim_and_full_japanese_link(self):
        r=review('string-strip-boss')
        p=r['profiles']['strip']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,411,482))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (317,132745))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(5,312,317,0,0))
        self.assertEqual(p['publics'],[(0,'@string@strip$q16string@StripTypec')])
        self.assertEqual(p['imports'],['@$bnew$qui','@__RefDestructorCount$qv'])
        self.assertEqual(len(p['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-strip-boss-build.json')).is_file(),
                         'original/source OBJ and native link pairs absent')
    def test_borland_refcount_new_and_original_literal_fixupp_order(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['strip']['index']]
        self.assertEqual(m.name,'strip')
        orig=original_library_member(m)
        old=payload(orig)
        self.assertEqual(len(old),317)
        self.assertEqual([old[1,i] for i in range(5)],[0x56,0x57,0x5f,0x5e,0xcb])
        fields=literal_fields(orig)
        self.assertEqual([(f['segment'],f['site'],f['target_method'],f['target'],f['frame_method'])
                          for f in fields],[(4,249,2,1,5),(4,110,2,1,5)])
        receipt=json.loads((ROOT/(PREFIX+'string-strip-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                obj=(ROOT/row['outputs']['strip']['path']).read_bytes()
                self.assertEqual(payload(obj),old)
                self.assertEqual(literal_fields(obj),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['strip'])
                self.assertFalse(row['original_program_equal_by_member']['strip'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
