"""Eight complete original Japanese MBCS, far-string, BGI and C++ leaves."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after411_work import (PREFIX,WORK,MODES,NATIVE,
    retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after411_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz

MODE='eight-mbcs-string-bgi-leaves'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalEightMbcsStringBgiLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound eight-leaf CRT receipt absent')
    def test_complete_original_source_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,587,306))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (335,165913))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'eight-leaf native CRT vectors absent')
    def test_all_eight_code_and_original_fixups_no_hidden_frame_gaps(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),8)
        self.assertFalse(set(names)&set(carry[0][0]))
        record=json.loads(RECEIPT.read_text())
        record_order_gaps={'fstrset','gregistr'}
        for n in names:
            with self.subTest(member=n):
                original=original_library_member(members[NATIVE[n]['index']])
                P=payload(original)
                F=literal_fields(original)
                self.assertEqual(len(P),NATIVE[n]['code'])
                self.assertEqual(len(F),NATIVE[n]['fields'])
                self.assertEqual(code_publics(original,1),NATIVE[n]['publics'])
                self.assertEqual(externs(original),NATIVE[n]['imports'])
                for row in record['rounds']:
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(scope(n,made),scope(n,original))
                    self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                            for f in literal_fields(made)),
                                     sorted(tuple(f[k] for k in KEYS) for f in F))
                    self.assertEqual(literal_fields(made)==F,n not in record_order_gaps)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],
                                     n not in record_order_gaps)
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__ == '__main__': unittest.main()
