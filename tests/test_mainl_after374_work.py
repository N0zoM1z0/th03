"""Original complete Borland C++ string::reserve and 19 literal FIXUPPs."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after374_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after374_work import review

class OriginalStringReserveBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-reserve-capacity-boss-build.json')).is_file(),
                         'native original 460-source Japanese receipts absent')
    def test_complete_reserve_capacity_exception_and_original_native_link(self):
        r=review('string-reserve-capacity-boss')
        p=r['profiles']['reserve']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,460,433))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(431,146094))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(177,254,431,0,0))
        self.assertEqual(p['publics'],[(0,'@string@reserve$qui')])
        self.assertEqual(p['imports'],NATIVE['reserve']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),19)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-reserve-capacity-boss-build.json')).is_file(),
                         'source and original native OMF/MZ pairs absent')
    def test_19_original_fixups_rtti_and_two_raw_rounds(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['reserve']['index']]
        self.assertEqual(m.name,'reserve')
        original=original_library_member(m)
        po=payload(original)
        self.assertEqual(len(po),431)
        self.assertEqual(code_publics(original,4),[(0,'@string@reserve$qui')])
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        F=literal_fields(original)
        self.assertEqual(len(F),19)
        for seg,count in ((1,9),(4,10)):
            pos=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(pos),count)
            self.assertEqual(pos,sorted(pos,reverse=True))
        for off,bs in ((92,b'string::outofrange\0\0'),(170,b'xalloc\0\0'),
                       (236,b'xmsg\0\0')):
            self.assertEqual(bytes(po[4,i] for i in range(off,off+len(bs))),bs)
        rec=json.loads((ROOT/(PREFIX+'string-reserve-capacity-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(native_round=row['round']):
                made=(ROOT/row['outputs']['reserve']['path']).read_bytes()
                self.assertEqual(payload(made),po)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['reserve'])
                self.assertFalse(row['original_program_equal_by_member']['reserve'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
