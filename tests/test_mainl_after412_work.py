"""Original NEC PC-98 BIOS disk INT 1Bh and firmware parameter block."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after412_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after412_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='nec-bios-disk-controller-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalNecBiosDisk(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-bound NEC disk receipt absent')
    def test_full_disk_boss_and_original_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,588,305))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (171,166084))
        self.assertEqual((r['profiles']['bion_dsk']['CODE_bytes'],
                          r['profiles']['bion_dsk']['DATA_bytes']),(171,8))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original NEC disk program absent')
    def test_original_int1b_opcode_table_and_code_data_fixupp(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['bion_dsk']['index']]
        self.assertEqual(m.name,'bion_dsk')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),179)
        self.assertEqual(code_publics(original,1),[(0,'__necpc_bios_disk')])
        self.assertEqual(externs(original),[])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual(bytes(P[2,i] for i in range(8)),
                         bytes.fromhex('060510010a090c02'))
        self.assertIn(bytes.fromhex('cd1b'),bytes(P[1,i] for i in range(171)))
        self.assertEqual([(f['site'],f['frame_method'],f['frame'],f['target_method'],
                           f['target'],f['addend']) for f in F],[(99,1,1,0,2,0)])
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['bion_dsk']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['bion_dsk'])
            self.assertFalse(row['original_program_equal_by_member']['bion_dsk'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
