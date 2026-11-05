"""Original getw two-byte FAR stream leaf with buffered and fallback paths."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after468_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after468_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='stdio-getw-two-byte-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalGetW(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'getw source receipt missing')
    def test_complete_original_and_two_new_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,676,217))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(130,181204))
        self.assertEqual((r['profiles']['getw']['CODE_bytes'],
                          r['profiles']['getw']['DATA_bytes']),(130,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original getw OMF missing')
    def test_two_real_fgetc_references_and_eof_control_flow(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['getw']['index']]
        self.assertEqual(m.name,'getw')
        raw=original_library_member(m)
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),130)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(raw,1),[(0,'_getw')])
        self.assertEqual(externs(raw),['__fgetc'])
        self.assertEqual({x['site']:(x['target_method'],x['target']) for x in F},
                         {44:(2,1),94:(2,1)})
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['getw']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
