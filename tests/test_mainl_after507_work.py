"""Original ios::iword far user-word slot and usersize expansion ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after507_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after507_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-iword-usersize-array-slot-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalIOSIword(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native iword receipt absent')
    def test_entire_original_member_two_mainl_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,715,178))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(97,187296))
        self.assertEqual((r['profiles']['stiword']['CODE_bytes'],
                          r['profiles']['stiword']['DATA_bytes']),(97,4))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original iword object absent')
    def test_real_usersize_and_invalid_slot_data_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['stiword']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),101)
        self.assertEqual(code_publics(original,1),[(0,'@ios@iword$qi')])
        self.assertEqual(externs(original),
                         ['@ios@usercount','@ios@usersize$qi'])
        self.assertEqual(bytes(P[2,i] for i in range(4)),bytes(4))
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual({f['site']:(f['target_method'],f['target'],f['addend']) for f in F},
                         {12:(2,1,0),22:(0,2,0),46:(2,2,0),68:(0,2,0)})
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['stiword']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
