"""Original Borland itoa/ultoa/ltoa and three exact imported near-call gaps."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after486_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after486_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='integer-radix-string-three-entrypoints'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalLtoaRadix(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original radix source-bound receipt missing')
    def test_original_code_and_two_native_exe_map_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,694,199))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(124,184344))
        self.assertEqual((r['profiles']['ltoa1']['CODE_bytes'],
                          r['profiles']['ltoa1']['DATA_bytes']),(124,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original ltoa OMF unavailable')
    def test_three_far_entries_and_three_locked_near_frame_gaps(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['ltoa1']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),124)
        self.assertEqual(len(F),3)
        self.assertEqual(code_publics(original,1),
                         [(0,'_itoa'),(47,'_ultoa'),(80,'_ltoa')])
        self.assertEqual(externs(original),['__LONGTOA'])
        self.assertEqual(NEAR_FRAME_GAPS,{'ltoa1':{41:1,74:1,118:1}})
        fields={x['site']:x for x in F}
        self.assertEqual(set(fields),{41,74,118})
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['ltoa1']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            records={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(records),set(fields))
            for site,orig in fields.items():
                now=records[site]
                self.assertEqual((orig['frame_method'],orig['frame']),(5,None))
                self.assertEqual((now['frame_method'],now['frame']),(0,1))
                for k in set(orig)-{'frame_method','frame'}:
                    self.assertEqual(orig[k],now[k])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
