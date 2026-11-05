"""Complete original Borland locale-aware near/far case and collate members."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after339_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.omf import parse_omf
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after339_work import review

SIZES={'lstrcoll':33,'lstrxfrm':36,'ltolower':43,'ltoupper':43,
       'lstrlwr':47,'lstrupr':47,'ftolower':48,'ftoupper':48}


class EightOriginalLocaleCaseLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'locale-string-case-leaves-build.json')).is_file(),
                         'local native 372-source original Japanese receipts absent')
    def test_all_eight_original_complete_code_and_native_link(self):
        r=review('locale-string-case-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,372,521))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (345,120173))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),1)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'locale-string-case-leaves-build.json')).is_file(),
                         'raw 8 source/native OBJ pairs unavailable')
    def test_full_original_near_far_locale_and_ctype_frames(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'locale-string-case-leaves-build.json')).read_text())
        for n in SIZES:
            original=original_library_member(members[NATIVE[n]['index']])
            orig_fields=literal_fields(original)
            self.assertEqual(len(orig_fields),1)
            if n in ('lstrlwr','lstrupr'):
                self.assertEqual(orig_fields[0]['frame_method'],5)
                self.assertEqual(NATIVE[n]['group'],'08ff03ff02')
            else:
                self.assertEqual((orig_fields[0]['frame_method'],orig_fields[0]['frame']),
                                 (1,1))
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),orig_fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
                    self.assertEqual([x.data.hex() for x in parse_omf(made)
                                      if x.name=='GRPDEF'],[NATIVE[n]['group']])
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
