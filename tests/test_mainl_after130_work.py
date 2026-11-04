"""Original Japanese PC-98 direct video screen source and literal OMF proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after130_work import PREFIX,WORK
from review_th03_mainl_after130_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalPC98Screen(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'cibmscrn-build.json')).is_file(),
                         '131-source original Japanese screen proof unavailable')
    def test_all_six_original_screen_functions_and_normal_link(self):
        r=review('cibmscrn')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,131,762))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (969,61806))
        p=r['profiles']['cibmscrn']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (969,0,0))
        self.assertEqual(p['publics'],[(396,'__IBM_SCREENIO'),
            (471,'__IBM_CHECK_DBCS_TRAIL'),(625,'__IBM_FILL_SPACE'),
            (691,'__IBM_OFF_CURSOR'),(733,'__IBM_SET_CURSOR'),
            (752,'__IBM_MOVELINE')])
        self.assertEqual(len(p['imports']),15)
        self.assertEqual(len(p['relocation_sites_targets']),30)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'cibmscrn-build.json')).is_file(),
                         'literal original screen OMF vectors unavailable')
    def test_all_30_relocations_have_original_order_and_frame_methods(self):
        r=json.loads((ROOT/(PREFIX+'cibmscrn-build.json')).read_text())
        original=(WORK/'vendor/cibmscrn.obj').read_bytes()
        o=literal_fields(original)
        self.assertEqual(len(o),30)
        self.assertEqual(len([x for x in o if x['target_method']==2]),30)
        for row in r['rounds']:
            made=(ROOT/row['outputs']['cibmscrn']['path']).read_bytes()
            self.assertEqual(payload(original),payload(made))
            self.assertEqual(o,literal_fields(made))
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['cibmscrn'])
