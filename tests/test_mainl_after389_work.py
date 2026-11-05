"""Original DOS _locking boss: complete code, jump table, OMF and native link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 7000))
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after389_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after389_work import review
from lib.pc98 import parse_mz

class OriginalDosLocking(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX+'dos-file-locking-boss-build.json')).is_file(),
                         'native source-linked _locking receipt absent')
    def test_all_original_code_relocations_and_both_native_rounds(self):
        record = review('dos-file-locking-boss')
        self.assertEqual((record['original_CRT_members'],record['native_source_members'],
                          record['untouched_vendor_members']), (893,512,381))
        self.assertEqual((record['added_CODE_bytes'],record['source_CRT_CODE_bytes']),
                         (310,159421))
        self.assertTrue(record['complete_original_CODE_DATA_equal'])
        self.assertTrue(record['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(record['original_literal_FIXUPP_equal'])
        self.assertFalse(record['original_library_member_program_equal'])
        self.assertFalse(record['source_acceptance'])
        self.assertFalse(record['original_cold_rebuilt'])
        self.assertEqual((record['native_rounds'],record['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT / (PREFIX+'dos-file-locking-boss-build.json')).is_file(),
                         'native two-round source receipt absent')
    def test_original_jump_table_and_literal_fixup_order_gap(self):
        _,_,_,members,_,_ = retained()
        o=original_library_member(members[NATIVE['locking']['index']])
        op=payload(o); of=literal_fields(o)
        self.assertEqual(bytes(op[1,i] for i in range(300,310)),
                         bytes.fromhex('f9009900dc009900dc00'))
        self.assertEqual(len(of),16)
        self.assertEqual([x['site'] for x in of[:5]],[308,306,304,302,300])
        record=json.loads((ROOT / (PREFIX+'dos-file-locking-boss-build.json')).read_text())
        keys=('segment','site','location_type','width','segment_relative',
              'frame_method','frame','target_method','target','addend')
        expected=sorted(tuple(f[k] for k in keys) for f in of)
        for row in record['rounds']:
            made=(ROOT / row['outputs']['locking']['path']).read_bytes()
            self.assertEqual(payload(made),op)
            mf=literal_fields(made)
            self.assertEqual(sorted(tuple(f[k] for k in keys) for f in mf),expected)
            self.assertNotEqual(mf,of)  # Honest Borland/TASM chronology gap.
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['locking'])
            exe=(ROOT / row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK / 'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__ == '__main__': unittest.main()
