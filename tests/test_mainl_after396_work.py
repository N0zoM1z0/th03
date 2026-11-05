"""Original 247-CODE/4-BSS PC-98 text VRAM output, exact ordered OMF."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after396_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after396_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics

MODE='pc98-text-vram-output-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalPc98TextVramOutput(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound PC98 text VRAM receipt absent')
    def test_complete_vram_output_and_native_original_exe_map(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,537,356))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (247,161855))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual((r['profiles']['cnecputn']['CODE_bytes'],
                          r['profiles']['cnecputn']['BSS_bytes']),(247,4))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound PC98 text VRAM receipt absent')
    def test_all_four_original_apis_and_twenty_one_literal_omf_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cnecputn']['index']]
        self.assertEqual(m.name,'cnecputn')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),247)
        self.assertEqual(code_publics(original,1),[
            (0,'__NEC_RESET_VRAM_ACCESS'),(11,'__NEC_START_VRAM_ACCESS'),
            (94,'__NEC_END_VRAM_ACCESS'),(160,'__NEC_OUTPUT_CHAR')])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(len(F),21)
        self.assertEqual([(F[i]['site'],F[i]['frame_method'],F[i]['target_method'])
                          for i in (0,2,6,11,20)],
                         [(4,1,0),(21,5,2),(43,1,0),(105,5,2),(239,1,0)])
        report=json.loads(RECEIPT.read_text())
        for row in report['rounds']:
            blob=(ROOT/row['outputs']['cnecputn']['path']).read_bytes()
            self.assertEqual(payload(blob),P)
            self.assertEqual(literal_fields(blob),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['cnecputn'])
            self.assertFalse(row['original_program_equal_by_member']['cnecputn'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
