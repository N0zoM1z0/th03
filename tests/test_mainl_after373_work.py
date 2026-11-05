"""Full original Borland string::append(string&,ui,ui) and 20 ordered OMF fixes."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after373_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after373_work import review

class OriginalStringAppendSliceBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-append-slice-boss-build.json')).is_file(),
                         'original 459-source Japanese native receipt absent')
    def test_full_append_exception_cleanup_and_native_japanese_link(self):
        r=review('string-append-slice-boss')
        p=r['profiles']['append1']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,459,434))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(578,145663))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(177,401,578,0,0))
        self.assertEqual(p['publics'],[(0,'@string@append$qmx6stringuiui')])
        self.assertEqual(p['imports'],NATIVE['append1']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),20)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-append-slice-boss-build.json')).is_file(),
                         'original and produced native OMF/MZ vectors absent')
    def test_original_20_ordered_relocs_and_three_typed_exception_rtti(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['append1']['index']]
        self.assertEqual(m.name,'append1')
        original=original_library_member(m)
        po=payload(original)
        self.assertEqual(len(po),578)
        self.assertEqual(code_publics(original,4),[(0,'@string@append$qmx6stringuiui')])
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        F=literal_fields(original)
        self.assertEqual(len(F),20)
        for seg,count in ((1,9),(4,11)):
            positions=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(positions),count)
            self.assertEqual(positions,sorted(positions,reverse=True))
        for off,text in ((239,b'string::lengtherror\0'),(317,b'xalloc\0\0'),
                         (383,b'xmsg\0\0')):
            self.assertEqual(bytes(po[4,i] for i in range(off,off+len(text))),text)
        rec=json.loads((ROOT/(PREFIX+'string-append-slice-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['append1']['path']).read_bytes()
                self.assertEqual(payload(made),po)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['append1'])
                self.assertFalse(row['original_program_equal_by_member']['append1'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
