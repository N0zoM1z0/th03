"""Original Borland 327/325-byte full istream::get/getline implementations."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after357_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after357_work import review

ENTRIES={'istgstr':(327,301,'@istream@get$qncic'),
         'istgline':(325,299,'@istream@getline$qncic')}

class OriginalIstreamInputMethods(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'istream-get-getline-boss-build.json')).is_file(),
                         'local native 410-source original Japanese receipts absent')
    def test_complete_both_input_methods_and_native_exe_map(self):
        r=review('istream-get-getline-boss')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,410,483))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (652,132428))
        self.assertEqual(set(r['profiles']),set(ENTRIES))
        for n,(size,site,name) in ENTRIES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],[(0,name)])
                self.assertEqual(p['imports'],['@ios@setstate$qi','@istream@ipfx$qi'])
                self.assertEqual(len(p['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'istream-get-getline-boss-build.json')).is_file(),
                         'original/compiled native OBJ and EXE pairs absent')
    def test_original_borland_ordered_fixups_at_two_real_far_calls(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'istream-get-getline-boss-build.json')).read_text())
        for name,(size,high,public) in ENTRIES.items():
            orig=original_library_member(members[NATIVE[name]['index']])
            original_fields=literal_fields(orig)
            self.assertEqual([(f['site'],f['target'],f['frame_method'])
                              for f in original_fields],[(high,1,5),(19,2,5)])
            self.assertEqual(len(payload(orig)),size)
            for row in receipt['rounds']:
                with self.subTest(member=name,round=row['round']):
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
                    self.assertEqual(literal_fields(made),original_fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
                    self.assertFalse(row['original_program_equal_by_member'][name])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[name]['index']].program_records)
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
