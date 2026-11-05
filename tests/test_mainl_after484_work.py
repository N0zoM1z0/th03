"""Original ios(streambuf FAR*) typed RTTI and real virtual destructor ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after484_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after484_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ios-streambuf-constructor-rtti-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalIOSStreambufConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original ios constructor receipt missing')
    def test_source_parity_and_two_complete_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,692,201))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(153,184085))
        self.assertEqual((r['profiles']['stctr2']['CODE_bytes'],
                          r['profiles']['stctr2']['DATA_bytes']),(153,12))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'typed original ios OMF missing')
    def test_real_typed_code99_rtti_and_data8_vtable(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['stctr2']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),165)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(raw,1),
                         [(0,'@ios@$bctr$qn9streambuf')])
        self.assertEqual(externs(raw),NATIVE['stctr2']['imports'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        self.assertEqual(bytes(P[2,i] for i in range(12)),
                         bytes.fromhex('630000000000000000000000'))
        self.assertEqual(bytes(P[1,i] for i in range(137,141)),b'ios\0')
        rels={(x['segment'],x['site']):x for x in F}
        self.assertEqual((rels[1,39]['target_method'],rels[1,39]['target'],
                          rels[1,39]['addend']),(0,2,8))
        self.assertEqual((rels[2,0]['target_method'],rels[2,0]['target'],
                          rels[2,0]['addend']),(0,1,99))
        self.assertEqual((rels[2,8]['target_method'],rels[2,8]['target']),
                         (2,3))
        self.assertEqual((rels[1,64]['target_method'],rels[1,64]['target']),
                         (2,4))
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['stctr2']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(obj)),expected)
            self.assertNotEqual(literal_fields(obj),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
