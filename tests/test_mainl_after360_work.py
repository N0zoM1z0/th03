"""Eight complete Borland 16-bit near/far MBCS string routines."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after360_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after360_work import review

SIZES={'MBSISLE':83,'MBSISTR':83,'FMBSISLE':83,'FMBSISTR':83,
       'MBSNBCNT':89,'FMBSNBCN':89,'MBSLWR':106,'MBSUPR':106}

class OriginalMBCSStringFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'mbcs-string-routines-build.json')).is_file(),
                         'native 420-member Japanese CRT source receipt absent')
    def test_eight_complete_original_code_and_japanese_native_exe(self):
        r=review('mbcs-string-routines')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,420,473))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (722,133800))
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

    @unittest.skipUnless((ROOT/(PREFIX+'mbcs-string-routines-build.json')).is_file(),
                         'raw original/source OMF and native link vectors absent')
    def test_all_original_ctype_frames_and_literal_fixupp_order(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'mbcs-string-routines-build.json')).read_text())
        for n,size in SIZES.items():
            orig=original_library_member(members[NATIVE[n]['index']])
            fields=literal_fields(orig)
            expected_sites=[66,34] if n in ('MBSLWR','MBSUPR') else [37] if 'NBCN' in n or n=='MBSNBCNT' else [19]
            self.assertEqual([f['site'] for f in fields],expected_sites)
            self.assertTrue(all((f['frame_method'],f['frame'],f['addend'])==(1,1,1)
                                for f in fields))
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
                    self.assertEqual(literal_fields(made),fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
