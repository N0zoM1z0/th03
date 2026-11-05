"""Two complete original Japanese Borland 16:16 huge-pointer arithmetic members."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after354_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after354_work import review

SIZES={'h_pada':(136,[(0,'N_PADA@'),(3,'F_PADA@'),(3,'PADA@'),
                       (68,'N_PSBA@'),(71,'F_PSBA@'),(71,'PSBA@')]),
       'h_pina':(102,[(0,'N_PINA@'),(3,'F_PINA@'),(3,'PINA@'),
                       (50,'N_PDEA@'),(53,'F_PDEA@'),(53,'PDEA@')])}


class OriginalHugePointerArithmetic(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'huge-pointer-adjustments-build.json')).is_file(),
                         'native 406-source original Japanese CRT receipt absent')
    def test_entire_near_far_huge_pointer_apis_and_native_link(self):
        r=review('huge-pointer-adjustments')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,406,487))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (238,130443))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,(size,pubs) in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],pubs)
                self.assertEqual(p['imports'],[])
                self.assertEqual(p['relocation_sites_targets'],[])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'huge-pointer-adjustments-build.json')).is_file(),
                         'raw native original/source OBJ vectors absent')
    def test_all_12_original_aliases_and_two_exact_mz_rounds(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'huge-pointer-adjustments-build.json')).read_text())
        for n,(size,publics) in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            self.assertEqual(len(payload(original)),size)
            self.assertEqual(literal_fields(original),[])
            for row in receipt['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),[])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
