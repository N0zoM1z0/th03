"""Original Borland DOS sleep with time rollover and FAR gettime."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after510_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after510_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='original-dos-time-rollover-sleep-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalSleep(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'sleep receipt missing')
    def test_complete_original_member_and_two_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,718,175))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(109,187626))
        self.assertEqual((r['profiles']['sleep']['CODE_bytes'],
                          r['profiles']['sleep']['DATA_bytes']),(109,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS sleep OMF unavailable')
    def test_three_original_far_time_calls_and_rollover(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['sleep']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),109)
        self.assertEqual(code_publics(original,1),[(0,'_sleep')])
        self.assertEqual(externs(original),['_gettime'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {14:(2,1),55:(2,1),87:(2,1)})
        self.assertEqual(bytes(P[1,i] for i in range(20,24)),
                         bytes.fromhex('807efe5a'))
        expect=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['sleep']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expect)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
