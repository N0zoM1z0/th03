"""Entire original NEC PC-98 BIOS serial controller and native two-round link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after409_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after409_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='nec-bios-serial-controller-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalNecBiosSerial(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-bound NEC serial receipt absent')
    def test_complete_original_serial_boss_and_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,578,315))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (227,165377))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original serial member and two rounds absent')
    def test_original_three_int_dispatches_and_zero_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['bion_com']['index']]
        self.assertEqual(m.name,'bion_com')
        o=original_library_member(m);P=payload(o)
        self.assertEqual(len(P),227)
        self.assertEqual(code_publics(o,1),[(0,'__necpc_bios_serialcom')])
        self.assertEqual(externs(o),[])
        self.assertEqual(literal_fields(o),[])
        self.assertEqual([(q['name'],q['class'],q['size'])
                          for q in segment_definitions(o)],
                         [('_TEXT','CODE',227),('_DATA','DATA',0),('_BSS','BSS',0)])
        self.assertEqual([r.data.hex() for r in parse_omf(o) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        for code in (bytes.fromhex('cd19'),bytes.fromhex('cdd4'),bytes.fromhex('cdd5')):
            self.assertIn(code,bytes(P[1,i] for i in range(227)))
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['bion_com']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),[])
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['bion_com'])
            self.assertFalse(row['original_program_equal_by_member']['bion_com'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__': unittest.main()
