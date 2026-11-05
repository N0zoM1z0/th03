"""Original Japanese Borland MBCS 10-function complete source-bound CRT family."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after346_work import PREFIX,WORK,MODES,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after346_work import review

SIZES={'MBISALP':32,'MBISDGT':32,'MBISLWR':32,'MBISSPC':32,'MBISUPR':32,
       'MBISL0':44,'MBISL1':44,'MBISLGL':49,'MBTOLWR':29,'MBTOUPR':29}

class OriginalMBCSClassifiers(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'mbcs-classification-leaves-build.json')).is_file(),
                         'native 389-member Japanese source-bound receipt absent')
    def test_all_ten_complete_native_members_and_original_link(self):
        r=review('mbcs-classification-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,389,504))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (355,125396))
        self.assertEqual(set(r['profiles']),set(SIZES))
        self.assertEqual(set(MODES['mbcs-classification-leaves']),set(SIZES))
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

    @unittest.skipUnless((ROOT/(PREFIX+'mbcs-classification-leaves-build.json')).is_file(),
                         'full original/source member OBJ pairs absent')
    def test_original_11_literal_ctype_fixups_in_both_rounds(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'mbcs-classification-leaves-build.json')).read_text())
        originals={}
        for n in SIZES:
            original=original_library_member(members[NATIVE[n]['index']])
            originals[n]=original
            fields=literal_fields(original)
            self.assertEqual([f['addend'] for f in fields],[1]*len(fields))
            self.assertTrue(all((f['frame_method'],f['frame'])==(1,1)
                                for f in fields))
            self.assertEqual([x.data.hex() for x in parse_omf(original)
                              if x.name=='GRPDEF'],['08ff02ff03'])
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    obj=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(obj),payload(original))
                    self.assertEqual(literal_fields(obj),fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(obj),
                                        members[NATIVE[n]['index']].program_records)
        self.assertEqual([f['site'] for f in literal_fields(originals['MBISLGL'])],
                         [33,20])
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
