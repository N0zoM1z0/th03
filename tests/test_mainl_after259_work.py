"""Actual original PC-98 NEC three screen text APIs native source proof."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after259_work import PREFIX,WORK
from review_th03_mainl_after259_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalNECScreenText(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'nec-screen-text-build.json')).exists(),
                         'original 260-source native proof missing')
    def test_3_complete_NEС_text_apis_and_full_original_link(self):
        r=review('nec-screen-text')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,260,633))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (475,97156))
        p=r['profiles']['cnecgptx']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),(475,0,0))
        self.assertEqual(p['publics'],[(0,'___nec_gettext'),(106,'___nec_puttext'),
                                       (446,'___nec_getputtextsize')])
        self.assertEqual(p['imports'],['__wgarbage','__video','__VALIDATEXY'])
        self.assertEqual(len(p['relocation_sites_targets']),9)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'nec-screen-text-build.json')).exists(),
                         'original NEC raw OBJ vectors missing')
    def test_all_9_original_ordered_omf_fields_and_raw_code(self):
        receipt=json.loads((ROOT/(PREFIX+'nec-screen-text-build.json')).read_text())
        original=(WORK/'vendor/cnecgptx.obj').read_bytes()
        f=literal_fields(original)
        self.assertEqual(len(f),9)
        self.assertEqual([x['site'] for x in f if x['frame_method']==0],[25,134])
        for rd in receipt['rounds']:
            obj=(ROOT/rd['outputs']['cnecgptx']['path']).read_bytes()
            self.assertEqual(payload(original),payload(obj))
            self.assertEqual(f,literal_fields(obj))
            self.assertTrue(rd['literal_omf_fixupp_equal_by_member']['cnecgptx'])
