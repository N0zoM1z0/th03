"""Original DOS file region lock/unlock and exact near IOERROR OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after496_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after496_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-file-region-lock-unlock-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosLock(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'scoped native lock proof absent')
    def test_original_member_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,704,189))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(78,185827))
        self.assertEqual((r['profiles']['lock']['CODE_bytes'],
                          r['profiles']['lock']['DATA_bytes']),(78,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS lock member absent')
    def test_both_dos_21h_calls_and_literal_omf(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['lock']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),78)
        self.assertEqual(code_publics(orig,1),[(0,'_lock'),(39,'_unlock')])
        self.assertEqual(externs(orig),['__IOERROR'])
        self.assertEqual([f['site'] for f in F],[33,72])
        self.assertEqual([(f['location_type'],f['frame_method'],f['frame'],
                          f['target_method'],f['target'],f['addend']) for f in F],
                         [(1,0,1,2,1,0)]*2)
        r=json.loads(RECEIPT.read_text())
        for round in r['rounds']:
            obj=(ROOT/round['outputs']['lock']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(literal_fields(obj),F)
            self.assertTrue(round['literal_omf_fixupp_equal_by_member']['lock'])
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
