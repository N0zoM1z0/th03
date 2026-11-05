"""Original Borland ios setbase FAR manipulator allocation and callback."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after476_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after476_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='cxx-ios-setbase-manipulator-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalSetbase(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'new native manipulator receipt missing')
    def test_complete_member_and_two_native_mainl_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,684,209))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']), (205,182684))
        self.assertEqual((r['profiles']['mnsbase']['CODE_bytes'],
                          r['profiles']['mnsbase']['DATA_bytes']),(205,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original manipulator OMF unavailable')
    def test_real_private_far_setter_and_allocated_public_callback(self):
        _,_,_,members,_,_=retained()
        member=members[NATIVE['mnsbase']['index']]
        self.assertEqual(member.name,'mnsbase')
        raw=original_library_member(member)
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),205)
        self.assertEqual(len(F),6)
        self.assertEqual(code_publics(raw,1),[(110,'@setbase$qi')])
        self.assertEqual(externs(raw),
                         ['@$bnew$qui','@ios@basefield','@ios@setf$qll'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        sites={f['site']:f for f in F}
        self.assertEqual(set(sites),{72,76,91,151,173,178})
        self.assertEqual({site:(sites[site]['target_method'],sites[site]['target'])
                          for site in (72,76,91,151,173,178)},
                         {72:(2,2),76:(2,2),91:(2,3),151:(2,1),
                          173:(0,1),178:(0,1)})
        self.assertEqual((sites[173]['location_type'],sites[178]['location_type']),
                         (2,1))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            obj=(ROOT/row['outputs']['mnsbase']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(obj)),expected)
            self.assertNotEqual(literal_fields(obj),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
