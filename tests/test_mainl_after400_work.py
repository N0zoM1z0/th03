"""Original Japanese DOS mktemp complete nested candidate enumerator."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),8000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after400_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after400_work import review
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
MODE='dos-mktemp-enumeration-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalDosMktemp(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound mktemp native receipt absent')
    def test_original_nested_filename_enumeration_and_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,550,343))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(253,162711))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(r['profiles']['mktemp']['DATA_bytes'],7)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native source and original objects absent')
    def test_entire_original_template_and_four_relocations(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['mktemp']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),260)
        self.assertEqual(code_publics(original,1),[(0,'_mktemp')])
        self.assertEqual(bytes(P[2,i] for i in range(7)),b'XXXXXX\0')
        self.assertEqual([f['site'] for f in F],[175,58,50,15])
        self.assertEqual([f['target_method'] for f in F],[2,2,0,2])
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['mktemp']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['mktemp'])
            self.assertFalse(row['original_program_equal_by_member']['mktemp'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
