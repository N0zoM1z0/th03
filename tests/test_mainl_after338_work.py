"""Original 16-bit DOS overlay exec: exact CODE gap, bytes, OMF and MZ link."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after338_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after338_work import review


class OriginalBorlandOverlayExec(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'dos-exec-overlay-boss-build.json')).is_file(),
                         'local original 364-source overlay exec receipts absent')
    def test_entire_overlay_exec_source_and_full_original_link(self):
        r=review('dos-exec-overlay-boss')
        p=r['profiles']['exec']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,364,529))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (933,119828))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (933,0,0))
        self.assertEqual(p['CODE_implicit_sites'],list(range(255))+[356,357])
        self.assertEqual(p['publics'],[(359,'__exec')])
        self.assertEqual(p['imports'],['__cexit','__IOERROR','__envseg',
                                      'DGROUP@','__psp','__version'])
        self.assertEqual(len(p['relocation_sites_targets']),21)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertTrue(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'dos-exec-overlay-boss-build.json')).is_file(),
                         'native original and compiled full OMF pair absent')
    def test_full_original_member_program_and_alternate_vendor_frame_disagreement(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['exec']['index']]
        self.assertEqual(m.name,'exec')
        orig=original_library_member(m)
        v=(WORK/'vendor/exec.obj').read_bytes()
        a={f['site']:f for f in literal_fields(orig)}
        b={f['site']:f for f in literal_fields(v)}
        self.assertEqual(set(a),set(b))
        self.assertEqual({site for site in a if a[site]!=b[site]},
                         {371,397,482,560})
        self.assertEqual([(a[site]['frame_method'],b[site]['frame_method'])
                          for site in (371,397,482,560)],[(1,5)]*4)
        data=payload(orig)
        self.assertEqual(len(data),676)
        self.assertEqual([i for i in range(933) if (1,i) not in data],
                         list(range(255))+[356,357])
        self.assertEqual(len(literal_fields(orig)),21)
        receipt=json.loads((ROOT/(PREFIX+'dos-exec-overlay-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                obj=(ROOT/row['outputs']['exec']['path']).read_bytes()
                self.assertEqual(payload(obj),data)
                self.assertEqual(literal_fields(obj),literal_fields(orig))
                self.assertEqual(object_program_records(obj),m.program_records)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['exec'])
                self.assertTrue(row['original_program_equal_by_member']['exec'])
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
