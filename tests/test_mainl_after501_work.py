"""Original ios destructor global fmtflags, class RTTI, vtable and BSS ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after501_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after501_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-destructor-rtti-vtable-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
DATA_PUBLICS=[(0,'@ios@basefield'),(4,'@ios@adjustfield'),
              (8,'@ios@floatfield'),(12,'@ios@nextbit'),
              (16,'@ios@usercount')]

class OriginalIOSDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'scoped source receipt absent')
    def test_original_full_member_and_two_native_mainl_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,709,184))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(141,186575))
        self.assertEqual((r['profiles']['stdtr']['CODE_bytes'],
                          r['profiles']['stdtr']['DATA_bytes'],
                          r['profiles']['stdtr']['BSS_bytes']),(141,30,4))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original ios destructor absent')
    def test_original_global_flags_rtti_vtable_and_all_fixups(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['stdtr']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),171)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(orig,1),[(0,'@ios@$bdtr$qv')])
        self.assertEqual(code_publics(orig,2),DATA_PUBLICS)
        self.assertEqual(code_publics(orig,3),[(0,'@ios@stdioflush')])
        self.assertEqual(externs(orig),['@$bdele$qnv','@$bdla$qnv',
                                        '@__RefDestructorCount$qv'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual(bytes(P[2,i] for i in range(18)),
                         bytes.fromhex('700000000e00000000180000100000000000'))
        self.assertEqual(bytes(P[1,i] for i in range(125,129)),b'ios\0')
        self.assertFalse(any(seg==3 for seg,i in P))
        self.assertEqual({(f['segment'],f['site']):(f['target_method'],f['target'],f['addend'])
                          for f in F},
                         {(1,6):(2,3,0),(1,37):(0,2,26),(1,58):(2,2,0),
                          (1,77):(2,1,0),(1,117):(0,1,0),
                          (2,18):(0,1,87),(2,26):(0,1,0)})
        canonical=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['stdtr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(code_publics(made,2),DATA_PUBLICS)
            self.assertEqual(code_publics(made,3),[(0,'@ios@stdioflush')])
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),canonical)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
