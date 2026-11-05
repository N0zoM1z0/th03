"""Complete original xmsg C++ RTTI/exception boss with original ordered MZ."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after327_work import NATIVE, PREFIX, WORK, retained, original_library_member
from build_th03_mainl_display_work import literal_fields, payload
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after327_work import review

ORIGINAL_FIVE_APIS = [
    (36, '@xmsg@$bctr$qmx6string'),
    (239, '@xmsg@$bctr$qmx4xmsg'),
    (410, '@xmsg@$bdtr$qv'),
    (518, '@xmsg@raise$qv'),
    (637, '@xmsg@$basg$qmx4xmsg'),
]
ORIGINAL_XMSG_RELOCATIONS = [
    927, 884, 852, 752, 705, 644, 601, 546, 525,
    512, 504, 474, 326, 246, 203, 119, 43, 0,
]


class OriginalXmsgExceptionBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'xmsg-exception-boss-build.json')).exists(),
                         'local native xmsg boss receipts unavailable')
    def test_entire_original_native_xmsg_and_exact_link(self):
        r = review('xmsg-exception-boss')
        p = r['profiles']['xmsg']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 332, 561))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (955, 110841))
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (955, 0, 0))
        self.assertEqual(p['publics'], ORIGINAL_FIVE_APIS)
        self.assertEqual(p['imports'], [
            '@$bnew$qui', '@$bdele$qnv', '@__RefDestructorCount$qv',
            '@_ThrowException$qnvt1t1t1uiuiuinuc',
            '___InitExceptBlocks', '___ExitExceptBlocks',
            '@string@$bctr$qmx6string', '@string@$bdtr$qv',
        ])
        self.assertEqual(len(p['relocation_sites_targets']), 49)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'xmsg-exception-boss-build.json')).exists(),
                         'original and produced native full source receipts absent')
    def test_all_original_fields_and_ordered_18_dos_mz_entries(self):
        _, _, _, members, _, _ = retained()
        original = original_library_member(members[NATIVE['xmsg']['index']])
        r = json.loads((ROOT / (PREFIX + 'xmsg-exception-boss-build.json')).read_text())
        original_fields = literal_fields(original)
        self.assertEqual(len(original_fields), 49)
        self.assertEqual(original_fields[0]['site'], 927)
        self.assertEqual(original_fields[-1]['site'], 0)
        orig_mz = parse_mz((WORK / 'bin/th03/mainl.target.exe').read_bytes())
        assert_sites = lambda mz: [mz.relocations[i].offset - 21588 for i in range(508, 526)]
        self.assertEqual(assert_sites(orig_mz), ORIGINAL_XMSG_RELOCATIONS)
        for row in r['rounds']:
            with self.subTest(round=row['round']):
                made = (ROOT / row['outputs']['xmsg']['path']).read_bytes()
                fields = literal_fields(made)
                self.assertEqual(payload(made), payload(original))
                self.assertEqual(sorted(tuple(sorted(f.items())) for f in fields),
                                 sorted(tuple(sorted(f.items())) for f in original_fields))
                self.assertNotEqual(fields, original_fields)
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['xmsg']['index']].program_records)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['xmsg'])
                mz = parse_mz((ROOT / row['outputs']['exe']['path']).read_bytes())
                self.assertEqual(len(mz.relocations), 677)
                self.assertEqual(assert_sites(mz), ORIGINAL_XMSG_RELOCATIONS)


if __name__ == '__main__':
    unittest.main()
