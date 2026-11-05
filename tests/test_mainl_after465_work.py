"""Original DOS DBCS path initializer with source-bound INITDATA registration."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after465_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after465_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-dbcs-path-initializer-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalPathDbcsInitializer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound DBCS initializer absent')
    def test_full_initdata_original_and_native_two_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,673,220))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(208,180648))
        self.assertEqual((r['profiles']['_pathops']['CODE_bytes'],
                          r['profiles']['_pathops']['DATA_bytes'],
                          r['profiles']['_pathops']['INITDATA_bytes']),(208,16,6))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original INITDATA OMF missing')
    def test_far_dbcs_vector_publics_and_exact_init_code_pointer(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['_pathops']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),230)
        self.assertEqual(len(F),8)
        self.assertEqual(code_publics(original,1),
                         [(73,'___path_isdbcsleadbyte'),(110,'___path_issbcs')])
        self.assertEqual(code_publics(original,2),
                         [(0,'___path_dbcs_vector'),(4,'___path_dbcs_default')])
        self.assertEqual(externs(original),[])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['0aff03ff02'])
        self.assertEqual(bytes(P[2,i] for i in range(16)),bytes(16))
        self.assertEqual(bytes(P[4,i] for i in range(6)),
                         bytes.fromhex('000f00000000'))
        init_fixups=[f for f in F if f['segment']==4]
        self.assertEqual(len(init_fixups),1)
        self.assertEqual((init_fixups[0]['site'],init_fixups[0]['target_method'],
                          init_fixups[0]['target'],init_fixups[0]['addend']), (2,0,1,0))
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['_pathops']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertEqual(code_publics(made,2),code_publics(original,2))
            self.assertTrue(round['literal_omf_fixupp_equal_by_member']['_pathops'])
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
