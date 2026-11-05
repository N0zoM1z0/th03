"""Original Borland streambuf(char far *, int) full constructor boss."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after441_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after441_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz

MODE='streambuf-buffer-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalStreambufBufferConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'new constructor native receipt missing')
    def test_entire_original_source_and_two_reproducible_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,649,244))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (258,175102))
        self.assertEqual((r['profiles']['stbctr2']['CODE_bytes'],
                          r['profiles']['stbctr2']['DATA_bytes']), (258,52))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']), (2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original constructor OMF missing')
    def test_real_buffer_and_typed_vtable(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['stbctr2']['index']]
        self.assertEqual(m.name,'stbctr2')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),310)
        self.assertEqual(len(F),16)
        self.assertEqual(code_publics(orig,1),[(0,'@streambuf@$bctr$qnci')])
        self.assertEqual(externs(orig),NATIVE['stbctr2']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(52)),
                         bytes.fromhex('c600')+bytes(50))
        self.assertIn(b'streambuf\0',bytes(P[1,i] for i in range(258)))
        fields={(f['segment'],f['site']):f for f in F}
        self.assertEqual((fields[1,42]['target_method'],fields[1,42]['target'],
                          fields[1,42]['addend']),(0,2,8))
        self.assertEqual((fields[2,0]['target_method'],fields[2,0]['target'],
                          fields[2,0]['addend']),(0,1,198))
        self.assertEqual((fields[1,18]['target_method'],fields[1,18]['target']),(2,1))
        self.assertEqual((fields[1,171]['target_method'],fields[1,171]['target']),(2,2))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['stbctr2']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['stbctr2'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
