"""Original Japanese PC-98 cursor control: complete CODE, DATA, and native link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after395_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after395_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics

MODE='pc98-cursor-control-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalPc98CursorControl(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound PC98 cursor receipt absent')
    def test_full_cursor_boss_and_native_original_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,536,357))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (346,161608))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(r['profiles']['cneccrsr']['DATA_bytes'],12)
        self.assertEqual(r['profiles']['cneccrsr']['BSS_bytes'],0)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound PC98 cursor receipt absent')
    def test_original_esc_mode_data_group_order_and_seven_literal_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cneccrsr']['index']]
        self.assertEqual(m.name,'cneccrsr')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),358)
        self.assertEqual(code_publics(original,1),[(168,'___nec_setcursortype')])
        self.assertEqual(bytes(P[2,i] for i in range(12)),b'\x1b[>5l\0\x1b[>5h\0')
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(len(F),7)
        self.assertEqual([(F[i]['site'],F[i]['addend']) for i in range(2)],
                         [(193,6),(200,0)])
        report=json.loads(RECEIPT.read_text())
        for row in report['rounds']:
            blob=(ROOT/row['outputs']['cneccrsr']['path']).read_bytes()
            self.assertEqual(payload(blob),P)
            self.assertEqual(literal_fields(blob),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['cneccrsr'])
            self.assertFalse(row['original_program_equal_by_member']['cneccrsr'])
            self.assertEqual([x.data.hex() for x in parse_omf(blob) if x.name=='GRPDEF'],
                             ['08ff03ff02'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
