"""Original complete 737-byte Borland string::copy and seven typed RTTI."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after380_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after380_work import review

class OriginalStringCopyBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-reference-copy-boss-build.json')).is_file(),
                         'source-bound 477-member Japanese native receipt unavailable')
    def test_whole_reference_copy_and_linked_japanese_exe_map(self):
        r=review('string-reference-copy-boss')
        p=r['profiles']['copy3']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,477,416))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(737,152556))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(140,597,737,0,0))
        self.assertEqual(p['publics'],[(0,'@string@copy$xqv')])
        self.assertEqual(p['imports'],NATIVE['copy3']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),27)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-reference-copy-boss-build.json')).is_file(),
                         'original/source raw OBJ and full native linked vectors absent')
    def test_all_27_literal_original_fixupps_and_seven_rtti(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['copy3']['index']]
        self.assertEqual(m.name,'copy3')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),737)
        self.assertEqual(code_publics(original,4),[(0,'@string@copy$xqv')])
        self.assertEqual([r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF'],
                         ['0aff02ff03'])
        self.assertEqual(len(F),27)
        for segment,count in ((1,9),(4,18)):
            sites=[f['site'] for f in F if f['segment']==segment]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for off,txt in ((269,b'TStringRef *\0'),(292,b'string *\0'),
                        (339,b'xalloc\0\0'),(405,b'xmsg\0\0'),
                        (461,b'string\0\0'),(519,b'TStringRef\0\0'),
                        (577,b'TReference\0\0')):
            self.assertEqual(bytes(P[4,i] for i in range(off,off+len(txt))),txt)
        rec=json.loads((ROOT/(PREFIX+'string-reference-copy-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(native_round=row['round']):
                obj=(ROOT/row['outputs']['copy3']['path']).read_bytes()
                self.assertEqual(payload(obj),P)
                self.assertEqual(literal_fields(obj),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['copy3'])
                self.assertFalse(row['original_program_equal_by_member']['copy3'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
