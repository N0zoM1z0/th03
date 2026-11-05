"""Six complete original Japanese near/far MBCS string span and compare APIs."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),5000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after372_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after372_work import review

SIZES={'MBSCSPN':194,'FMBSCSPN':194,'MBSSPN':194,
       'FMBSSPN':194,'MBSNCMP':180,'FMBSNCMP':180}
SITES={'MBSCSPN':[145,49],'FMBSCSPN':[145,49],
       'MBSSPN':[145,49],'FMBSSPN':[145,49],
       'MBSNCMP':[99,34],'FMBSNCMP':[99,34]}

class OriginalJapaneseDBCSStringSpanFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-span-and-length-build.json')).is_file(),
                         'native source-bound Japanese 458-member receipts absent')
    def test_six_entire_multibyte_members_and_original_link(self):
        r=review('japanese-mbcs-span-and-length')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,458,435))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1136,145085))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for name,size in SIZES.items():
            with self.subTest(member=name):
                p=r['profiles'][name]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[name]['publics'])
                self.assertEqual(p['imports'],['__mbctype'])
                self.assertEqual(len(p['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-span-and-length-build.json')).is_file(),
                         'original/source OMF and Japanese EXE vectors absent')
    def test_all_12_literal_original_byte_table_fixupps_and_mz(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'japanese-mbcs-span-and-length-build.json')).read_text())
        for name,size in SIZES.items():
            original=original_library_member(members[NATIVE[name]['index']])
            fields=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual([f['site'] for f in fields],SITES[name])
            self.assertTrue(all((f['location_type'],f['target_method'],
                                 f['frame_method'],f['frame'],f['target'],f['addend'])==
                                (1,2,1,1,1,1) for f in fields))
            for row in rec['rounds']:
                with self.subTest(member=name,round=row['round']):
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
                    self.assertFalse(row['original_program_equal_by_member'][name])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[name]['index']].program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
