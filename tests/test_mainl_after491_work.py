"""Original DOS time/stime roll-over-safe two FAR APIs and exact OMF targets."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after491_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after491_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-settime-gettime-rollover-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalDosTime(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS time source receipt missing')
    def test_full_original_source_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,699,194))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(170,185165))
        self.assertEqual((r['profiles']['stime']['CODE_bytes'],
                          r['profiles']['stime']['DATA_bytes']),(170,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original time OMF missing')
    def test_both_far_entrypoints_and_rollover_retry(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['stime']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),170)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(raw,1),[(0,'_stime'),(64,'_time')])
        self.assertEqual(externs(raw),['_dostounix','_getdate','_gettime',
                                      '_setdate','_settime','_unixtodos'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {29:(2,6),39:(2,4),49:(2,5),78:(2,2),
                          88:(2,3),98:(2,2),124:(2,1)})
        self.assertEqual(bytes(P[1,i] for i in range(0x6c,0x71)),
                         bytes.fromhex('3a46f275d7'))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['stime']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
