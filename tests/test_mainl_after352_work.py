"""Five complete Japanese DOS drive/find/lock/date native CRT wrappers."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after352_work import PREFIX, WORK, NATIVE, retained, original_library_member, source_equivalent
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after352_work import review

SIZES={'chdrive':(84,3,[(0,'__chdrive'),(55,'__getdrive')]),
       'dosfind':(104,2,[(0,'__dos_findfirst'),(55,'__dos_findnext')]),
       'doslock':(78,2,[(0,'__dos_lock'),(39,'__dos_unlock')]),
       'dossdate':(92,2,[(0,'__dos_setdate'),(44,'__dos_settime')]),
       'findfirs':(104,2,[(0,'_findfirst'),(55,'_findnext')])}


class OriginalDOSDriveFindLockDate(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-drive-find-lock-date-build.json')).is_file(),
                         'original Japanese 403-source native receipts unavailable')
    def test_five_complete_original_members_and_full_native_link(self):
        r=review('dos-drive-find-lock-date')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,403,490))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (462,129234))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,(size,fixes,pubs) in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],pubs)
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),fixes)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'dos-drive-find-lock-date-build.json')).is_file(),
                         'original/source OBJ pairs and linked MZ receipts absent')
    def test_literal_four_members_and_explicit_two_doslock_frame_gaps(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'dos-drive-find-lock-date-build.json')).read_text())
        for n in SIZES:
            orig=original_library_member(members[NATIVE[n]['index']])
            old=literal_fields(orig)
            self.assertEqual(len(old),NATIVE[n]['fields'])
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
                    self.assertTrue(source_equivalent(n,made,orig))
                    mf=literal_fields(made)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],
                                     n!='doslock')
                    self.assertEqual(mf==old,n!='doslock')
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
                    if n=='doslock':
                        aa={f['site']:f for f in old}
                        bb={f['site']:f for f in mf}
                        self.assertEqual(set(aa),{29,68})
                        for site in (29,68):
                            self.assertEqual((aa[site]['frame_method'],aa[site]['frame']),
                                             (5,None))
                            self.assertEqual((bb[site]['frame_method'],bb[site]['frame']),
                                             (0,1))
                            for k in ('segment','site','location_type','width','target_method','target','addend'):
                                self.assertEqual(aa[site][k],bb[site][k])
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
