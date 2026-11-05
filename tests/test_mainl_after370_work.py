"""Original Japanese MBCS case-insensitive near/far compare families."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),5000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after370_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after370_work import review

SIZES={'JSTRICMP':247,'FJSTRICM':247,'JSTRNICM':259,'FJSTRNIC':259,
       'MBSICMP':198,'FMBSICMP':198}
SITES={'JSTRICMP':[138,31],'FJSTRICM':[138,31],
       'JSTRNICM':[141,34],'FJSTRNIC':[141,34],
       'MBSICMP':[153,112,82,31],'FMBSICMP':[153,112,82,31]}

class OriginalJapaneseMBCSComparators(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-comparators-build.json')).is_file(),
                         'Japanese 451-source native producer receipts absent')
    def test_six_complete_original_functions_and_full_japanese_link(self):
        r=review('japanese-mbcs-comparators')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,451,442))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1408,143127))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),len(SITES[n]))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-comparators-build.json')).is_file(),
                         'original and native OBJ/MZ vectors absent')
    def test_original_literal_16_byte_table_fixupps_and_mz(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'japanese-mbcs-comparators-build.json')).read_text())
        for n,size in SIZES.items():
            orig=original_library_member(members[NATIVE[n]['index']])
            fields=literal_fields(orig)
            self.assertEqual(len(payload(orig)),size)
            self.assertEqual([f['site'] for f in fields],SITES[n])
            self.assertTrue(all((f['location_type'],f['target_method'],
                                 f['frame_method'],f['frame'],f['addend'])==
                                (1,2,1,1,1) for f in fields))
            for row in rec['rounds']:
                with self.subTest(member=n,native_round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
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
