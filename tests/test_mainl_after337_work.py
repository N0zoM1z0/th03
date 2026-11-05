"""Pinned Japanese Borland LoadProg, full source/errno/OMF/DATA native link."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after337_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import literal_fields, payload
from build_th03_mainl_resources_work import sha
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after337_work import review


class OriginalLoadProg(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-loadprog-boss-build.json')).is_file(),
                         'local original-source 363-member native receipts absent')
    def test_complete_program_loader_and_original_exe(self):
        r=review('dos-loadprog-boss')
        p=r['profiles']['loadprog']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,363,530))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (871,118895))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (871,40,0))
        self.assertEqual(p['publics'],[(269,'__LoadProg')])
        self.assertEqual(p['imports'],NATIVE['loadprog']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),32)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'dos-loadprog-boss-build.json')).is_file(),
                         'raw source-bound loadprog native vectors absent')
    def test_exact_original_fields_and_real_library_over_alternate_vendor_obj(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['loadprog']['index']]
        self.assertEqual(m.name,'loadprog')
        original=original_library_member(m)
        vendor=(WORK/'vendor/loadprog.obj').read_bytes()
        self.assertEqual(payload(vendor),payload(original))
        o={f['site']:f for f in literal_fields(original)}
        v={f['site']:f for f in literal_fields(vendor)}
        self.assertEqual(set(o),set(v))
        self.assertEqual({site for site in o if o[site]!=v[site]}, {633,754})
        self.assertEqual([(o[s]['frame_method'],v[s]['frame_method'])
                          for s in (633,754)], [(0,5),(0,5)])
        self.assertEqual(len(o),32)
        rec=json.loads((ROOT/(PREFIX+'dos-loadprog-boss-build.json')).read_text())
        self.assertEqual(rec['include_source_path'],'src/mainl/crt/crt_errno.inc')
        self.assertEqual(rec['include_sha256'],sha((ROOT/rec['include_source_path']).read_bytes()))
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['loadprog']['path']).read_bytes()
                self.assertEqual(payload(made),payload(original))
                self.assertEqual(literal_fields(made),literal_fields(original))
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['loadprog'])
                self.assertFalse(row['original_program_equal_by_member']['loadprog'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
