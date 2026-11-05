"""Original Japanese getdcwd + DOS raw-write near error API, full native OMF."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after349_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from build_th03_mainl_resources_work import sha
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after349_work import review

SIZES={'getdcwd':(157,5,[(0,'__getdcwd')]),
       'writea':(91,3,[(0,'__rtl_write'),(63,'__write')])}

class OriginalDOSDirectoryRawWrite(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'directory-and-raw-write-build.json')).is_file(),
                         'two native 395-source original Japanese receipts absent')
    def test_both_complete_original_members_and_full_native_link(self):
        r=review('directory-and-raw-write')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,395,498))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (248,127254))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,(bytes_,fields,pub) in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (bytes_,0,0))
                self.assertEqual(p['publics'],pub)
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),fields)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'directory-and-raw-write-build.json')).is_file(),
                         'original and source OBJ receipt bytes absent')
    def test_actual_original_library_both_omf_rounds_and_struct_include(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'directory-and-raw-write-build.json')).read_text())
        inc='src/mainl/crt/stdio_layout.inc'
        self.assertEqual((record['include_source_path'],record['include_sha256']),
                         (inc,sha((ROOT/inc).read_bytes())))
        for n,(size,cnt,pubs) in SIZES.items():
            orig=original_library_member(members[NATIVE[n]['index']])
            vendor=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(payload(orig),payload(vendor))
            fields=literal_fields(orig)
            self.assertEqual(len(fields),cnt)
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(orig),payload(made))
                    self.assertEqual(fields,literal_fields(made))
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertEqual(row['original_program_equal_by_member'][n], n=='getdcwd')
                    self.assertEqual(object_program_records(made)==
                                     members[NATIVE[n]['index']].program_records,
                                     n=='getdcwd')
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
