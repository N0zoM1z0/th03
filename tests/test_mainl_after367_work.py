"""Five full Borland istream get/extraction and whitespace-classification APIs."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after367_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after367_work import review

SIZES={'istget':190,'istepchr':246,'isteschr':246,'isteuchr':246,'isteatwh':234}
SITES={'istget':[158,19],'istepchr':[222,18],
       'isteschr':[222,18],'isteuchr':[222,18],'isteatwh':[221,190]}

class OriginalIstreamExtract(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'istream-extract-eatwhite-build.json')).is_file(),
                         'local 443-member Japanese original native receipt absent')
    def test_five_complete_original_functions_and_native_link(self):
        r=review('istream-extract-eatwhite')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,443,450))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1162,140583))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'istream-extract-eatwhite-build.json')).is_file(),
                         'raw original/source OBJ and Japanese link vectors absent')
    def test_original_far_calls_and_ctype_table_fixup_order(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'istream-extract-eatwhite-build.json')).read_text())
        for n,size in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            F=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual([f['site'] for f in F],SITES[n])
            if n=='isteatwh':
                self.assertEqual((F[1]['location_type'],F[1]['target_method'],
                                  F[1]['target'],F[1]['frame_method'],F[1]['addend']),
                                 (1,2,2,1,1))
            else:
                self.assertTrue(all(f['location_type']==3 and f['frame_method']==5
                                    and f['target_method']==2 for f in F))
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
