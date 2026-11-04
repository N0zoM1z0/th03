"""Original Japanese Borland istream long integer extraction source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after116_work import PREFIX,WORK
from review_th03_mainl_after116_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalLongIntegerExtraction(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'istelng-build.json')).is_file(),
                         '117-source original Japanese native vectors unavailable')
    def test_complete_1439_byte_istream_boss_and_link(self):
        r=review('istelng')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,117,776))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1439,55809))
        p=r['profiles']['istelng']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (1439,0,0))
        self.assertEqual(p['publics'],[(811,'@istream@$brsh$qml')])
        self.assertEqual(p['imports'],[
            '@ios@clear$qi','@streambuf@do_snextc$qv',
            '@istream@ipfx$qi','__ctype','F_LXMUL@','F_LXLSH@'])
        self.assertEqual(len(p['relocation_sites_targets']),19)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'istelng-build.json')).is_file(),
                         'source-bound native istelng object pair unavailable')
    def test_all_19_original_fixup_sites_and_frames(self):
        receipt=json.loads((ROOT/(PREFIX+'istelng-build.json')).read_text())
        original=(WORK/'vendor/istelng.obj').read_bytes()
        lhs=literal_fields(original)
        self.assertEqual(len(lhs),19)
        key=lambda f:(f['segment'],f['site'])
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['istelng']['path']).read_bytes()
            self.assertEqual(payload(original),payload(obj))
            rhs=literal_fields(obj)
            self.assertEqual(sorted(lhs,key=key),sorted(rhs,key=key))
            self.assertNotEqual(lhs,rhs)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['istelng'])
