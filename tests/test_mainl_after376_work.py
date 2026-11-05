"""Three full original Borland string::append/prepend C++ exception members."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after376_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after376_work import review

CODE={'append2':(177,329,506),'append3':(177,400,577),
      'prepend':(177,391,568)}
RTTI={'append2':(167,245,311),'append3':(238,316,382),
      'prepend':(229,307,373)}

class OriginalAppendPrependFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-append-prepend-bosses-build.json')).is_file(),
                         'native 473-source Japanese CRT receipts absent')
    def test_three_complete_borland_cxx_methods_and_native_full_link(self):
        r=review('string-append-prepend-bosses')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,473,420))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1651,149671))
        self.assertEqual(set(r['profiles']),set(CODE))
        for n,(seg1,seg4,total) in CODE.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                                  p['DATA_bytes'],p['BSS_bytes']),
                                 (seg1,seg4,total,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),21)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-append-prepend-bosses-build.json')).is_file(),
                         'native TASM OMF and linked Japanese MZ pairs absent')
    def test_original_63_ordered_fixups_and_nine_typed_rtti_records(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'string-append-prepend-bosses-build.json')).read_text())
        for n,(seg1,seg4,total) in CODE.items():
            member=members[NATIVE[n]['index']]
            self.assertEqual(member.name,n)
            original=original_library_member(member)
            po=payload(original)
            self.assertEqual(len(po),total)
            self.assertEqual(code_publics(original,4),NATIVE[n]['publics'])
            self.assertEqual([x.data.hex() for x in parse_omf(original)
                              if x.name=='GRPDEF'],['0aff02ff03'])
            F=literal_fields(original)
            self.assertEqual(len(F),21)
            for seg,count in ((1,9),(4,12)):
                sites=[f['site'] for f in F if f['segment']==seg]
                self.assertEqual(len(sites),count)
                self.assertEqual(sites,sorted(sites,reverse=True))
            for at,name in zip(RTTI[n],
                               (b'string::lengtherror\0',b'xalloc\0\0',b'xmsg\0\0')):
                self.assertEqual(bytes(po[4,i] for i in range(at,at+len(name))),name)
            for row in rec['rounds']:
                with self.subTest(member=n,native_round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),po)
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        member.program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
