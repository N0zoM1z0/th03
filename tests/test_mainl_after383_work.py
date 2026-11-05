"""Original complete Borland string::substr and original ordered OMF fields."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after383_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after383_work import review

class OriginalStringSubstrBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-substr-exception-boss-build.json')).is_file(),
                         'native original 489-member Japanese CRT receipt absent')
    def test_full_substr_bounds_exception_and_native_link(self):
        r=review('string-substr-exception-boss')
        p=r['profiles']['substr1']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,489,404))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(570,155180))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(199,371,570,0,0))
        self.assertEqual(p['publics'],[(0,'@string@substr$xqui')])
        self.assertEqual(p['imports'],NATIVE['substr1']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),24)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-substr-exception-boss-build.json')).is_file(),
                         'raw original/source native OMF and Japanese EXE/MAP absent')
    def test_original_24_literal_fixups_and_type_record_padding(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['substr1']['index']]
        self.assertEqual(m.name,'substr1')
        o=original_library_member(m);P=payload(o);F=literal_fields(o)
        self.assertEqual(len(P),570)
        self.assertEqual(code_publics(o,4),[(0,'@string@substr$xqui')])
        self.assertEqual([r.data.hex() for r in parse_omf(o) if r.name=='GRPDEF'],
                         ['0aff02ff03'])
        self.assertEqual(len(F),24)
        for seg,count in ((1,11),(4,13)):
            sites=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for off,txt in ((104,b'string *\0'),(151,b'string::outofrange\0\0'),
                        (229,b'xalloc\0\0'),(295,b'xmsg\0\0'),
                        (351,b'string\0\0')):
            self.assertEqual(bytes(P[4,i] for i in range(off,off+len(txt))),txt)
        rec=json.loads((ROOT/(PREFIX+'string-substr-exception-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                obj=(ROOT/row['outputs']['substr1']['path']).read_bytes()
                self.assertEqual(payload(obj),P)
                self.assertEqual(literal_fields(obj),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['substr1'])
                self.assertFalse(row['original_program_equal_by_member']['substr1'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
