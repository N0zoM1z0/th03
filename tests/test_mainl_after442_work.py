"""Original 176-byte streambuf::setb far-buffer ownership implementation."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after442_work import PREFIX, WORK, NATIVE, retained, original_library_member
from review_th03_mainl_after442_work import review
from build_th03_mainl_display_work import payload, literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='streambuf-setb-buffer-management'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalStreambufSetb(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound setb receipt missing')
    def test_exact_original_and_both_native_producer_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,650,243))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (176,175278))
        self.assertEqual((r['profiles']['stbsetb']['CODE_bytes'],
                          r['profiles']['stbsetb']['DATA_bytes']),(176,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original setb OMF missing')
    def test_far_delete_original_literal_fixupp_and_complete_code(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['stbsetb']['index']]
        self.assertEqual(m.name,'stbsetb')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),176)
        self.assertEqual(len(F),1)
        self.assertEqual(code_publics(orig,1),
                         [(0,'@streambuf@setb$qnct1i')])
        self.assertEqual(externs(orig),['@$bdla$qnv'])
        self.assertEqual((F[0]['segment'],F[0]['site'],
                          F[0]['target_method'],F[0]['target']),
                         (1,55,2,1))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['stbsetb']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['stbsetb'])
            self.assertFalse(row['original_program_equal_by_member']['stbsetb'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
