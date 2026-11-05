"""Six complete original Borland istream bulk/ignore/get/putback methods."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after366_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after366_work import review

SIZES={'istread':287,'istign':272,'istgpchr':274,
       'istgschr':274,'istguchr':274,'istpback':205}
SITES={'istread':[268,19],'istign':[253,19],
       'istgpchr':[255,229,19],'istgschr':[255,229,19],
       'istguchr':[255,229,19],'istpback':[186,155]}

class OriginalIstreamBatch(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'istream-read-ignore-get-putback-build.json')).is_file(),
                         'native original 438-member Japanese receipts absent')
    def test_six_complete_members_and_original_native_link(self):
        r=review('istream-read-ignore-get-putback')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,438,455))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1586,139421))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),NATIVE[n]['fields'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'istream-read-ignore-get-putback-build.json')).is_file(),
                         'actual original and native OBJ/EXE pairs absent')
    def test_original_imported_relocations_literal_order_and_mz(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'istream-read-ignore-get-putback-build.json')).read_text())
        for n,size in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            fields=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual([f['site'] for f in fields],SITES[n])
            self.assertTrue(all(f['frame_method']==5 and f['target_method']==2
                                and f['location_type']==3 for f in fields))
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
