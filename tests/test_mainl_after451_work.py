"""Source-bound complete Borland stdiobuf destructor with true virtual flush."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after451_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after451_work import review
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='stdiobuf-virtual-destructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalStdiobufDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native original destructor missing')
    def test_complete_original_bytes_and_fresh_native_producers(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,659,234))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (224,177307))
        self.assertEqual((r['profiles']['sdbdtr']['CODE_bytes'],
                          r['profiles']['sdbdtr']['DATA_bytes']),(224,52))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original destructor OMF absent')
    def test_original_virtual_flush_and_all_nineteen_symbolic_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['sdbdtr']['index']]
        self.assertEqual(m.name,'sdbdtr')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),276)
        self.assertEqual(len(F),19)
        self.assertEqual(code_publics(orig,1),[(0,'@stdiobuf@$bdtr$qv')])
        self.assertEqual(externs(orig),NATIVE['sdbdtr']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(52)),bytes.fromhex('6000')+bytes(50))
        self.assertIn(b'stdiobuf\0',bytes(P[1,i] for i in range(224)))
        fields={(f['segment'],f['site']):f for f in F}
        self.assertEqual((fields[1,37]['target_method'],fields[1,37]['target'],
                          fields[1,37]['addend']),(0,2,8))
        self.assertEqual((fields[2,0]['target_method'],fields[2,0]['target'],
                          fields[2,0]['addend']),(0,1,96))
        self.assertEqual((fields[2,8]['target_method'],fields[2,8]['target']), (0,1))
        self.assertEqual((fields[1,66]['target_method'],fields[1,66]['target']), (2,3))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['sdbdtr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
