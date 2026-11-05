"""Ten complete original near/far MBCS pointer/compare/set routines."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after381_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after381_work import review

SIZES={'MBSNBCMP':198,'FMBSNBCM':198,'MBSSPNP':204,'FMBSSPNP':204,
       'MBSNSET':178,'FMBSNSET':178,'MBCCMP':151,'FMBCCMP':151,
       'MBSDEC':132,'FMBSDEC':132}
SITES={'MBSNBCMP':[111,37],'FMBSNBCM':[111,37],
       'MBSSPNP':[145,49],'FMBSSPNP':[145,49],
       'MBSNSET':[102,53],'FMBSNSET':[102,53],
       'MBCCMP':[89,28],'FMBCCMP':[89,28],
       'MBSDEC':[85,63],'FMBSDEC':[85,63]}

class OriginalMBCSPointerOperations(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-pointer-ops-build.json')).is_file(),
                         'original 487-source Japanese native receipts absent')
    def test_ten_whole_byte_compare_span_set_and_pointer_methods(self):
        r=review('japanese-mbcs-pointer-ops')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,487,406))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1726,154282))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],['__mbctype'])
                self.assertEqual(len(p['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-pointer-ops-build.json')).is_file(),
                         'raw original and TASM member/EXE/MAP receipt pairs absent')
    def test_original_twenty_literal_ctype_fixups_and_full_ordered_mz(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'japanese-mbcs-pointer-ops-build.json')).read_text())
        for n,size in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            F=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual([f['site'] for f in F],SITES[n])
            self.assertTrue(all((f['location_type'],f['target_method'],
                                 f['frame_method'],f['frame'],f['target'],f['addend'])==
                                (1,2,1,1,1,1) for f in F))
            for row in receipt['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
