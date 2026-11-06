"""Original ostream FAR pointer insertion formatting and seven OMF fields."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after504_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after504_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ostream-pointer-format-flags-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalOstreamPointer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native ostream pointer source receipt absent')
    def test_complete_original_code_and_two_native_mainl_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,712,181))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(135,186946))
        self.assertEqual((r['profiles']['ostptr']['CODE_bytes'],
                          r['profiles']['ostptr']['DATA_bytes']),(135,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original ostream pointer OMF missing')
    def test_original_flag_groups_and_real_ulong_insertion(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['ostptr']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),135)
        self.assertEqual(code_publics(original,1),[(0,'@ostream@$blsh$qnv')])
        self.assertEqual(externs(original),
                         ['@ios@basefield','@ios@adjustfield',
                          '@ios@flags$ql','@ios@setf$qll',
                          '@ostream@$blsh$qul'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual(len(F),7)
        self.assertEqual({f['site']:(f['target_method'],f['target'],f['addend']) for f in F},
                         {30:(2,1,2),33:(2,1,0),37:(2,2,0),44:(2,2,2),
                          63:(2,4,0),98:(2,5,0),116:(2,3,0)})
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['ostptr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
