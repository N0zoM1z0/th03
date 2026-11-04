"""Complete original Japanese PC-98 extended serial driver source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after128_work import PREFIX,WORK
from review_th03_mainl_after128_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalExtendedPC98Serial(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'pc98comx-build.json')).is_file(),
                         '129-source selected original Japanese native rounds absent')
    def test_all_ten_original_PC98_extended_APIs_and_link(self):
        r=review('pc98comx')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,129,764))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1383,60022))
        p=r['profiles']['pc98comx']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (1383,35,70))
        self.assertEqual(p['publics'],[(672,'_pc98cominitx'),
            (951,'_pc98comtermx'),(1021,'_pc98comsendx'),
            (1043,'_pc98comrecvx'),(1068,'_pc98comgetstatx'),
            (1104,'_pc98comsetstatx'),(1126,'_pc98comchkbufx'),
            (1165,'_pc98comsendbreakx'),(1202,'_pc98comresetx'),
            (1268,'_pc98comcheckbaudx')])
        self.assertEqual(p['imports'],
                         ['_getvect','_setvect','___nec_delay','N_SCOPY@'])
        self.assertEqual(len(p['relocation_sites_targets']),58)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']), (2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'pc98comx-build.json')).is_file(),
                         'extended serial native OBJ pair unavailable')
    def test_code_bios_signature_data_and_site_sorted_literal_omf_fields(self):
        r=json.loads((ROOT/(PREFIX+'pc98comx-build.json')).read_text())
        original=(WORK/'vendor/pc98comx.obj').read_bytes()
        raw=payload(original)
        self.assertEqual(len([f for f in raw if f[0]==1]),1383)
        self.assertEqual(len([f for f in raw if f[0]==2]),35)
        self.assertEqual(len([f for f in raw if f[0]==3]),0)
        d=bytes(raw[2,i] for i in range(35))
        self.assertEqual(d[:5],bytes(5))
        self.assertEqual(d[25:],bytes((0,4,8,12,0,48,16,64,128,192)))
        o=literal_fields(original)
        self.assertEqual(len(o),58)
        original_near=next(f for f in o if f['site']==1245)
        self.assertEqual((original_near['target_method'],
                          original_near['target'],original_near['frame_method']),
                         (2,4,0))
        key=lambda f:(f['segment'],f['site'])
        for rd in r['rounds']:
            new=(ROOT/rd['outputs']['pc98comx']['path']).read_bytes()
            self.assertEqual(payload(original),payload(new))
            f=literal_fields(new)
            self.assertEqual(sorted(o,key=key),sorted(f,key=key))
            self.assertNotEqual(o,f)
            self.assertFalse(rd['literal_omf_fixupp_equal_by_member']['pc98comx'])
