"""Original Borland FAR heap binary search, true multiply/add and comparator."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after489_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after489_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='far-heap-binary-search-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFarHeapBinarySearch(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native bsearch receipt missing')
    def test_complete_original_scope_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,697,196))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(145,184835))
        self.assertEqual((r['profiles']['hbsearch']['CODE_bytes'],
                          r['profiles']['hbsearch']['DATA_bytes']),(145,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original heap search OMF missing')
    def test_comparator_and_three_exact_imported_near_frame_gaps(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['hbsearch']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),145)
        self.assertEqual(len(F),3)
        self.assertEqual(code_publics(original,1),[(0,'__hbsearch')])
        self.assertEqual(externs(original),['N_LXMUL@','N_PADD@'])
        self.assertEqual(NEAR_FRAME_GAPS,{'hbsearch':{41:1,54:2,111:2}})
        self.assertEqual(bytes(P[1,i] for i in range(70,73)),
                         bytes.fromhex('ff5e12'))
        original_by_site={f['site']:f for f in F}
        self.assertEqual(set(original_by_site),{41,54,111})
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['hbsearch']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            observed={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(observed),set(original_by_site))
            for site,f in original_by_site.items():
                g=observed[site]
                self.assertEqual((f['frame_method'],f['frame']),(5,None))
                self.assertEqual((g['frame_method'],g['frame']),(0,1))
                self.assertEqual((f['target_method'],f['target'],f['addend']),
                                 (2,NEAR_FRAME_GAPS['hbsearch'][site],0))
                for k in set(f)-{'frame_method','frame'}: self.assertEqual(f[k],g[k])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
