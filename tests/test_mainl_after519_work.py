"""Original fstreambase open mode translation and native ios state."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after519_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after519_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='fstreambase-open-native-ios-state'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalFstreamOpen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.exists():raise unittest.SkipTest('fstreambase open receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['fsopen']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_complete_source_bound_two_rounds(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,727,166))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(105,194201))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_true_filebuf_and_ios_state_calls_and_both_fixups(self):
        P=payload(self.original);F=literal_fields(self.original)
        self.assertEqual(len(P),105)
        self.assertEqual(code_publics(self.original,1),
                         [(0,'@fstreambase@open$qnxcii')])
        self.assertEqual(externs(self.original),
                         ['@ios@clear$qi','@filebuf@open$qnxcii'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {67:(2,2),94:(2,1)})
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        for row in self.receipt['rounds']:
            made=(ROOT/row['outputs']['fsopen']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['fsopen'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
