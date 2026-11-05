"""Exact original DOS date/time formatting helper plus two public far APIs."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after394_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after394_work import review
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics

MODE='dos-date-time-format-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalDosDateTimeFormatter(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound DOS formatter native receipt absent')
    def test_complete_original_helper_and_two_far_date_time_entrypoints(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,535,358))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (272,161262))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound DOS formatter native receipt absent')
    def test_complete_original_two_imports_and_near_pascal_clean_up(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['strdate']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),272)
        self.assertEqual(code_publics(original,1),[(159,'__strdate'),(216,'__strtime')])
        self.assertEqual(bytes(P[1,i] for i in range(153,159)),
                         bytes.fromhex('5f5e5dc20c00'))
        self.assertEqual([f['site'] for f in F],[230,173])
        self.assertEqual([f['target'] for f in F],[2,1])
        self.assertEqual([f['location_type'] for f in F],[3,3])
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            b=(ROOT/row['outputs']['strdate']['path']).read_bytes()
            self.assertEqual(payload(b),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(b)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(b),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['strdate'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
