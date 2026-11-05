"""18 original CRT ABI leaves: full native members and preserved link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 7000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after391_work import (PREFIX, WORK, MODES, NATIVE,
    retained, original_library_member)
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after391_work import review

MODE = 'eighteen-runtime-abi-leaves'
RECEIPT = ROOT / (PREFIX + MODE + '-build.json')
FIXUP_KEYS = ('segment','site','location_type','width','segment_relative',
              'frame_method','frame','target_method','target','addend')

def logical(fields):
    return sorted(tuple(f[k] for k in FIXUP_KEYS) for f in fields)

class OriginalRuntimeLeaves(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(), 'two-round source receipt absent')
    def test_complete_native_replacement_and_source_bound_reproducibility(self):
        result = review(MODE)
        self.assertEqual((result['original_CRT_members'],result['native_source_members'],
                          result['untouched_vendor_members']), (893, 531, 362))
        self.assertEqual((result['added_CODE_bytes'],result['source_CRT_CODE_bytes']),
                         (268, 159989))
        self.assertEqual(len(result['profiles']), 18)
        self.assertEqual((result['native_rounds'],result['original_MZ_relocations']),
                         (2, 677))
        self.assertTrue(result['complete_original_CODE_DATA_equal'])
        self.assertTrue(result['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(result['original_literal_FIXUPP_equal'])
        self.assertFalse(result['original_library_member_program_equal'])
        self.assertFalse(result['source_acceptance'])
        self.assertFalse(result['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(), 'original CRT receipt absent')
    def test_each_of_eighteen_exact_code_fixups_and_group(self):
        _,_,_,members,carry,_ = retained()
        names=MODES[MODE]
        self.assertEqual(len(names),18)
        self.assertFalse(set(names) & set(carry[0][0]))
        record=json.loads(RECEIPT.read_text())
        self.assertEqual(set(record['rounds'][0]['outputs']),set(names)|{'lib','exe','map'})
        for n in names:
            orig=original_library_member(members[NATIVE[n]['index']])
            op=payload(orig)
            original_fixups=literal_fields(orig)
            self.assertEqual(members[NATIVE[n]['index']].name,n)
            for row in record['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),op)
                    self.assertEqual(logical(literal_fields(made)),logical(original_fixups))
                    self.assertEqual([x.data.hex() for x in parse_omf(made)
                                      if x.name=='GRPDEF'],
                                     [x.data.hex() for x in parse_omf(orig)
                                      if x.name=='GRPDEF'])
                    exact = n != 'stxalc'
                    self.assertEqual(literal_fields(made)==original_fixups,exact)
                    self.assertEqual(row['literal_omf_fixupp_equal_by_member'][n],exact)
        self.assertEqual([f['site'] for f in literal_fields(original_library_member(
            members[NATIVE['stxalc']['index']]))], [7,4])
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__ == '__main__': unittest.main()
