"""Original TStringRef char constructor and xalloc address semantics."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after480_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after480_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='tstringref-character-capacity-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalTStringRefConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native TStringRef receipt missing')
    def test_complete_original_and_both_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,688,205))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(197,183350))
        self.assertEqual((r['profiles']['ctor8']['CODE_bytes'],
                          r['profiles']['ctor8']['DATA_bytes']),(197,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original TStringRef object absent')
    def test_far_allocator_capacity_memset_and_xalloc_address(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['ctor8']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),197)
        self.assertEqual(len(F),7)
        self.assertEqual(code_publics(raw,1),[(0,'@TStringRef@$bctr$qcui')])
        self.assertEqual(externs(raw),NATIVE['ctor8']['imports'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {18:(2,1),62:(2,6),81:(2,4),109:(2,7),
                          113:(2,5),140:(2,3),170:(2,2)})
        self.assertEqual(P[1,108],0xb8) # xalloc ADDRESS, not indirect load
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['ctor8']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
