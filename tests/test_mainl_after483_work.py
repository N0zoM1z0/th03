"""Original ios::setf 32-bit masks and Borland formatting state ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after483_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after483_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-32bit-format-flags-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalIOSSetf(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native format flag proof missing')
    def test_complete_original_and_both_native_mainl_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,691,202))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(195,183932))
        self.assertEqual((r['profiles']['stsetf1']['CODE_bytes'],
                          r['profiles']['stsetf1']['DATA_bytes']),(195,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original ios flag OMF missing')
    def test_three_real_mask_groups_and_twelve_complete_fixups(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['stsetf1']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),195)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(raw,1),[(0,'@ios@setf$ql')])
        self.assertEqual(externs(raw),[
            '@ios@basefield','@ios@adjustfield','@ios@floatfield'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        self.assertEqual({f['site']:(f['target_method'],f['target'],f['addend'])
                          for f in F},
                         {33:(2,2,0),37:(2,2,2),45:(2,2,2),48:(2,2,0),
                          70:(2,1,0),74:(2,1,2),82:(2,1,2),85:(2,1,0),
                          110:(2,3,0),114:(2,3,2),122:(2,3,2),125:(2,3,0)})
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['stsetf1']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS) for f in literal_fields(obj)),expected)
            self.assertNotEqual(literal_fields(obj),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
