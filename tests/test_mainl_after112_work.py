"""Original Borland vector apply / new / delete complete 8086 sources."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after112_work import PREFIX,WORK
from review_th03_mainl_after112_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalVectorLifecycle(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'vector-family-build.json')).is_file(),
                         'source-bound original 116-source vector native pair absent')
    def test_all_four_full_vector_algorithms_and_product(self):
        r=review('vector-family')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,116,777))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2824,54370))
        sizes={'vapp':674,'vdelf':657,'vnewf':707,'vnewvf':786}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in sizes},sizes)
        self.assertTrue(all(r['profiles'][n]['DATA_bytes']==0 and
                            r['profiles'][n]['BSS_bytes']==0 for n in sizes))
        self.assertEqual(r['profiles']['vapp']['publics'],[(0,'__vector_apply_')])
        self.assertEqual(r['profiles']['vdelf']['publics'],
                         [(0,'@_vector_delete_$qnvuiuluie')])
        self.assertEqual(r['profiles']['vnewf']['publics'],
                         [(0,'@_vector_new_$qnvuiuluie')])
        self.assertEqual(r['profiles']['vnewvf']['publics'],
                         [(0,'@_vector_vnew_$qnvuiuluie')])
        self.assertEqual([len(r['profiles'][n]['relocation_sites_targets'])
                          for n in sizes],[34,22,26,26])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'vector-family-build.json')).is_file(),
                         'source-bound original vector OMF fields absent')
    def test_original_80_symbolic_switch_entries_and_bounded_near_frame_drifts(self):
        r=json.loads((ROOT/(PREFIX+'vector-family-build.json')).read_text())
        cases={'vapp':(610,32),'vdelf':(625,16),'vnewf':(675,16),
               'vnewvf':(754,16)}
        known={'vapp':set(),'vdelf':{167},
               'vnewf':{152,203,272},'vnewvf':{152,203,272}}
        by=lambda f:(f['segment'],f['site'])
        for n,(site,count) in cases.items():
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            old=literal_fields(original)
            self.assertEqual(len([f for f in old if site<=f['site']<site+count*2]),
                             count)
            self.assertEqual(sorted(f['site'] for f in old if
                             site<=f['site']<site+count*2),
                             list(range(site,site+count*2,2)))
            for rd in r['rounds']:
                src=(ROOT/rd['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(original),payload(src))
                fa,fb=sorted(old,key=by),sorted(literal_fields(src),key=by)
                noframe=lambda f:tuple((k,v) for k,v in f.items()
                    if k not in ('frame','frame_method'))
                self.assertEqual([noframe(f) for f in fa],
                                 [noframe(f) for f in fb],n)
                self.assertEqual({(f['site'],f['frame_method'],g['frame_method'])
                    for f,g in zip(fa,fb) if f!=g},
                    {(site,5,0) for site in known[n]},n)
