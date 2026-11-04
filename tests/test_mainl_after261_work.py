"""Original NEC PC-98 CRT init and screen fill/move native proof."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after261_work import PREFIX,WORK
from review_th03_mainl_after261_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalNECVideoCore(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'nec-video-core-build.json')).exists(),
                         '263-source original Japanese native vectors absent')
    def test_original_nec_video_init_and_screen_product(self):
        r=review('nec-video-core')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,263,630))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (542,98203))
        init,scrn=r['profiles']['cnecinit'],r['profiles']['cnecscrn']
        self.assertEqual((init['CODE_bytes'],scrn['CODE_bytes']),(209,333))
        self.assertEqual(init['publics'],[(0,'___nec_c0crtinit'),
            (145,'___nec_get_screen_height'),(165,'___nec_get_windowy2'),
            (195,'__NEC_VIDEOINT18'),(202,'__NEC_VIDEOINTDC')])
        self.assertEqual(scrn['publics'],[(64,'__NEC_ZAP_LINE'),
                                         (179,'__NEC_MOVELINE')])
        self.assertEqual(init['imports'],['__directvideo','__video'])
        self.assertEqual(scrn['imports'],['__wclrnorm','__wgarbage','__video'])
        self.assertEqual((len(init['relocation_sites_targets']),
                          len(scrn['relocation_sites_targets'])),(19,10))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'nec-video-core-build.json')).exists(),
                         'actual original NEC CRT OBJ pair missing')
    def test_literal_29_original_omf_fixups_and_modrm_xchg(self):
        r=json.loads((ROOT/(PREFIX+'nec-video-core-build.json')).read_text())
        for name,expected in [('cnecinit',19),('cnecscrn',10)]:
            orig=(WORK/'vendor'/(name+'.obj')).read_bytes()
            fs=literal_fields(orig)
            self.assertEqual(len(fs),expected)
            for row in r['rounds']:
                made=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(orig),payload(made))
                self.assertEqual(fs,literal_fields(made))
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
        p=payload((WORK/'vendor/cnecscrn.obj').read_bytes())
        for offset in (150,157,311):
            self.assertEqual(bytes(p[1,i] for i in (offset,offset+1)),
                             bytes.fromhex('87fe'))
