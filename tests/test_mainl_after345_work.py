"""Complete native original farheap break/sbrk owner; real CL.LIB OMF evidence."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after345_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from lib.borland_library import object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_mainl_after345_work import review


class OriginalHeapBreakManager(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'heap-break-manager-build.json')).is_file(),
                         'local native 379-source original fbrk receipts absent')
    def test_complete_original_heap_break_and_japanese_link(self):
        r = review('heap-break-manager')
        p = r['profiles']['fbrk']
        self.assertEqual((r['original_CRT_members'], r['native_source_members'],
                          r['untouched_vendor_members']), (893, 379, 514))
        self.assertEqual((r['added_CODE_bytes'], r['source_CRT_CODE_bytes']),
                         (352, 125041))
        self.assertEqual((p['CODE_bytes'], p['DATA_bytes'], p['BSS_bytes']),
                         (352, 2, 0))
        self.assertEqual(p['publics'], [(142, '__brk'), (209, '__sbrk')])
        self.assertEqual(p['imports'], NATIVE['fbrk']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']), 33)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']),
                         (2, 677))

    @unittest.skipUnless((ROOT / (PREFIX + 'heap-break-manager-build.json')).is_file(),
                         'raw original/source heap break OMF pairs absent')
    def test_actual_library_not_alternate_vendor_obj_and_both_native_rounds(self):
        _, _, _, members, _, _ = retained()
        m = members[NATIVE['fbrk']['index']]
        self.assertEqual(m.name, 'fbrk')
        original = original_library_member(m)
        vendor = (WORK / 'vendor/fbrk.obj').read_bytes()
        self.assertEqual(payload(vendor), payload(original))
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name == 'GRPDEF'], ['08ff03ff02'])
        self.assertEqual([r.data.hex() for r in parse_omf(vendor)
                          if r.name == 'GRPDEF'], ['08ff02ff03'])
        self.assertNotEqual(externs(vendor), externs(original))
        orig_fields = literal_fields(original)
        vendor_fields = literal_fields(vendor)
        self.assertEqual(len(orig_fields), 33)
        norm = lambda blob: sorted(
            (f['segment'], f['site'], f['location_type'], f['width'],
             f['segment_relative'], f['target_method'],
             externs(blob)[f['target'] - 1] if f['target_method'] == 2 else f['target'],
             f['addend']) for f in literal_fields(blob))
        self.assertEqual(norm(original), norm(vendor))
        orig_by_site = {f['site']: f for f in orig_fields}
        vendor_by_site = {f['site']: f for f in vendor_fields}
        self.assertEqual({i for i in orig_by_site
                          if orig_by_site[i]['frame_method'] != vendor_by_site[i]['frame_method']},
                         {162, 181, 225, 266, 283, 302})
        record = json.loads((ROOT / (PREFIX + 'heap-break-manager-build.json')).read_text())
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                obj = (ROOT / row['outputs']['fbrk']['path']).read_bytes()
                self.assertEqual(payload(obj), payload(original))
                self.assertEqual(literal_fields(obj), orig_fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fbrk'])
                self.assertFalse(row['original_program_equal_by_member']['fbrk'])
                self.assertNotEqual(object_program_records(obj), m.program_records)
                exe = (ROOT / row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe, (WORK / 'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations), 677)


if __name__ == '__main__':
    unittest.main()
