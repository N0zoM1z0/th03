"""Nine complete original near/far CRT string and memory functions."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after119_work import PREFIX,WORK
from review_th03_mainl_after119_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalFarPointerMemoryString(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'far-memory-leaves-build.json')).is_file(),
                         '128-source original native far memory rounds unavailable')
    def test_all_nine_complete_member_ABIs_and_product(self):
        r=review('far-memory-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,128,765))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (479,58639))
        expected={'memccpy':57,'fmemccpy':57,'fstrcpy':41,'fstrncpy':49,
                  'fstrcmp':48,'fstrncmp':56,'fstrchr':63,
                  'fmemset':72,'fmemcpy':36}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        self.assertEqual(r['profiles']['fmemset']['publics'],
                         [(0,'__fsetmem'),(38,'__fmemset')])
        self.assertEqual(r['profiles']['memccpy']['publics'],[(0,'_memccpy')])
        self.assertEqual(r['profiles']['fmemccpy']['publics'],[(0,'__fmemccpy')])
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']), (0,0),n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'far-memory-leaves-build.json')).is_file(),
                         'raw original far memory vector pairs unavailable')
    def test_all_original_CODE_bytes_and_full_empty_fixup_inventory(self):
        r=json.loads((ROOT/(PREFIX+'far-memory-leaves-build.json')).read_text())
        for n in r['names']:
            old=(WORK/'vendor'/(n+'.obj')).read_bytes()
            for row in r['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(old),payload(made),n)
                self.assertEqual(literal_fields(old),[],n)
                self.assertEqual(literal_fields(made),[],n)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n],n)
