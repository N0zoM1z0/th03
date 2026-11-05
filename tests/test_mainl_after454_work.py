"""Original stateful far MBCS tokenizer with the persistent far cursor."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after454_work import PREFIX,WORK,NATIVE,retained,original_library_member
from review_th03_mainl_after454_work import review
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='far-multibyte-strtok-state-machine'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalFarMBCSTokenizer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original MBCS receipt missing')
    def test_complete_original_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,662,231))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (230,177902))
        self.assertEqual((r['profiles']['FMBSTOK']['CODE_bytes'],
                          r['profiles']['FMBSTOK']['DATA_bytes']),(230,4))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'native original MBCS OMF absent')
    def test_static_far_cursor_and_leadbyte_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['FMBSTOK']['index']]
        self.assertEqual(m.name,'FMBSTOK')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),234)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(orig,1),[(0,'__fmbstok')])
        self.assertEqual(externs(orig),NATIVE['FMBSTOK']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(4)),b'\0'*4)
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        sites={f['site']:f for f in F}
        self.assertEqual((sites[54]['target_method'],sites[54]['target']),(2,3))
        self.assertEqual((sites[127]['target_method'],sites[127]['target']),(2,2))
        self.assertEqual((sites[93]['frame_method'],sites[93]['target_method'],
                          sites[93]['target'],sites[93]['addend']),(1,2,1,1))
        self.assertEqual((sites[213]['target_method'],sites[213]['target'],
                          sites[213]['addend']),(0,2,2))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['FMBSTOK']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            self.assertEqual([r.data.hex() for r in parse_omf(made) if r.name=='GRPDEF'],
                             ['08ff02ff03'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
