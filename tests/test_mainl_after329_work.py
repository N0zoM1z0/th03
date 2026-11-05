"""Whole Japanese Borland TRegexp constructor/destructor/pattern/RTTI member."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after329_work import PREFIX, WORK, NATIVE, original_library_member, retained
from build_th03_mainl_display_work import literal_fields, payload
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after329_work import review

REGEXP_PUBLICS = [
    (0, '@TRegexp@$bctr$qnxc'),
    (81, '@TRegexp@$bctr$qmx7TRegexp'),
    (162, '@TRegexp@$bdtr$qv'),
    (233, '@TRegexp@copy_pattern$qmx7TRegexp'),
    (332, '@TRegexp@gen_pattern$qnxc'),
]


class OriginalTRegexpBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'regexp-boss-build.json')).is_file(),
                         'local native 341-source TRegexp receipts absent')
    def test_full_two_code_segment_regexp_exception_boss(self):
        r = review('regexp-boss')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 341, 552))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (649, 111706))
        p = r['profiles']['regexp']
        self.assertEqual((p['TEXT_bytes'], p['TEXTC_bytes'], p['CODE_bytes'],
                          p['DATA_bytes'], p['BSS_bytes']), (110, 539, 649, 2, 0))
        self.assertEqual(p['publics'], REGEXP_PUBLICS)
        self.assertEqual(p['data_publics'], [(0, '@TRegexp@maxpat')])
        self.assertEqual(p['bss_publics'], [])
        self.assertEqual(p['imports'], [
            '@$bnew$qui', '@$bnwa$qui', '@$bdele$qnv',
            '@__RefDestructorCount$qv', '___InitExceptBlocks',
            '___ExitExceptBlocks', '@xmsg@$bdtr$qv', '_memcpy',
            '@makepat$qnxcnucui',
        ])
        self.assertEqual(len(p['relocation_sites_targets']), 31)
        self.assertEqual([x[1] for x in p['relocation_sites_targets']
                          if x[0] == 4 and x[7] == 0 and x[8] == 4],
                         [46, 127, 463])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'regexp-boss-build.json')).is_file(),
                         'original and source-producer raw OBJ/EXE pair absent')
    def test_all_original_segment_payloads_frames_and_stable_exe_relocations(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['regexp']['index']]
        self.assertEqual(m.name, 'regexp')
        original = original_library_member(m)
        receipt = json.loads((ROOT / (PREFIX + 'regexp-boss-build.json')).read_text())
        original_fields = literal_fields(original)
        self.assertEqual(len(original_fields), 31)
        self.assertEqual(original_fields[0]['site'], 94)
        self.assertEqual(original_fields[-1]['site'], 18)
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                made = (ROOT / row['outputs']['regexp']['path']).read_bytes()
                self.assertEqual(payload(original), payload(made))
                self.assertEqual(sorted(tuple(sorted(f.items())) for f in original_fields),
                                 sorted(tuple(sorted(f.items())) for f in literal_fields(made)))
                self.assertNotEqual(literal_fields(original), literal_fields(made))
                self.assertNotEqual(m.program_records, object_program_records(made))
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['regexp'])
                self.assertEqual([r.data.hex() for r in parse_omf(made)
                                  if r.name == 'GRPDEF'], ['0aff02ff03'])
                self.assertEqual(bytes(payload(made)[2, i] for i in range(2)), b'\x80\x00')
                exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
                mz = parse_mz(exe)
                self.assertTrue(mz.valid)
                self.assertEqual(len(mz.relocations), 677)
                self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())


if __name__ == '__main__':
    unittest.main()
