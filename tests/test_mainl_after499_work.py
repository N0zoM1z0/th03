"""Original Borland ios::usersize array growth and FAR lifetime ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after499_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after499_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-usersize-far-array-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalIOSUserArray(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native usersize receipt absent')
    def test_complete_original_and_both_native_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,707,186))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(156,186321))
        self.assertEqual((r['profiles']['stusize']['CODE_bytes'],
                          r['profiles']['stusize']['DATA_bytes']),(156,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original usersize object absent')
    def test_allocation_copy_deletion_and_original_three_far_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['stusize']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),156)
        self.assertEqual(code_publics(original,1),[(0,'@ios@usersize$qi')])
        self.assertEqual(externs(original),['@$bnwa$qui','@$bdla$qnv','_memcpy'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual({x['site']:(x['target_method'],x['target']) for x in F},
                         {17:(2,1),67:(2,3),83:(2,2)})
        self.assertEqual(len(F),3)
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['stusize']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
