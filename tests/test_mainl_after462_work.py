"""Original FAR vector-delete dispatcher and near-frame precision."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after462_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after462_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='far-vector-delete-dispatch-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFarVectorDelete(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native vector destructor evidence missing')
    def test_entire_original_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,670,223))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(215,179995))
        self.assertEqual((r['profiles']['vdelxf']['CODE_bytes'],
                          r['profiles']['vdelxf']['DATA_bytes']),(215,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original far-vector OMF missing')
    def test_four_symbolic_call_sites_and_single_exact_near_exception(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['vdelxf']['index']]
        self.assertEqual(m.name,'vdelxf')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),215)
        self.assertEqual(len(F),4)
        self.assertEqual(code_publics(original,1),
                         [(0,'@_vector_delete_$qnvuiuiuluie')])
        self.assertEqual(externs(original),[
            '@_vector_delete_$qnvuiuluie','@__RefDestructorCount$qv','N_LXMUL@'])
        self.assertEqual(NEAR_FRAME_GAPS,{'vdelxf':{118:3}})
        f={v['site']:v for v in F}
        self.assertEqual({k:(v['target_method'],v['target']) for k,v in f.items()},
                         {118:(2,3),123:(2,2),171:(2,1),202:(2,1)})
        r=json.loads(RECEIPT.read_text())
        for round in r['rounds']:
            b=(ROOT/round['outputs']['vdelxf']['path']).read_bytes()
            self.assertEqual(payload(b),P)
            actual={x['site']:x for x in literal_fields(b)}
            self.assertEqual(set(f),set(actual))
            for site,orig in f.items():
                current=actual[site]
                if site==118:
                    self.assertEqual((orig['frame_method'],orig['frame']),(5,None))
                    self.assertEqual((current['frame_method'],current['frame']),(0,1))
                    keys=set(orig)-{'frame_method','frame'}
                    self.assertEqual({k:orig[k] for k in keys},
                                     {k:current[k] for k in keys})
                else:self.assertEqual(orig,current)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
