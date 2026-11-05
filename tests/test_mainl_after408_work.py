"""Original NEC PC-98 BIOS equipment, memory and time with x87 probe."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after408_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after408_work import review
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics

MODE='nec-bios-equipment-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalNecBiosEquipment(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound NEC BIOS equipment native receipt absent')
    def test_full_hardware_boss_and_two_original_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,577,316))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (262,165150))
        self.assertEqual((r['profiles']['bion_equ']['CODE_bytes'],
                          r['profiles']['bion_equ']['DATA_bytes']),(262,41))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original NEC BIOS source/native receipt absent')
    def test_x87_mouse_memory_time_original_code_and_literal_fixupp(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['bion_equ']['index']]
        self.assertEqual(m.name,'bion_equ')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),303)
        self.assertEqual(code_publics(original,1),[
            (0,'__necpc_bios_equiplist'),
            (207,'__necpc_bios_memsize'),
            (231,'__necpc_bios_timeofday')])
        self.assertEqual(bytes(P[2,i] for i in range(41)),
                         b'*** This is Copyright 1983 Microsoft ***\0')
        self.assertEqual(bytes(P[1,i] for i in (11,12)),bytes.fromhex('dbe3'))
        self.assertEqual(bytes(P[1,i] for i in (125,126)),bytes.fromhex('cd33'))
        self.assertEqual(bytes(P[1,i] for i in (254,255)),bytes.fromhex('cd1c'))
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(len(F),1)
        self.assertEqual((F[0]['site'],F[0]['frame_method'],F[0]['frame'],
                          F[0]['target_method'],F[0]['target']),
                         (107,1,1,0,2))
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['bion_equ']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['bion_equ'])
            self.assertFalse(row['original_program_equal_by_member']['bion_equ'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
