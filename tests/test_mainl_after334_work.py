"""Eight complete original Japanese path, file and ostream CRT utilities."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after334_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after334_work import review

MEMBERS={'mkdir':28,'rmdir':28,'tell':28,'umask':25,
         'ostendl':43,'ostends':32,'ostmflsh':28,'fsetpos':36}
ORDER_GAPS={'umask','ostendl'}


class OriginalStreamPathLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'stream-path-leaves-build.json')).is_file(),
                         'native 360-member original Japanese receipt absent')
    def test_complete_eight_original_source_members_and_native_link(self):
        r=review('stream-path-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,360,533))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (248,115155))
        self.assertEqual(set(r['profiles']),set(MEMBERS))
        for n,size in MEMBERS.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),NATIVE[n]['fields'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'stream-path-leaves-build.json')).is_file(),
                         'native source / original OMF pairs absent')
    def test_original_omf_fields_and_two_native_output_rounds(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'stream-path-leaves-build.json')).read_text())
        for n in MEMBERS:
            original=original_library_member(members[NATIVE[n]['index']])
            orig_payload=payload(original)
            orig_fields=literal_fields(original)
            self.assertEqual(len(orig_fields),NATIVE[n]['fields'])
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    fields=literal_fields(made)
                    self.assertEqual(payload(made),orig_payload)
                    self.assertEqual(sorted(orig_fields,key=lambda f:(f['segment'],f['site'])),
                                     sorted(fields,key=lambda f:(f['segment'],f['site'])))
                    self.assertEqual(fields==orig_fields,n not in ORDER_GAPS)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],
                                     n not in ORDER_GAPS)
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
                    group=[f.data.hex() for f in parse_omf(made) if f.name=='GRPDEF']
                    self.assertEqual(group,[NATIVE[n]['group']])
        self.assertEqual([f['site'] for f in literal_fields(original_library_member(
                         members[NATIVE['umask']['index']]))],[17,7])
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
