"""Ten complete original near/far Japanese MBCS search and compare programs."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after375_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after375_work import review

SIZES={'MBSCMP':168,'FMBSCMP':168,'MBSPBRK':195,'FMBSPBRK':195,
       'MBSRCHR':162,'FMBSRCHR':162,'MBSNBICM':228,'FMBSNBIC':228,
       'MBSNICMP':210,'FMBSNICM':210}
SITES={'MBSCMP':[96,31],'FMBSCMP':[96,31],
       'MBSPBRK':[153,49],'FMBSPBRK':[153,49],
       'MBSRCHR':[30],'FMBSRCHR':[30],
       'MBSNBICM':[177,127,97,37],'FMBSNBIC':[177,127,97,37],
       'MBSNICMP':[156,115,85,34],'FMBSNICM':[156,115,85,34]}

class OriginalMBCSSearchCompareTen(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-search-comparators-build.json')).is_file(),
                         'two original 470-source Japanese native receipts absent')
    def test_all_ten_complete_members_and_exact_native_link(self):
        r=review('japanese-mbcs-search-comparators')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,470,423))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1926,148020))
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

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-search-comparators-build.json')).is_file(),
                         'raw source/original OBJ and Japanese MZ vectors absent')
    def test_all_26_original_byte_table_fields_and_literal_record_order(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'japanese-mbcs-search-comparators-build.json')).read_text())
        for n,size in SIZES.items():
            o=original_library_member(members[NATIVE[n]['index']])
            F=literal_fields(o)
            self.assertEqual(len(payload(o)),size)
            self.assertEqual([f['site'] for f in F],SITES[n])
            self.assertTrue(all((f['location_type'],f['target_method'],
                                 f['frame_method'],f['frame'],f['addend'])==
                                (1,2,1,1,1) for f in F))
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(o))
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
