"""Original DOS putenv complete table replacement and full native pair."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after402_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after402_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
MODE='dos-putenv-environment-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalDosPutenv(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-bound putenv receipt absent')
    def test_all_original_environment_paths_and_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,552,341))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (261,163263))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original putenv OBJ absent')
    def test_complete_original_group_imports_and_ten_literal_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['putenv']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),261)
        self.assertEqual(code_publics(original,1),[(0,'_putenv')])
        self.assertEqual(externs(original),['_free','_malloc','__environ','__envSize'])
        self.assertEqual([r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual([f['site'] for f in F],
                         [35,162,169,178,198,204,211,215,220,230])
        self.assertEqual([f['target'] for f in F],[3,3,4,2,4,3,3,3,1,3])
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['putenv']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['putenv'])
            self.assertFalse(row['original_program_equal_by_member']['putenv'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
