"""Full original Borland string(char*,ui,ui) constructor and typed RTTI."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after379_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after379_work import review

class OriginalCStringRangeConstructor(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-cstr-range-constructor-boss-build.json')).is_file(),
                         'native 476-member Japanese original CRT receipt absent')
    def test_complete_constructor_exception_and_original_native_link(self):
        r=review('string-cstr-range-constructor-boss')
        p=r['profiles']['ctor4']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,476,417))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(811,151819))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(207,604,811,0,0))
        self.assertEqual(p['publics'],[(0,'@string@$bctr$qnxcuiui')])
        self.assertEqual(p['imports'],NATIVE['ctor4']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),29)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-cstr-range-constructor-boss-build.json')).is_file(),
                         'both native original/source OBJ/LIB/EXE/MAP vectors unavailable')
    def test_exact_29_borland_fixups_six_typed_rtti_and_mz_order(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['ctor4']['index']]
        self.assertEqual(m.name,'ctor4')
        o=original_library_member(m);P=payload(o);F=literal_fields(o)
        self.assertEqual(len(P),811)
        self.assertEqual(code_publics(o,4),[(0,'@string@$bctr$qnxcuiui')])
        self.assertEqual([x.data.hex() for x in parse_omf(o) if x.name=='GRPDEF'],
                         ['0aff02ff03'])
        self.assertEqual(len(F),29)
        for seg,count in ((1,11),(4,18)):
            sites=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for off,fragment in ((275,b'TStringRef *\0'),(326,b'string::lengtherror\0'),
                             (404,b'xalloc\0\0'),(470,b'xmsg\0\0'),
                             (526,b'TStringRef\0\0'),(584,b'TReference\0\0')):
            self.assertEqual(bytes(P[4,i] for i in range(off,off+len(fragment))),fragment)
        rec=json.loads((ROOT/(PREFIX+'string-cstr-range-constructor-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['ctor4']['path']).read_bytes()
                self.assertEqual(payload(made),P)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['ctor4'])
                self.assertFalse(row['original_program_equal_by_member']['ctor4'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
