"""Original Japanese PC-98 ten-function serial driver native source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after117_work import PREFIX,WORK
from review_th03_mainl_after117_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalPC98SerialDriver(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'pc98com-build.json')).is_file(),
                         '118-source selected original Japanese CRT rounds absent')
    def test_ten_full_original_serial_APIs_and_native_product(self):
        r=review('pc98com')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,118,775))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1467,57276))
        p=r['profiles']['pc98com']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (1467,55,54))
        self.assertEqual(p['publics'],[
            (468,'_pc98cominit'),(923,'_pc98comterm'),
            (998,'_pc98comsend'),(1067,'_pc98comrecv'),
            (1208,'_pc98comgetstat'),(1244,'_pc98comsetstat'),
            (1267,'_pc98comchkbuf'),(1322,'_pc98comsendbreak'),
            (1367,'_pc98comreset'),(1422,'_pc98comcheckbaud')])
        self.assertEqual(p['imports'],['_getvect','_setvect','___nec_delay'])
        self.assertEqual(len(p['relocation_sites_targets']),130)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'pc98com-build.json')).is_file(),
                         'original PC-98 native OBJ pair absent')
    def test_baud_data_and_bss_and_all_130_original_fixup_frames(self):
        rep=json.loads((ROOT/(PREFIX+'pc98com-build.json')).read_text())
        a=(WORK/'vendor/pc98com.obj').read_bytes()
        pa=payload(a)
        self.assertEqual(len([z for z in pa if z[0]==2]),55)
        self.assertEqual(len([z for z in pa if z[0]==3]),0)
        fa=literal_fields(a)
        self.assertEqual(len(fa),130)
        self.assertEqual(next(f for f in fa if f['site']==10)['target_method'],1)
        self.assertEqual(next(f for f in fa if f['site']==10)['target'],1)
        key=lambda f:(f['segment'],f['site'])
        for roundinfo in rep['rounds']:
            b=(ROOT/roundinfo['outputs']['pc98com']['path']).read_bytes()
            self.assertEqual(pa,payload(b))
            fb=literal_fields(b)
            self.assertEqual(sorted(fa,key=key),sorted(fb,key=key))
            self.assertNotEqual(fa,fb)
            self.assertFalse(roundinfo['literal_omf_fixupp_equal_by_member']['pc98com'])
