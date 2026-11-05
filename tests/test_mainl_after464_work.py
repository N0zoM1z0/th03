"""Original NEC/IBM conio rectangle dispatchers and complete code."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after464_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after464_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='pc98-ibm-conio-text-dispatch-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
       'frame_method','frame','target_method','target','addend')
class OriginalConioTextDispatch(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound NEC/IBM evidence missing')
    def test_complete_native_two_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,672,221))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(210,180440))
        self.assertEqual((r['profiles']['ccomgptx']['CODE_bytes'],
                          r['profiles']['ccomgptx']['DATA_bytes']),(210,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'native NEC/IBM OMF absent')
    def test_three_far_entrypoints_and_all_twelve_original_relations(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['ccomgptx']['index']]
        self.assertEqual(m.name,'ccomgptx')
        raw=original_library_member(m)
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),210)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(raw,1),[(0,'_gettext'),(74,'_puttext'),
                                             (148,'__getputtextsize')])
        self.assertEqual(externs(raw),NATIVE['ccomgptx']['imports'])
        sites={f['site']:(f['target_method'],f['target']) for f in F}
        self.assertEqual(sites,{195:(2,6),185:(2,7),177:(2,3),
                                167:(2,7),133:(2,4),117:(2,7),
                                109:(2,1),93:(2,7),59:(2,5),
                                43:(2,7),35:(2,2),19:(2,7)})
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['ccomgptx']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
