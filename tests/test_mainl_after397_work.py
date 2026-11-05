"""Original six NEC text-color APIs and complete 128-byte palette DATA."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after397_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after397_work import review
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics

MODE='pc98-text-color-attribute-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalNecTextColors(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound NEC text palette receipt absent')
    def test_native_original_palette_and_six_public_apis(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,538,355))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (222,162077))
        self.assertEqual((r['profiles']['cneccolr']['CODE_bytes'],
                          r['profiles']['cneccolr']['DATA_bytes']),(222,128))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound NEC text palette receipt absent')
    def test_all_four_native_color_tables_and_original_logical_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cneccolr']['index']]
        self.assertEqual(m.name,'cneccolr')
        original=original_library_member(m);P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),350)
        self.assertEqual(code_publics(original,1),[
            (0,'___nec_textcolor'),(52,'___nec_textbackground'),
            (90,'___nec_textattr'),(175,'___nec_highvideo'),
            (193,'___nec_lowvideo'),(211,'___nec_normvideo')])
        self.assertEqual([x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF'],
                         ['08ff02ff03'])
        d=bytes(P[2,i] for i in range(128))
        words=[int.from_bytes(d[i:i+2],'little') for i in range(0,128,2)]
        self.assertEqual(words[:8],[1,33,129,161,65,97,193,225])
        self.assertEqual(words[16:20],[1,0x1001,0x2001,0x3001])
        self.assertEqual(words[32:36],[0,2,4,6])
        self.assertEqual(words[48:52],[0x0800,0x0802,0x0804,0x0806])
        self.assertEqual(len(F),21)
        report=json.loads(RECEIPT.read_text())
        for row in report['rounds']:
            made=(ROOT/row['outputs']['cneccolr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual([x.data.hex() for x in parse_omf(made) if x.name=='GRPDEF'],
                             ['08ff02ff03'])
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['cneccolr'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
