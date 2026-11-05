"""Both complete original Borland DOSCMD/DOSENV near constructors and OMF."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after340_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after340_work import review

SIZES={'doscmd':311,'dosenv':365}


class OriginalDOSConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-command-environment-build.json')).is_file(),
                         'local 374-member source-bound native receipts absent')
    def test_entire_command_and_environment_near_constructor_pair(self):
        r=review('dos-command-environment')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,374,519))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (676,120849))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],['_malloc','_strlen','__stpcpy'])
                self.assertEqual(len(p['relocation_sites_targets']),5)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'dos-command-environment-build.json')).is_file(),
                         'raw native 374-source DOS constructor vectors absent')
    def test_both_complete_member_programs_identical_original_omf(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'dos-command-environment-build.json')).read_text())
        for name,size in SIZES.items():
            orig=original_library_member(members[NATIVE[name]['index']])
            vendor=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(payload(vendor),payload(orig))
            # Standalone vendor OMF may rearrange FIXUPPs, while library record
            # identity is independently checked against the pinned CL.LIB.
            self.assertEqual(sorted(literal_fields(vendor),key=lambda f:f['site']),
                             sorted(literal_fields(orig),key=lambda f:f['site']))
            for row in rec['rounds']:
                with self.subTest(member=name,round=row['round']):
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
                    self.assertEqual(literal_fields(made),literal_fields(orig))
                    self.assertEqual(object_program_records(made),
                                     members[NATIVE[name]['index']].program_records)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
                    self.assertTrue(row['original_program_equal_by_member'][name])
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
