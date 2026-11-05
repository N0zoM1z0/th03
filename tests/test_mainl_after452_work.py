"""Source-bound original filebuf::setbuf and all three buffer-window calls."""
import sys,json,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after452_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after452_work import review
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='filebuf-setbuf-range-management'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method',
      'frame','target_method','target','addend')
class OriginalFilebufSetbuf(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'complete native buffer scope missing')
    def test_entire_source_and_native_reproduction(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,660,233))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (191,177498))
        self.assertEqual((r['profiles']['fsbsbuf']['CODE_bytes'],
                          r['profiles']['fsbsbuf']['DATA_bytes']),(191,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original OMF missing')
    def test_three_true_streambuf_calls_and_complete_logical_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsbsbuf']['index']]
        self.assertEqual(m.name,'fsbsbuf')
        orig=original_library_member(m)
        P=payload(orig); F=literal_fields(orig)
        self.assertEqual(len(P),191)
        self.assertEqual(len(F),3)
        self.assertEqual(code_publics(orig,1),[(0,'@filebuf@setbuf$qnci')])
        self.assertEqual(externs(orig),NATIVE['fsbsbuf']['imports'])
        self.assertEqual([(f['site'],f['target_method'],f['target']) for f in sorted(F,key=lambda x:x['site'])],
                         [(110,2,3),(138,2,1),(172,2,2)])
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fsbsbuf']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
