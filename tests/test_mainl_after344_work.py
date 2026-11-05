"""Original Japanese setenvp absolute PUBDEF and sparse INITDATA source."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after344_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after344_work import review


class OriginalStartupEnvironment(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'startup-environment-init-build.json')).is_file(),
                         'original setenvp 378-source native receipts absent')
    def test_complete_88_code_four_data_and_sparse_init_startup(self):
        r=review('startup-environment-init')
        p=r['profiles']['setenvp']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,378,515))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (88,124689))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (88,4,0))
        self.assertEqual((p['INITDATA_bytes'],p['INITDATA_implicit_sites']),
                         (6,[4,5]))
        self.assertEqual(p['absolute_publics'],[(0,'__setenvp__')])
        self.assertEqual(p['publics'],[])
        self.assertEqual(p['data_publics'],[(0,'__environ')])
        self.assertEqual(p['imports'],NATIVE['setenvp']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),11)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'startup-environment-init-build.json')).is_file(),
                         'raw two-round setenvp OMF and full native image absent')
    def test_absolute_pubdef_init_reloc_and_exact_map_in_both_rounds(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['setenvp']['index']]
        original=original_library_member(m)
        p=payload(original)
        self.assertEqual(code_publics(original,0),[(0,'__setenvp__')])
        self.assertEqual(code_publics(original,2),[(0,'__environ')])
        self.assertEqual([i for i in range(6) if (3,i) not in p],[4,5])
        self.assertEqual(bytes(p[3,i] for i in range(4)),b'\x00\x10\x00\x00')
        old_fields=literal_fields(original)
        self.assertEqual(len(old_fields),11)
        init=[f for f in old_fields if f['segment']==3]
        self.assertEqual(len(init),1)
        self.assertEqual((init[0]['site'],init[0]['target_method'],
                          init[0]['target'],init[0]['addend']), (2,0,1,0))
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['08ff02'])
        receipt=json.loads((ROOT/(PREFIX+'startup-environment-init-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['setenvp']['path']).read_bytes()
                self.assertEqual(payload(made),p)
                self.assertEqual(literal_fields(made),old_fields)
                self.assertEqual(code_publics(made,0),[(0,'__setenvp__')])
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['setenvp'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                self.assertEqual((ROOT/row['outputs']['exe']['path']).read_bytes(),
                                 (WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual((ROOT/row['outputs']['map']['path']).read_bytes(),
                                 (WORK/'obj/th03/mainl.map').read_bytes())


if __name__=='__main__':
    unittest.main()
