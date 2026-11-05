"""Complete IBM PC video VRAM copy, pointer and refresh hardware boss."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after410_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after410_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='ibm-text-vram-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalIbmVram(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound IBM VRAM native receipt absent')
    def test_complete_original_hardware_boss_and_native_pair(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,579,314))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (201,165578))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound original IBM VRAM OBJ absent')
    def test_three_original_near_abis_and_seven_literal_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cibmvram']['index']]
        self.assertEqual(m.name,'cibmvram')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),201)
        self.assertEqual(code_publics(orig,1),[
            (0,'__IBM_VPTR'),(36,'__IBM_VRAM'),(158,'__IBM_REFRESH_VRAM')])
        self.assertEqual(externs(orig),['__video','__IBM_VIDEOINTESDI'])
        self.assertEqual([f['site'] for f in F],[6,24,28,45,165,175,193])
        self.assertEqual([f['addend'] for f in F],[10,16,18,12,13,18,0])
        self.assertEqual([x.data.hex() for x in parse_omf(orig) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        raw=bytes(P[1,i] for i in range(201))
        self.assertIn(bytes.fromhex('bada03'),raw)  # I/O status port 03DAh
        self.assertIn(bytes.fromhex('f3a5'),raw)    # original REP MOVSW
        self.assertGreaterEqual(raw.count(b'\xfa'),2) # original CLI
        self.assertGreaterEqual(raw.count(b'\xfb'),2) # original STI
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['cibmvram']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['cibmvram'])
            self.assertFalse(row['original_program_equal_by_member']['cibmvram'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
