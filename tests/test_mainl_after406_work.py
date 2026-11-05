"""Complete original ostream << streambuf C++ transfer and native link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after406_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after406_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz

MODE='ostream-streambuf-insertion-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalOstreamStreambufInsertion(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound ostream insertion receipt absent')
    def test_entire_original_ostream_insertion_and_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,564,329))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (290,164492))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound ostream insertion receipt absent')
    def test_complete_code_virtual_calls_and_three_far_import_sites(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['ostibuf']['index']]
        self.assertEqual(m.name,'ostibuf')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),290)
        self.assertEqual(code_publics(original,1),[(0,'@ostream@$blsh$qn9streambuf')])
        self.assertEqual(externs(original),
                         ['@ios@setstate$qi','@ostream@do_opfx$qv',
                          '@ostream@do_osfx$qv'])
        self.assertEqual([f['site'] for f in F],[270,173,28])
        self.assertEqual([f['target'] for f in F],[3,1,2])
        self.assertEqual([f['location_type'] for f in F],[3,3,3])
        report=json.loads(RECEIPT.read_text())
        for row in report['rounds']:
            made=(ROOT/row['outputs']['ostibuf']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['ostibuf'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
