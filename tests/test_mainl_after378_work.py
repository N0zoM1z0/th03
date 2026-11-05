"""Full original Borland C++ string constructor, 716 CODE and 22 literal fixes."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after378_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after378_work import review

class OriginalTSubStringConstructorBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-tsubstring-constructor-boss-build.json')).is_file(),
                         'native source-bound Japanese 475-member receipts absent')
    def test_complete_original_constructor_exception_and_two_native_links(self):
        r=review('string-tsubstring-constructor-boss')
        p=r['profiles']['ctor6']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,475,418))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (621,151008))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(126,495,621,0,0))
        self.assertEqual(p['publics'],[(0,'@string@$bctr$qmx10TSubString')])
        self.assertEqual(p['imports'],NATIVE['ctor6']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),22)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-tsubstring-constructor-boss-build.json')).is_file(),
                         'raw original and native TASM OBJ/MZ vectors absent')
    def test_original_22_ordered_relocs_five_rtti_and_full_japanese_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['ctor6']['index']]
        self.assertEqual(m.name,'ctor6')
        o=original_library_member(m)
        po=payload(o)
        self.assertEqual(len(po),621)
        self.assertEqual(code_publics(o,4),[(0,'@string@$bctr$qmx10TSubString')])
        self.assertEqual([x.data.hex() for x in parse_omf(o) if x.name=='GRPDEF'],
                         ['0aff02ff03'])
        F=literal_fields(o)
        self.assertEqual(len(F),22)
        for seg,count in ((1,7),(4,15)):
            sites=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for off,bs in ((244,b'TStringRef *\0'),(295,b'xalloc\0\0'),
                       (361,b'xmsg\0\0'),(417,b'TStringRef\0\0'),
                       (475,b'TReference\0\0')):
            self.assertEqual(bytes(po[4,i] for i in range(off,off+len(bs))),bs)
        rec=json.loads((ROOT/(PREFIX+'string-tsubstring-constructor-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(native_round=row['round']):
                made=(ROOT/row['outputs']['ctor6']['path']).read_bytes()
                self.assertEqual(payload(made),po)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['ctor6'])
                self.assertFalse(row['original_program_equal_by_member']['ctor6'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
