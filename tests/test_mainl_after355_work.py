"""Six complete Borland string/TSubString case methods and typed RTTI."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after355_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after355_work import review

PUBLICS=[(0,'@string@to_lower$qv'),(57,'@string@to_upper$qv'),
         (114,'@to_lower$qmx6string'),(240,'@to_upper$qmx6string'),
         (366,'@TSubString@to_lower$qv'),(512,'@TSubString@to_upper$qv')]

class OriginalUprLwrBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-substring-case-boss-build.json')).is_file(),
                         'native 407-source Japanese C++ proof absent')
    def test_all_six_complete_case_methods_and_original_native_link(self):
        r=review('string-substring-case-boss')
        p=r['profiles']['uprlwr']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,407,486))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (912,131355))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(177,735,912,0,0))
        self.assertEqual(p['publics'],PUBLICS)
        self.assertEqual(p['imports'],NATIVE['uprlwr']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),48)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-substring-case-boss-build.json')).is_file(),
                         'both native exact original/source OMF pairs absent')
    def test_original_exception_frames_pointer_rtti_and_literal_omf_order(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['uprlwr']['index']]
        self.assertEqual(m.name,'uprlwr')
        original=original_library_member(m)
        orig=payload(original)
        self.assertEqual(len(orig),912)
        fields=literal_fields(original)
        self.assertEqual(len(fields),48)
        self.assertEqual([f['site'] for f in fields if f['segment']==1],
                         [171,161,155,147,139,127,113,99,85,79,71,63,51,37,23,9])
        textc=[f['site'] for f in fields if f['segment']==4]
        self.assertEqual(textc,sorted(textc,reverse=True))
        relocs={(f['segment'],f['site']):f for f in fields}
        self.assertEqual((relocs[4,664]['target'],relocs[4,664]['addend']),
                         (4,677))
        self.assertEqual((relocs[4,707]['target_method'],relocs[4,707]['target']),
                         (2,9))
        self.assertEqual(bytes(orig[4,i] for i in range(668,677)),b'string *\0')
        self.assertEqual(orig[4,392],255)
        self.assertEqual(orig[4,538],255)
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['0aff02ff03'])
        rec=json.loads((ROOT/(PREFIX+'string-substring-case-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(native_round=row['round']):
                obj=(ROOT/row['outputs']['uprlwr']['path']).read_bytes()
                self.assertEqual(payload(obj),orig)
                self.assertEqual(literal_fields(obj),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['uprlwr'])
                self.assertFalse(row['original_program_equal_by_member']['uprlwr'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
