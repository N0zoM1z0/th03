"""Original complete Borland string::clone with full 328-byte CODE and RTTI."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after382_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after382_work import review

class OriginalStringCloneBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-clone-reference-boss-build.json')).is_file(),
                         'native 488-member original Japanese CRT receipt absent')
    def test_whole_reference_clone_and_full_native_japanese_link(self):
        r=review('string-clone-reference-boss')
        p=r['profiles']['clone']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,488,405))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(328,154610))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(41,287,328,0,0))
        self.assertEqual(p['publics'],[(0,'@string@clone$qv')])
        self.assertEqual(p['imports'],NATIVE['clone']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),12)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-clone-reference-boss-build.json')).is_file(),
                         'original/TASM OBJ vectors and complete Japanese MZ rounds absent')
    def test_original_12_fixups_and_three_typed_rtti(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['clone']['index']]
        self.assertEqual(m.name,'clone')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),328)
        self.assertEqual(code_publics(original,4),[(0,'@string@clone$qv')])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['0aff02ff03'])
        self.assertEqual(len(F),12)
        self.assertEqual([f['site'] for f in F if f['segment']==1],[39,5])
        sites=[f['site'] for f in F if f['segment']==4]
        self.assertEqual(len(sites),10)
        self.assertEqual(sites,sorted(sites,reverse=True))
        for off,fragment in ((158,b'TStringRef *\0'),(209,b'TStringRef\0\0'),
                             (267,b'TReference\0\0')):
            self.assertEqual(bytes(P[4,i] for i in range(off,off+len(fragment))),fragment)
        rec=json.loads((ROOT/(PREFIX+'string-clone-reference-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['clone']['path']).read_bytes()
                self.assertEqual(payload(made),P)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['clone'])
                self.assertFalse(row['original_program_equal_by_member']['clone'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
