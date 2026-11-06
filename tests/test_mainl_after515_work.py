"""Original Borland farcalloc: 32-bit size, segmented zeroing and near pointer advance."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after515_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after515_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='farcalloc-32bit-segmented-zeroing-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalFarCalloc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.is_file():raise unittest.SkipTest('native original fcalloc receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['fcalloc']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_entire_original_member_two_complete_native_links(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,723,170))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(148,193732))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_genuine_chunked_far_heap_zeroing_and_exact_omf(self):
        P=payload(self.original);F=literal_fields(self.original)
        self.assertEqual(len(P),148)
        self.assertEqual(code_publics(self.original,1),[(0,'_farcalloc')])
        self.assertEqual(externs(self.original),
                         ['_farmalloc','_setmem','N_LXMUL@','N_PADA@'])
        self.assertEqual([(f['site'],f['target_method'],f['target'])
                          for f in sorted(F,key=lambda f:f['site'])],
                         [(21,2,3),(32,2,1),(98,2,2),(116,2,4)])
        self.assertEqual(len(F),4)
        for row in self.receipt['rounds']:
            made=(ROOT/row['outputs']['fcalloc']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fcalloc'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
