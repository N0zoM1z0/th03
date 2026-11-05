"""Original complete Borland string::remove exception/RTTI and 30-byte DATA."""
import json
import sys
import unittest
import setuptools
from pathlib import Path
sys.setrecursionlimit(max(sys.getrecursionlimit(),5000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after371_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after371_work import review

class OriginalStringRemoveBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-remove-exception-boss-build.json')).is_file(),
                         'scoped 452-source native Japanese CRT receipt absent')
    def test_full_remove_bounds_exception_and_native_link(self):
        r=review('string-remove-exception-boss')
        p=r['profiles']['stremove']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,452,441))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (822,143949))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(284,538,822,30,0))
        self.assertEqual(p['publics'],[(0,'@string@remove$quiui')])
        self.assertEqual(p['imports'],NATIVE['stremove']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),37)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-remove-exception-boss-build.json')).is_file(),
                         'raw TASM original/source OBJ and EXE receipts absent')
    def test_all_37_original_fixupps_bounds_message_rtti_and_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['stremove']['index']]
        self.assertEqual(m.name,'stremove')
        old=original_library_member(m)
        P=payload(old)
        self.assertEqual(len(P),852)
        self.assertEqual(code_publics(old,4),[(0,'@string@remove$quiui')])
        self.assertEqual([x.data.hex() for x in parse_omf(old)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        self.assertEqual(bytes(P[2,i] for i in range(30)),b'String reference out of range\0')
        F=literal_fields(old)
        self.assertEqual(len(F),37)
        for seg,count in ((1,16),(4,21)):
            sites=[f['site'] for f in F if f['segment']==seg]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for offset,bs in ((318,b'xmsg\0\0'),(374,b'string\0\0'),
                          (432,b'xalloc\0\0'),(498,b'string::outofrange\0\0')):
            self.assertEqual(bytes(P[4,i] for i in range(offset,offset+len(bs))),bs)
        self.assertEqual((next(f for f in F if f['segment']==4 and f['site']==63)['target'],
                          next(f for f in F if f['segment']==4 and f['site']==63)['frame_method']),
                         (2,1))
        receipt=json.loads((ROOT/(PREFIX+'string-remove-exception-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['stremove']['path']).read_bytes()
                self.assertEqual(payload(made),P)
                self.assertEqual(literal_fields(made),F)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['stremove'])
                self.assertFalse(row['original_program_equal_by_member']['stremove'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
