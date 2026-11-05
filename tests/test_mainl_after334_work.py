"""Original complete DOS path/offset and C++ ostream manipulator leaf members."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after334_work import NATIVE, PREFIX, WORK, original_library_member, retained
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after334_work import review

MEMBERS = {
    'mkdir': (28, (0, '_mkdir'), ['__IOERROR']),
    'rmdir': (28, (0, '_rmdir'), ['__IOERROR']),
    'tell': (28, (0, '_tell'), ['_lseek']),
    'umask': (25, (0, '_umask'), ['__notUmask']),
    'ostendl': (43, (0, '@endl$qm7ostream'), ['@ostream@flush$qv','@ostream@$blsh$qc']),
    'ostends': (32, (0, '@ends$qm7ostream'), ['@ostream@$blsh$qc']),
    'ostmflsh': (28, (0, '@flush$qm7ostream'), ['@ostream@flush$qv']),
    'fsetpos': (36, (0, '_fsetpos'), ['_fseek']),
}
ORDERED_OMF_GAPS = {'umask', 'ostendl'}


class OriginalStreamPathLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX+'stream-path-leaves-build.json')).is_file(),
                         'source-bound 360 member native receipts not available')
    def test_all_original_functions_and_two_complete_native_rounds(self):
        r = review('stream-path-leaves')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 360, 533))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (248, 115155))
        self.assertEqual(set(r['profiles']), set(MEMBERS))
        for n,(size,publics,imports) in MEMBERS.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'], [publics])
                self.assertEqual(p['imports'],imports)
                self.assertEqual(len(p['relocation_sites_targets']),NATIVE[n]['fields'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']), (2,677))

    @unittest.skipUnless((ROOT / (PREFIX+'stream-path-leaves-build.json')).is_file(),
                         'selected original OBJ/EXE native pair absent')
    def test_original_relocation_frames_and_literal_order_are_not_conflated(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT / (PREFIX+'stream-path-leaves-build.json')).read_text())
        for name in MEMBERS:
            native=NATIVE[name]
            original=original_library_member(members[native['index']])
            fields=literal_fields(original)
            expected_group=native['group']
            for row in receipt['rounds']:
                with self.subTest(member=name,round=row['round']):
                    output=(ROOT/row['outputs'][name]['path']).read_bytes()
                    made=literal_fields(output)
                    self.assertEqual(payload(original),payload(output))
                    self.assertEqual(sorted(fields,key=lambda f:(f['segment'],f['site'])),
                                     sorted(made,key=lambda f:(f['segment'],f['site'])))
                    equal=(name not in ORDERED_OMF_GAPS)
                    self.assertEqual(fields==made,equal)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][name],equal)
                    self.assertEqual([f.data.hex() for f in parse_omf(output)
                                      if f.name=='GRPDEF'],[expected_group])
                    self.assertEqual(row['original_program_equal_by_member'][name],
                        object_program_records(output)==
                        members[native['index']].program_records)
                    self.assertFalse(row['original_program_equal_by_member'][name])
            if name in ORDERED_OMF_GAPS:
                self.assertEqual(len(fields),2)
                self.assertGreater(fields[0]['site'],fields[1]['site'])
        orig=original_library_member(members[NATIVE['umask']['index']])
        self.assertEqual([f['site'] for f in literal_fields(orig)], [17,7])
        for f in literal_fields(orig):
            self.assertEqual((f['frame_method'],f['frame']), (1,1))
        orig=original_library_member(members[NATIVE['ostendl']['index']])
        self.assertEqual([f['site'] for f in literal_fields(orig)], [26,15])
        for f in literal_fields(orig):
            self.assertEqual(f['frame_method'],5)
        # These differences in OMF field order do not change the original MZ order.
        target=(WORK/'bin/th03/mainl.target.exe').read_bytes()
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,target)
            self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
