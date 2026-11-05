"""Original PC-98 hardware equipment probe, x87 and in-CODE IEEE constant."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after415_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after415_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='pc98-equipment-fpu-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalPc98Equipment(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound equipment native receipt absent')
    def test_complete_original_hardware_probe_and_native_pair(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,591,302))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (213,166683))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original/native equipment pair absent')
    def test_genuine_inline_fpu_constant_two_relocations_and_flag_merge(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['pc98eqip']['index']]
        self.assertEqual(m.name,'pc98eqip')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),213)
        self.assertEqual(code_publics(original,1),[(0,'_pc98equip')])
        self.assertEqual([v.data.hex() for v in parse_omf(original) if v.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(bytes(P[1,i] for i in range(132,136)),
                         bytes.fromhex('0000807f'))
        self.assertEqual(bytes(P[1,i] for i in range(136,138)),
                         bytes.fromhex('0ac2'))  # merge floating capability bits
        self.assertIn(bytes.fromhex('dbe3'),bytes(P[1,i] for i in range(213)))
        self.assertEqual([(f['site'],f['frame_method'],f['target_method'],f['target'],
                           f['addend']) for f in F],
                         [(97,5,0,1,132),(106,5,0,1,132)])
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['pc98eqip']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['pc98eqip'])
            self.assertFalse(row['original_program_equal_by_member']['pc98eqip'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
