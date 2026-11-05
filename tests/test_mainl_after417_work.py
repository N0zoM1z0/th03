"""Original 383-CODE/12-DATA stdiostream constructor and real typed RTTI."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after417_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after417_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='stdiostream-file-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalStdiostreamFileConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original stdiostream receipt absent')
    def test_full_borland_constructor_and_two_japanese_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,604,289))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (383,167706))
        self.assertEqual((r['profiles']['sdctr']['CODE_bytes'],r['profiles']['sdctr']['DATA_bytes']),
                         (383,12))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native constructor source/OBJ pair absent')
    def test_complete_four_rtti_types_and_fifteen_relocation_fields(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['sdctr']['index']]
        self.assertEqual(m.name,'sdctr')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),395)
        self.assertEqual(code_publics(orig,1),[(0,'@stdiostream@$bctr$qn4FILE')])
        self.assertEqual(externs(orig),NATIVE['sdctr']['imports'])
        self.assertEqual(len(F),15)
        self.assertEqual(bytes(P[1,i] for i in range(163,175)),b'stdiostream\0')
        self.assertEqual(bytes(P[1,i] for i in range(239,249)),b'stdiobuf\0\0')
        self.assertEqual(bytes(P[1,i] for i in range(307,311)),b'ios\0')
        self.assertEqual(bytes(P[1,i] for i in range(361,371)),b'streambuf\0')
        self.assertEqual(bytes(P[2,i] for i in range(12)),bytes.fromhex('7d0000000000000000000000'))
        self.assertEqual([(f['segment'],f['site'],f['target_method'],f['target'],f['addend'])
                          for f in F if f['segment']==1 and f['site'] in (155,175,191,249)],
                         [(1,249,0,1,323),(1,191,0,1,201),
                          (1,175,0,1,269),(1,155,2,9,0)])
        self.assertEqual([(f['segment'],f['site']) for f in F if f['segment']==2],
                         [(2,8),(2,0)])
        original_fields=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['sdctr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             original_fields)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['sdctr'])
            self.assertFalse(row['original_program_equal_by_member']['sdctr'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
