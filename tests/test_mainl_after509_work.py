"""Original FAR strncat with authentic strlen and overlap-aware move."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after509_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after509_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='original-far-strncat-move-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalFarStrncat(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original FAR strncat receipt missing')
    def test_two_complete_original_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,717,176))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(105,187517))
        self.assertEqual((r['profiles']['fstrncat']['CODE_bytes'],
                          r['profiles']['fstrncat']['DATA_bytes']),(105,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original FAR strncat OMF missing')
    def test_two_real_far_strlen_and_single_movmem(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['fstrncat']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),105)
        self.assertEqual(code_publics(original,1),[(0,'__fstrncat')])
        self.assertEqual(externs(original),['__fmovmem','__fstrlen'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {15:(2,2),31:(2,2),71:(2,1)})
        self.assertEqual(bytes(P[1,i] for i in range(89,93)),
                         bytes.fromhex('26c60700'))
        expect=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['fstrncat']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expect)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
