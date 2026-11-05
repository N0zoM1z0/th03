"""Original Borland complex double arithmetic and x87 EMUL import chronology."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after461_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after461_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='complex-x87-multiply-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
PUBLICS=[(0,'@abs$qm7complex'),(46,'@norm$qm7complex'),(89,'@complex@$brmul$qm7complex'),(167,'@$bmul$qm7complext1')]
IMPORTS=['FIERQQ','FIDRQQ','FIWRQQ','@$bnew$qui']
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')
class OriginalComplexFpuArithmetic(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native complex arithmetic receipt missing')
    def test_complete_four_functions_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,669,224))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (364,179780))
        self.assertEqual((r['profiles']['cplx1']['CODE_bytes'],
                          r['profiles']['cplx1']['DATA_bytes']),(364,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original complex arithmetic OMF missing')
    def test_real_fpu_relocations_and_far_allocator_after_emulator(self):
        _,_,_,members,_,_=retained()
        member=members[NATIVE['cplx1']['index']]
        self.assertEqual(member.name,'cplx1')
        orig=original_library_member(member)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),364)
        self.assertEqual(len(F),55)
        self.assertEqual(code_publics(orig,1),PUBLICS)
        self.assertEqual(externs(orig),IMPORTS)
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        sites={f['site']:f for f in F}
        for site,target,addend in [(11,1,9883),(15,2,55451),
                                   (225,3,39824),(262,3,39824),
                                   (280,3,39824),(344,3,39824)]:
            f=sites[site]
            self.assertEqual((f['target_method'],f['target'],f['addend']),
                             (2,target,addend))
        alloc=sites[309]
        self.assertEqual((alloc['location_type'],alloc['width'],
                          alloc['target_method'],alloc['target'],alloc['addend']),
                         (3,4,2,4,0))
        self.assertEqual(P[1,308],0x9a)
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['cplx1']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(code_publics(made,1),PUBLICS)
            self.assertEqual(externs(made),IMPORTS)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
