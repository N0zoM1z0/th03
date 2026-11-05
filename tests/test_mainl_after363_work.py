"""Full original Borland DOS PSP/startup setargv, sparse CODE/DATA and INIT."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after363_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after363_work import review

class OriginalDOSSetargvBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'startup-dos-argv-boss-build.json')).is_file(),
                         'original Japanese 428-source native receipts absent')
    def test_full_dos_dbcs_argv_parser_and_original_link(self):
        r=review('startup-dos-argv-boss')
        p=r['profiles']['setargv']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,428,465))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (343,136524))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes'],
                          p['INITDATA_bytes']),(343,16,0,6))
        self.assertEqual(p['CODE_implicit_sites'],[0,1])
        self.assertEqual(p['DATA_implicit_sites'],list(range(6,16)))
        self.assertEqual(p['INITDATA_implicit_sites'],[4,5])
        self.assertEqual(p['absolute_publics'],[(0,'__setargv__')])
        self.assertEqual(p['publics'],[])
        self.assertEqual(p['data_publics'],[(0,'__argc'),(2,'__argv')])
        self.assertEqual(p['imports'],NATIVE['setargv']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),30)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'startup-dos-argv-boss-build.json')).is_file(),
                         'original source OBJ and linked EXE pairs unavailable')
    def test_original_sparse_init_and_c0argv_segment_relocation(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['setargv']['index']])
        old=payload(original)
        self.assertEqual(len(old),341+6+4)
        self.assertEqual([i for i in range(343) if (1,i) not in old],[0,1])
        self.assertEqual([i for i in range(16) if (2,i) not in old],list(range(6,16)))
        self.assertEqual([i for i in range(6) if (3,i) not in old],[4,5])
        self.assertEqual(bytes(old[3,i] for i in range(4)),bytes.fromhex('00 10 02 00'))
        self.assertEqual(code_publics(original,0),[(0,'__setargv__')])
        fields=literal_fields(original)
        self.assertEqual(len(fields),30)
        site={f['site']:f for f in fields if f['segment']==1}
        self.assertEqual((site[331]['target_method'],site[331]['target'],
                          site[331]['addend'],site[331]['frame_method']),(2,2,2,5))
        self.assertEqual((site[337]['target_method'],site[337]['target'],
                          site[337]['addend'],site[337]['frame_method']),(2,2,0,5))
        receipt=json.loads((ROOT/(PREFIX+'startup-dos-argv-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['setargv']['path']).read_bytes()
                self.assertEqual(payload(made),old)
                self.assertEqual(sorted(literal_fields(made),key=lambda f:(f['segment'],f['site'])),
                                 sorted(fields,key=lambda f:(f['segment'],f['site'])))
                self.assertNotEqual(literal_fields(made),fields)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['setargv'])
                self.assertFalse(row['original_program_equal_by_member']['setargv'])
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['setargv']['index']].program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
