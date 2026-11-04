"""Original Japanese C++ strstreambuf seekoff and overflow source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after134_work import PREFIX,WORK
from review_th03_mainl_after134_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStringStreamBufferBosses(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strstream-bosses-build.json')).is_file(),
                         '136-source native streambuf pair unavailable')
    def test_both_complete_streambuf_algorithms_and_Japanese_product(self):
        r=review('strstream-bosses')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,136,757))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1112,64568))
        a,b=r['profiles']['srbskoff'],r['profiles']['srboflow']
        self.assertEqual((a['CODE_bytes'],b['CODE_bytes']),(600,512))
        self.assertEqual((a['DATA_bytes'],a['BSS_bytes'],
                          b['DATA_bytes'],b['BSS_bytes']),(0,0,0,0))
        self.assertEqual(a['publics'],
                         [(0,'@strstreambuf@seekoff$ql12ios@seek_diri')])
        self.assertEqual(b['publics'],[(0,'@strstreambuf@overflow$qi')])
        self.assertEqual(len(a['relocation_sites_targets']),2)
        self.assertEqual(len(b['relocation_sites_targets']),7)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'strstream-bosses-build.json')).is_file(),
                         'original native selected OBJ pairs unavailable')
    def test_all_nine_original_relocations_with_native_frames(self):
        report=json.loads((ROOT/(PREFIX+'strstream-bosses-build.json')).read_text())
        by=lambda f:(f['segment'],f['site'])
        for name,count in [('srbskoff',2),('srboflow',7)]:
            orig=(WORK/'vendor'/(name+'.obj')).read_bytes()
            f=literal_fields(orig)
            self.assertEqual(len(f),count)
            for rd in report['rounds']:
                out=(ROOT/rd['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(orig),payload(out))
                self.assertEqual(sorted(f,key=by),
                                 sorted(literal_fields(out),key=by))
                self.assertNotEqual(f,literal_fields(out))
                self.assertFalse(rd['literal_omf_fixupp_equal_by_member'][name])
