"""Scoped verification of Japanese original MAINL native post-89 CRT work."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after89_work import PREFIX, WORK
from review_th03_mainl_after89_work import review
from build_th03_mainl_display_work import literal_fields,payload

class OriginalAfter89(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'utime-build.json')).is_file(),
                         'source-bound original native utime pair not retained')
    def test_complete_time_conversion_and_original_link(self):
        r=review('utime')
        self.assertTrue(r['complete'])
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(90,803,38225))
        p=r['profiles']['utime']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (654,12,0))
        self.assertEqual(p['publics'],[(0,'_utime')])
        self.assertEqual(p['imports'],['__ISDST','__dos_close','__dos_getdate',
            '__dos_gettime','__dos_open','__dos_setftime','__daylight',
            '__timezone','_tzset','N_LMOD@','N_LDIV@'])
        self.assertEqual(len(p['relocation_sites_targets']),24)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'utime-build.json')).is_file(),
                         'utime native object vector not retained')
    def test_24_original_relocations_and_known_target_frame_differences(self):
        import json
        rep=json.loads((ROOT/(PREFIX+'utime-build.json')).read_text())
        original=(WORK/'vendor/utime.obj').read_bytes()
        source=(ROOT/rep['rounds'][0]['outputs']['utime']['path']).read_bytes()
        self.assertEqual(payload(original),payload(source))
        lhs=literal_fields(original);rhs=literal_fields(source)
        self.assertEqual((len(lhs),len(rhs)),(24,24))
        key=lambda z:(z['segment'],z['site'])
        a,b=sorted(lhs,key=key),sorted(rhs,key=key)
        no_frame=lambda f:tuple(v for k,v in f.items() if k not in ('frame','frame_method'))
        self.assertEqual([no_frame(f) for f in a],[no_frame(f) for f in b])
        diffs=[(x['site'],x['frame_method'],y['frame_method'])
               for x,y in zip(a,b) if x['frame_method']!=y['frame_method']]
        self.assertEqual(len(diffs),13)
        self.assertTrue(all(z[1:]==(5,0) for z in diffs))
        self.assertNotEqual(lhs,rhs)

    @unittest.skipUnless((ROOT/(PREFIX+'utime-console-build.json')).is_file(),
                         '97-source console CRT original rounds absent')
    def test_seven_original_keyboard_printf_and_getcwd_members(self):
        import json
        r=review('utime-console')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(97,796,38563))
        assert r['complete_original_CODE_DATA_equal']
        assert r['complete_native_link_EXE_MAP_equal']
        assert r['original_MZ_relocations']==677
        expected={'getch':29,'getche':52,'getcwd':142,'kbhit':22,
                  'printf':31,'putch':25,'ungetch':37}
        self.assertEqual({k:r['profiles'][k]['CODE_bytes'] for k in expected},expected)
        self.assertEqual(r['profiles']['kbhit']['DATA_bytes'],2)
        self.assertEqual(r['profiles']['kbhit']['data_publics'],
                         [(0,'__cFlag'),(1,'__cChar')])
        self.assertEqual(r['profiles']['getche']['publics'],
                         [(0,'__Ngetche'),(3,'_getche')])
        self.assertEqual(r['profiles']['ungetch']['publics'],
                         [(0,'__Nungetch'),(3,'_ungetch')])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])
        receipt=json.loads((ROOT/(PREFIX+'utime-console-build.json')).read_text())
        for row in receipt['rounds']:
            field_status=row['literal_omf_fixupp_equal_by_member']
            for name in ('kbhit','getch','getche','ungetch'):
                self.assertTrue(field_status[name],name)
            for name in ('getcwd','printf','putch'):
                self.assertFalse(field_status[name],name)
