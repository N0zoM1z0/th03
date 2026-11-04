"""Thirteen selected native 16-bit far string/memory source algorithms."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after155_work import PREFIX,WORK
from review_th03_mainl_after155_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFarStringAlgorithms(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'far-string-algorithms-build.json')).is_file(),
                         '168-source native far-string pair unavailable')
    def test_all_thirteen_complete_original_members_and_product(self):
        r=review('far-string-algorithms')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,168,725))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (777,72053))
        expected={'fstrstr':108,'fstrspn':82,'fstrpbrk':80,'fstrcspn':73,
                  'fstrnicm':68,'fstricmp':65,'fstrcat':63,'fstrrev':52,
                  'fmemchr':37,'fmemcmp':40,'fstrlen':33,'fstrlwr':38,'fstrupr':38}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0),n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
            self.assertEqual(len(p['publics']),1,n)
            self.assertEqual(p['publics'][0][0],0,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'far-string-algorithms-build.json')).is_file(),
                         'native source and original CRT member vectors unavailable')
    def test_complete_code_and_empty_original_omf_field_inventory(self):
        r=json.loads((ROOT/(PREFIX+'far-string-algorithms-build.json')).read_text())
        for name in r['names']:
            a=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(literal_fields(a),[],name)
            for row in r['rounds']:
                b=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(a),payload(b),name)
                self.assertEqual(literal_fields(b),[],name)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name],name)

    def test_original_far_search_XCHG_register_forms(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        cases={'fstrstr':{39:'87ca',62:'87fb',64:'87ca',85:'87ca'},
               'fstrcat':{38:'87f7'},'fstrrev':{30:'87f7'}}
        for name,expected in cases.items():
            p=payload((WORK/'vendor'/(name+'.obj')).read_bytes())
            code=bytes(p[1,i] for i in range(max(i for s,i in p if s==1)+1))
            ins={x.address:x.bytes.hex() for x in Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0)}
            self.assertEqual({site:ins[site] for site in expected},expected)
