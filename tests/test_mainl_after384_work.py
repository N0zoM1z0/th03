"""Eleven complete original MBCS count, length, next, copy, inc functions."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after384_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after384_work import review

SIZES={'MBSNCCNT':70,'FMBSNCCN':70,'MBSLEN':57,'FMBSLEN':57,'MBISL2':56,
       'MBSNEXTC':56,'FMBSNEXT':56,'MBSINC':50,'FMBSINC':50,
       'MBCCPY':49,'FMBCCPY':49}
SITES={'MBSNCCNT':25,'FMBSNCCN':25,'MBSLEN':21,'FMBSLEN':21,'MBISL2':40,
       'MBSNEXTC':17,'FMBSNEXT':17,'MBSINC':31,'FMBSINC':31,
       'MBCCPY':26,'FMBCCPY':26}

class OriginalMBCSCountNavigationFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-count-navigation-build.json')).is_file(),
                         'original 500-member Japanese CRT native receipt absent')
    def test_eleven_complete_originals_and_full_native_link(self):
        r=review('japanese-mbcs-count-navigation')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,500,393))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (620,155800))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],['__mbctype'])
                self.assertEqual(len(p['relocation_sites_targets']),1)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-count-navigation-build.json')).is_file(),
                         'source and original OMF/MZ vectors absent')
    def test_original_lead_byte_fixups_for_each_member_and_two_rounds(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'japanese-mbcs-count-navigation-build.json')).read_text())
        for n,size in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            F=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual(len(F),1)
            f=F[0]
            self.assertEqual((f['site'],f['location_type'],f['target_method'],
                              f['target'],f['addend'],f['frame_method'],f['frame']),
                             (SITES[n],1,2,1,1,1,1))
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    obj=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(obj),payload(original))
                    self.assertEqual(literal_fields(obj),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(obj),
                                        members[NATIVE[n]['index']].program_records)
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
