"""Original Japanese PC-98 complete screen text get/put and native product."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after133_work import PREFIX,WORK
from review_th03_mainl_after133_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalPC98GetPutText(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'cibmgptx-build.json')).is_file(),
                         'two original Japanese 134-source output vectors absent')
    def test_complete_three_public_pc98_text_API_and_product(self):
        r=review('cibmgptx')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,134,759))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (554,63456))
        p=r['profiles']['cibmgptx']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (554,0,0))
        self.assertEqual(p['publics'],[(0,'___ibm_gettext'),
                                     (227,'___ibm_puttext'),
                                     (527,'___ibm_getputtextsize')])
        self.assertEqual(len(p['imports']),10)
        self.assertEqual(len(p['relocation_sites_targets']),25)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'cibmgptx-build.json')).is_file(),
                         'original get/put native OBJ vectors absent')
    def test_literal_original_OMF_fixups_including_record_order(self):
        r=json.loads((ROOT/(PREFIX+'cibmgptx-build.json')).read_text())
        original=(WORK/'vendor/cibmgptx.obj').read_bytes()
        f=literal_fields(original)
        self.assertEqual(len(f),25)
        for rd in r['rounds']:
            made=(ROOT/rd['outputs']['cibmgptx']['path']).read_bytes()
            self.assertEqual(payload(original),payload(made))
            self.assertEqual(f,literal_fields(made))
            self.assertTrue(rd['literal_omf_fixupp_equal_by_member']['cibmgptx'])

    def test_133_source_ancestry_audited_once(self):
        from build_th03_mainl_after133_work import retained
        base,files,accepted,members,carrier,parent_hash=retained()
        self.assertEqual(len(members),893)
        self.assertEqual(len(carrier),2)
        self.assertEqual(len(carrier[0][0]),133)
        self.assertEqual(carrier[0][0],carrier[1][0])
        self.assertIn('cibmscrn',carrier[0][0])
        self.assertIn('cibminit',carrier[0][0])
        self.assertIn('cibmputn',carrier[0][0])
