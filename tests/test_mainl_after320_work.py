"""Native full-member filebuf open source proof on the 320-source carrier."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after320_work import PREFIX, WORK
from review_th03_mainl_after320_work import review
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import parse_omf


class OriginalFilebufOpen(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'filebuf-open-build.json')).is_file(),
                         '321-source native outputs missing')
    def test_full_original_japanese_mainl(self):
        r = review('filebuf-open')
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 321, 572))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (346, 105526))
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])
        q = r['profiles']['fsbopen']
        self.assertEqual((q['CODE_bytes'], q['DATA_bytes'], q['BSS_bytes']),
                         (346, 0, 0))
        self.assertEqual(q['publics'], [(0, '@filebuf@open$qnxcii')])
        self.assertEqual(q['imports'], [
            '_lseek', '_open', '@streambuf@setp$qnct1',
            '@streambuf@setg$qnct1t1'])
        self.assertEqual([f[1] for f in q['relocation_sites_targets']],
                         [122, 176, 293, 327])

    @unittest.skipUnless((ROOT / (PREFIX + 'filebuf-open-build.json')).is_file(),
                         'native raw OBJ outputs missing')
    def test_original_sections_logical_frames_and_record_order_gap(self):
        r = json.loads((ROOT / (PREFIX + 'filebuf-open-build.json')).read_text())
        old = (WORK / 'vendor/fsbopen.obj').read_bytes()
        group = [x.data.hex() for x in parse_omf(old) if x.name == 'GRPDEF']
        self.assertEqual(group, ['08ff02ff03'])
        for row in r['rounds']:
            got = (ROOT / row['outputs']['fsbopen']['path']).read_bytes()
            self.assertEqual(payload(got), payload(old))
            self.assertEqual(
                [x.data.hex() for x in parse_omf(got) if x.name == 'GRPDEF'],
                group)
            frames = lambda blob: sorted(
                tuple(sorted(f.items())) for f in literal_fields(blob))
            self.assertEqual(frames(got), frames(old))
            self.assertNotEqual(literal_fields(got), literal_fields(old))
            self.assertFalse(
                row['literal_omf_fixupp_equal_by_member']['fsbopen'])
