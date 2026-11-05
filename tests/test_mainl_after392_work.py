"""Original 343-byte Borland vector_delete boss and source-bound native pair."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 7000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after392_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after392_work import review
from lib.pc98 import parse_mz

MODE = 'vector-destructor-boss'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
KEYS = ('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')

class OriginalVectorDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound native vector destructor receipt absent')
    def test_exact_original_boss_and_two_full_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,532,361))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (343,160332))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'source-bound native vector destructor receipt absent')
    def test_seven_word_dispatch_entries_and_one_far_delete(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['vdel']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),343)
        self.assertEqual(bytes(P[1,i] for i in range(329,343)),
                         bytes.fromhex('9400a200b000bc00c800da00ec00'))
        self.assertEqual([f['site'] for f in F],
                         [341,339,337,335,333,331,329,317,146])
        self.assertEqual([f['addend'] for f in F[:7]],
                         [236,218,200,188,176,162,148])
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            b=(ROOT / row['outputs']['vdel']['path']).read_bytes()
            self.assertEqual(payload(b),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(b)),
                             sorted(tuple(f[k] for k in KEYS) for f in F))
            self.assertNotEqual(literal_fields(b),F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['vdel'])
            exe=(ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__ == '__main__': unittest.main()
