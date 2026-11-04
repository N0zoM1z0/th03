"""Original selected Japanese CRT DOS vectors, times and vscanf family."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after106_work import PREFIX, WORK
from review_th03_mainl_after106_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalDOSAndScannerLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'scan-vectors-time-build.json')).is_file(),
                         '112-source original Japanese selected CRT output absent')
    def test_six_original_native_members_complete_product(self):
        r=review('scan-vectors-time')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,112,781))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (253,51546))
        expected={'vscanf':40,'vfscanf':41,'dosvect':40,'getvect':40,
                  'getdate':46,'setdate':46}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        self.assertTrue(all(r['profiles'][n]['DATA_bytes']==0 and
                            r['profiles'][n]['BSS_bytes']==0 for n in expected))
        self.assertEqual(r['profiles']['dosvect']['publics'],
                         [(0,'__dos_getvect'),(19,'__dos_setvect')])
        self.assertEqual(r['profiles']['getvect']['publics'],
                         [(0,'_getvect'),(19,'_setvect')])
        self.assertEqual(r['profiles']['getdate']['publics'],
                         [(0,'_getdate'),(23,'_gettime')])
        self.assertEqual(r['profiles']['setdate']['publics'],
                         [(0,'_setdate'),(23,'_settime')])
        self.assertEqual(r['profiles']['vscanf']['imports'],
                         ['__streams','__Nfgetc','__Nungetc','__scanner'])
        self.assertEqual(r['profiles']['vfscanf']['imports'],
                         ['__Nfgetc','__Nungetc','__scanner'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'scan-vectors-time-build.json')).is_file(),
                         'raw Borland DOS leaf vector pairs absent')
    def test_original_fields_and_only_two_near_scanner_frame_gaps(self):
        receipt=json.loads((ROOT/(PREFIX+'scan-vectors-time-build.json')).read_text())
        expected={'vscanf':{31},'vfscanf':{32},
                  'dosvect':set(),'getvect':set(),
                  'getdate':set(),'setdate':set()}
        key=lambda f:(f['segment'],f['site'])
        for name,sites in expected.items():
            a=(WORK/'vendor'/(name+'.obj')).read_bytes()
            for roundinfo in receipt['rounds']:
                b=(ROOT/roundinfo['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(a),payload(b),name)
                fa,fb=literal_fields(a),literal_fields(b)
                self.assertEqual(len(fa),len(fb))
                sorted_a,sorted_b=sorted(fa,key=key),sorted(fb,key=key)
                without_frame=lambda f:tuple((k,v) for k,v in f.items()
                    if k not in ('frame','frame_method'))
                self.assertEqual([without_frame(f) for f in sorted_a],
                                 [without_frame(f) for f in sorted_b],name)
                drift={(x['site'],x['frame_method'],y['frame_method'])
                        for x,y in zip(sorted_a,sorted_b) if x!=y}
                self.assertEqual(drift,{(site,5,0) for site in sites},name)
                if not sites:
                    self.assertEqual(fa,fb,name)
