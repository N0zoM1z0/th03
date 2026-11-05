"""Original DOS ftime, timezone and near DST/division invocation."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after463_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after463_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-ftime-timezone-dst-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosFtime(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native time-conversion evidence missing')
    def test_original_scope_two_complete_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,671,222))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(235,180230))
        self.assertEqual((r['profiles']['_ftime']['CODE_bytes'],
                          r['profiles']['_ftime']['DATA_bytes']),(235,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original time-conversion OMF absent')
    def test_both_dos_helpers_and_only_two_near_call_frame_gaps(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['_ftime']['index']]
        self.assertEqual(m.name,'_ftime')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),235)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(orig,1),[(46,'__ftime')])
        self.assertEqual(externs(orig),NATIVE['_ftime']['imports'])
        self.assertEqual(NEAR_FRAME_GAPS,{'_ftime':{119:6,159:5}})
        # Original DOS interrupts 2Ah and 2Ch and the 3 push-CS near calls.
        self.assertEqual(bytes(P[1,i] for i in (5,6,7,8)),bytes.fromhex('b42acd21'))
        self.assertEqual(bytes(P[1,i] for i in (28,29,30,31)),bytes.fromhex('b42ccd21'))
        original={x['site']:x for x in F}
        self.assertEqual(set(original),{55,112,116,119,130,159,196})
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['_ftime']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            actual={x['site']:x for x in literal_fields(made)}
            self.assertEqual(set(actual),set(original))
            for site,field in original.items():
                out=actual[site]
                if site in NEAR_FRAME_GAPS['_ftime']:
                    self.assertEqual((field['frame_method'],field['frame']),(5,None))
                    self.assertEqual((out['frame_method'],out['frame']),(0,1))
                    others=set(field)-{'frame_method','frame'}
                    self.assertEqual({k:field[k] for k in others},
                                     {k:out[k] for k in others})
                else:self.assertEqual(out,field)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
