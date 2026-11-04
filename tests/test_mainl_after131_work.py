"""Original PC-98 video initialization and VRAM counted output chain."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after131_work import PREFIX,WORK
from review_th03_mainl_after131_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalPC98VideoChain(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'video-chain-build.json')).is_file(),
                         '133-source native PC-98 video proof absent')
    def test_two_original_video_members_and_entire_exe_map(self):
        r=review('video-chain')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,133,760))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1096,62902))
        p,q=r['profiles']['cibminit'],r['profiles']['cibmputn']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (663,7,0))
        self.assertEqual((q['CODE_bytes'],q['DATA_bytes'],q['BSS_bytes']),
                         (433,0,12))
        self.assertEqual(p['publics'],[(67,'__IBM_VIDEOINT'),
            (243,'__IBM_VIDEOINTESDI'),(269,'__IBM_VIDEOINTESBP'),
            (324,'___ibm_c0crtinit'),(359,'___ibm_crtinit'),
            (612,'___ibm_get_screen_height'),(633,'___ibm_get_windowy2')])
        self.assertEqual(q['publics'],[(0,'__IBM_RESET_VRAM_ACCESS'),
            (11,'__IBM_START_VRAM_ACCESS'),(126,'__IBM_END_VRAM_ACCESS'),
            (278,'__IBM_OUTPUT_CHAR')])
        self.assertEqual(len(p['imports']),4)
        self.assertEqual(len(q['imports']),13)
        self.assertEqual((len(p['relocation_sites_targets']),
                          len(q['relocation_sites_targets'])),(40,65))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'video-chain-build.json')).is_file(),
                         'literal original PC-98 video OBJ vectors absent')
    def test_computer_vendor_data_and_105_original_site_sorted_frames(self):
        receipt=json.loads((ROOT/(PREFIX+'video-chain-build.json')).read_text())
        raw=(WORK/'vendor/cibminit.obj').read_bytes()
        p=payload(raw)
        self.assertEqual(bytes(p[2,i] for i in range(7)),b'COMPAQ\0')
        old=[literal_fields((WORK/'vendor'/(name+'.obj')).read_bytes())
             for name in ('cibminit','cibmputn')]
        self.assertEqual([len(x) for x in old],[40,65])
        key=lambda f:(f['segment'],f['site'])
        for rd in receipt['rounds']:
            for j,name in enumerate(('cibminit','cibmputn')):
                original=(WORK/'vendor'/(name+'.obj')).read_bytes()
                made=(ROOT/rd['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made))
                f=literal_fields(made)
                self.assertEqual(sorted(old[j],key=key),sorted(f,key=key))
                self.assertNotEqual(old[j],f)
                self.assertFalse(rd['literal_omf_fixupp_equal_by_member'][name])
        self.assertFalse(receipt['literal_OMF_FIXUPP_equal'])
