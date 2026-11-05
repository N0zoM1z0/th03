"""Original xalloc C++ exception boss and literal ordered Japanese MZ proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after341_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after341_work import review

PUBLICS=[(0,'@xalloc@$bctr$qmx6stringui'),(127,'@xalloc@raise$qv')]
ORIGINAL_MZ_SITES=[489,362,346,157,136,115,101,93]


class OriginalXallocExceptionBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'xalloc-exception-boss-build.json')).is_file(),
                         'local original 375-source xalloc native receipts absent')
    def test_full_original_borland_xalloc_and_native_image(self):
        r=review('xalloc-exception-boss')
        p=r['profiles']['xalloc']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,375,518))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (513,121362))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (513,0,0))
        self.assertEqual(p['publics'],PUBLICS)
        self.assertEqual(p['imports'],[
            '@$bnew$qui','@$bdele$qnv','@__RefDestructorCount$qv',
            '@_ThrowException$qnvt1t1t1uiuiuinuc','___InitExceptBlocks',
            '@xmsg@$bctr$qmx6string','@xmsg@$bctr$qmx4xmsg',
            '@xmsg@$bdtr$qv',
        ])
        self.assertEqual(len(p['relocation_sites_targets']),24)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'xalloc-exception-boss-build.json')).is_file(),
                         'raw source/CL.LIB original C++ member absent')
    def test_original_omf_frame_fields_and_eight_mz_entries_in_original_order(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['xalloc']['index']]
        self.assertEqual(m.name,'xalloc')
        orig=original_library_member(m)
        oldfields=literal_fields(orig)
        self.assertEqual(len(oldfields),24)
        self.assertEqual([r.data.hex() for r in parse_omf(orig)
                          if r.name=='GRPDEF'],['08ff02ff03'])
        old=payload(orig)
        self.assertEqual([i for i in range(513) if (1,i) not in old],[])
        fields={f['site']:f for f in oldfields}
        for site,addend in ((91,314),(99,314),(113,91),(125,99),
                            (161,247),(230,314),(344,380),(360,457)):
            self.assertEqual((fields[site]['target_method'],fields[site]['target'],
                              fields[site]['addend']), (0,1,addend))
        rec=json.loads((ROOT/(PREFIX+'xalloc-exception-boss-build.json')).read_text())
        orig_exe=(WORK/'bin/th03/mainl.target.exe').read_bytes()
        orig_mz=parse_mz(orig_exe)
        self.assertEqual([orig_mz.relocations[i].offset-21073
                          for i in range(500,508)],ORIGINAL_MZ_SITES)
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['xalloc']['path']).read_bytes()
                self.assertEqual(payload(made),old)
                self.assertEqual(sorted(literal_fields(made),key=lambda f:f['site']),
                                 sorted(oldfields,key=lambda f:f['site']))
                self.assertNotEqual(literal_fields(made),oldfields)
                self.assertNotEqual(object_program_records(made),m.program_records)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member']['xalloc'])
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,orig_exe)
                mz=parse_mz(exe)
                self.assertEqual(len(mz.relocations),677)
                self.assertEqual([mz.relocations[i].offset-21073
                                  for i in range(500,508)],ORIGINAL_MZ_SITES)


if __name__=='__main__':
    unittest.main()
