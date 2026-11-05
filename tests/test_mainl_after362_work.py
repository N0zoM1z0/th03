"""Six original Borland C++ streambuf/istream/ostream methods, exact native link."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after362_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after362_work import review

SIZES={'stbsgetn':117,'stbsputn':113,'isttellg':120,
       'osttellp':123,'sttie':104,'istws':96}

class OriginalStreamIOMembers(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-io-leaves-build.json')).is_file(),
                         'original Japanese 427-source native rounds absent')
    def test_all_six_complete_original_stream_methods_and_two_links(self):
        r=review('streambuf-io-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,427,466))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (673,136181))
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

    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-io-leaves-build.json')).is_file(),
                         'raw original/source stream OBJ vectors absent')
    def test_all_original_imported_frames_and_ordered_fixup_fields(self):
        _,_,_,members,_,_=retained()
        record=json.loads((ROOT/(PREFIX+'streambuf-io-leaves-build.json')).read_text())
        for n,size in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            fields=literal_fields(original)
            self.assertEqual(len(payload(original)),size)
            if n=='istws':
                self.assertEqual([f['site'] for f in fields],[77,59,45])
                self.assertEqual([f['target'] for f in fields],[1,3,2])
            else:
                self.assertEqual(len(fields),1)
            self.assertTrue(all(f['frame_method']==5 and f['target_method']==2
                                for f in fields))
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(original))
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
