"""Six original stdio inlined macro ABI entrypoints and real stream state."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after457_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after457_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='stdio-six-inline-entrypoints-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
PUBLICS=[(0,'_getc'),(51,'_getchar'),(89,'_putchar'),(138,'_putc'),
         (196,'_feof'),(215,'_ferror')]

class OriginalStdioMacroABI(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native stdio source receipt absent')
    def test_native_both_rounds_original_and_literal_omf(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,665,228))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (234,178597))
        self.assertEqual((r['profiles']['iomacro']['CODE_bytes'],
                          r['profiles']['iomacro']['DATA_bytes']),(234,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original module OMF absent')
    def test_six_publics_file_state_and_every_ordered_fixupp(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['iomacro']['index']]
        self.assertEqual(m.name,'iomacro')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),234)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(orig,1),PUBLICS)
        self.assertEqual(externs(orig),['__streams','__fgetc','__fputc'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        site_to_target={f['site']:(f['target_method'],f['target'],f['addend']) for f in F}
        self.assertEqual(site_to_target[41],(2,2,0))
        self.assertEqual(site_to_target[127],(2,3,0))
        self.assertEqual(site_to_target[185],(2,3,0))
        self.assertEqual(site_to_target[105],(2,1,32))
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['iomacro']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['iomacro'])
            self.assertEqual(code_publics(made,1),PUBLICS)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
