"""Eight original MBCS near/far append, string-search and case APIs."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after387_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after387_work import review

SIZES={'MBSNCAT':187,'FMBSNCAT':187,'MBSNBCAT':224,'FMBSNBCA':224,
       'MBSSTR':199,'FMBSSTR':199,'FMBSLWR':106,'FMBSUPR':106}
SITES={'MBSNCAT':[97,68],'FMBSNCAT':[97,68],
       'MBSNBCAT':[127,68],'FMBSNBCA':[127,68],
       'MBSSTR':[160,37,15],'FMBSSTR':[160,37,15],
       'FMBSLWR':[66,34],'FMBSUPR':[66,34]}

class OriginalMBCSAppendSearchCase(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-append-search-case-build.json')).is_file(),
                         'source-bound 510-member Japanese CRT receipt absent')
    def test_all_eight_original_code_apis_and_complete_native_link(self):
        r=review('japanese-mbcs-append-search-case')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,510,383))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1432,158551))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for name,size in SIZES.items():
            with self.subTest(member=name):
                p=r['profiles'][name]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[name]['publics'])
                self.assertEqual(p['imports'],NATIVE[name]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),len(SITES[name]))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'japanese-mbcs-append-search-case-build.json')).is_file(),
                         'original and produced raw OBJ/EXE vectors absent')
    def test_original_mixed_far_call_and_ctype_fixup_order(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'japanese-mbcs-append-search-case-build.json')).read_text())
        for name,size in SIZES.items():
            original=original_library_member(members[NATIVE[name]['index']])
            F=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            self.assertEqual([f['site'] for f in F],SITES[name])
            self.assertTrue(any((f['location_type'],f['target_method'],f['frame_method'],f['addend'])
                                ==(1,2,1,1) for f in F))
            if name in ('MBSSTR','FMBSSTR','MBSNCAT','FMBSNCAT','MBSNBCAT','FMBSNBCA'):
                self.assertTrue(any((f['location_type'],f['target_method'],f['frame_method'],f['addend'])
                                    ==(3,2,5,0) for f in F))
            for row in record['rounds']:
                with self.subTest(member=name,round=row['round']):
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
                    self.assertFalse(row['original_program_equal_by_member'][name])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[name]['index']].program_records)
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
