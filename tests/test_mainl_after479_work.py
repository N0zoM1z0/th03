"""Original Borland FAR overlap-safe memory move and public wrapper."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after479_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after479_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='far-overlap-safe-memmove-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFarMemmove(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source memmove receipt missing')
    def test_original_code_and_two_independent_mainl_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,687,206))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(119,183153))
        self.assertEqual((r['profiles']['fmovmem']['CODE_bytes'],
                          r['profiles']['fmovmem']['DATA_bytes']),(119,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original far-copy OMF absent')
    def test_true_direction_flag_and_only_near_segment_compare(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['fmovmem']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),119)
        self.assertEqual(len(F),1)
        self.assertEqual(code_publics(raw,1),
                         [(0,'__fmovmem'),(82,'__fmemmove')])
        self.assertEqual(externs(raw),['N_PCMP@'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual((F[0]['site'],F[0]['location_type'],
                          F[0]['target_method'],F[0]['target'],
                          F[0]['frame_method'],F[0]['frame']),
                         (19,1,2,1,0,1))
        self.assertEqual(P[1,23],0xfd)  # STD on backward copy
        self.assertEqual(P[1,29],0xfc)  # CLD on forward copy
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fmovmem']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fmovmem'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':
    unittest.main()
