"""Original Borland far-heap search core, find and insert APIs."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after469_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after469_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='far-heap-linear-search-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFarHeapLinearSearch(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'search native source receipt missing')
    def test_original_scope_and_two_native_full_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,677,216))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']), (209,181413))
        self.assertEqual((r['profiles']['hlsearch']['CODE_bytes'],
                          r['profiles']['hlsearch']['DATA_bytes']),(209,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'search original OMF unavailable')
    def test_real_search_insert_and_exact_one_near_frame_gap(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['hlsearch']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),209)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(orig,1),[(124,'__hlsearch'),(167,'__hlfind')])
        self.assertEqual(externs(orig),['__fmovmem','N_PADA@'])
        self.assertEqual(NEAR_FRAME_GAPS,{'hlsearch':{52:2}})
        original={f['site']:f for f in F}
        self.assertEqual(set(original),{52,91})
        self.assertEqual((original[52]['target_method'],original[52]['target']),
                         (2,2))
        self.assertEqual((original[91]['target_method'],original[91]['target']),
                         (2,1))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['hlsearch']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            observed={f['site']:f for f in literal_fields(obj)}
            self.assertEqual(set(observed),set(original))
            self.assertEqual(observed[91],original[91])
            self.assertEqual((original[52]['frame_method'],original[52]['frame']),
                             (5,None))
            self.assertEqual((observed[52]['frame_method'],observed[52]['frame']),
                             (0,1))
            for key in set(original[52])-{'frame_method','frame'}:
                self.assertEqual(observed[52][key],original[52][key])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
