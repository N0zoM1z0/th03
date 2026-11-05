"""Original Japanese DBCS-aware Borland cgets and near erase helper."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after336_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after336_work import review


class OriginalDBCSCgets(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'cgets-dbcs-console-build.json')).is_file(),
                         'scoped native original cgets receipt absent')
    def test_complete_pc98_multibyte_console_original_and_native_link(self):
        r=review('cgets-dbcs-console')
        p=r['profiles']['cgets']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,362,531))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (347,118024))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (347,0,0))
        self.assertEqual(p['publics'],[(35,'_cgets')])
        self.assertEqual(p['imports'],['__wkanji','_getch','_putch',
                                       '__mbctype','__mbsbtype','___conio_type'])
        self.assertEqual(len(p['relocation_sites_targets']),11)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'cgets-dbcs-console-build.json')).is_file(),
                         'raw original/compiled cgets OBJ unavailable')
    def test_full_native_omf_fields_and_original_near_backspace_logic(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cgets']['index']]
        self.assertEqual(m.name,'cgets')
        original=original_library_member(m)
        old=payload(original)
        old_fields=literal_fields(original)
        self.assertEqual(len(old_fields),11)
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual([p for p in range(347) if (1,p) not in old],[])
        for off in (123,166,258,272):
            f=next(f for f in old_fields if f['site']==off)
            self.assertEqual((f['frame_method'],f['frame']), (1,1))
        self.assertEqual(next(f['addend'] for f in old_fields if f['site']==272),1)
        rec=json.loads((ROOT/(PREFIX+'cgets-dbcs-console-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['cgets']['path']).read_bytes()
                self.assertEqual(payload(made),old)
                fields=literal_fields(made)
                self.assertEqual(sorted(fields,key=lambda f:(f['segment'],f['site'])),
                                 sorted(old_fields,key=lambda f:(f['segment'],f['site'])))
                self.assertNotEqual(fields,old_fields)
                self.assertNotEqual(object_program_records(made),m.program_records)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['cgets'])
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
