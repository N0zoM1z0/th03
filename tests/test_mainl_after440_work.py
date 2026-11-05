"""Original streambuf base destructor and its 38-byte class RTTI layout."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after440_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after440_work import review
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz

MODE = 'streambuf-base-destructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')

class OriginalStreambufDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'native destructor receipt missing')
    def test_fresh_complete_source_link(self):
        r = review(MODE)
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 648, 245))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (153,174844))
        self.assertEqual((r['profiles']['stbdtr']['CODE_bytes'],
                          r['profiles']['stbdtr']['DATA_bytes']), (153,52))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']), (2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'native destructor OMF missing')
    def test_original_owned_buffer_cleanup_and_symbolic_type_metadata(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['stbdtr']['index']]
        self.assertEqual(m.name,'stbdtr')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),205)
        self.assertEqual(len(F),17)
        self.assertEqual(externs(orig),NATIVE['stbdtr']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(52)),
                         bytes.fromhex('5d00')+bytes(50))
        self.assertIn(b'streambuf\0',bytes(P[1,i] for i in range(153)))
        sites={(f['segment'],f['site']):f for f in F}
        self.assertEqual((sites[1,37]['target_method'],sites[1,37]['target'],
                          sites[1,37]['addend']), (0,2,8))
        self.assertEqual((sites[2,0]['target_method'],sites[2,0]['target'],
                          sites[2,0]['addend']), (0,1,93))
        self.assertEqual((sites[1,55]['target_method'],sites[1,55]['target']),
                         (2,2))  # owned far buffer delete[]
        self.assertEqual((sites[1,83]['target_method'],sites[1,83]['target']),
                         (2,1))  # object delete
        original_fields=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['stbdtr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),original_fields)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
