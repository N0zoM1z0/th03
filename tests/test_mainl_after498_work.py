"""Native original DOS four-entry file creation family and ordered OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after498_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after498_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-create-family-four-far-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosCreateFamily(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS create source proof absent')
    def test_original_code_and_both_complete_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,706,187))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(170,186165))
        self.assertEqual((r['profiles']['creata']['CODE_bytes'],
                          r['profiles']['creata']['DATA_bytes']),(170,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original file-create OMF absent')
    def test_private_core_public_offsets_and_all_literal_fixups(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['creata']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),170)
        self.assertEqual(code_publics(orig,1),[(55,'__rtl_creat'),(83,'__creat'),
                                              (108,'_creattemp'),(139,'_creatnew')])
        self.assertEqual(externs(orig),['__IOERROR','__openfd','__fmode'])
        self.assertEqual([(f['site'],f['target_method'],f['target'],
                           f['frame_method']) for f in sorted(F,key=lambda f:f['site'])],
                         [(36,2,2,1),(45,2,1,0),(126,2,3,1),(157,2,3,1)])
        self.assertEqual(len(F),4)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['creata']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['creata'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
