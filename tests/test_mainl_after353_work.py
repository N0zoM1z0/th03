"""Original 3-API 971-byte Borland rfind/reverse substring search boss."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after353_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after353_work import review

PUBLICS=[(0,'@string@rfind$xqmx6stringui'),
         (71,'@string@rfind_index$xqnxcuimui'),
         (282,'@string@rfind_case_index$xqnxcuimui')]


class OriginalReverseFindBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-reverse-find-boss-build.json')).is_file(),
                         'local original 404-source rfind native receipts absent')
    def test_three_original_full_cxx_apis_and_exact_native_link(self):
        r=review('string-reverse-find-boss')
        p=r['profiles']['rfind']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,404,489))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (971,130205))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(63,908,971,0,0))
        self.assertEqual(p['publics'],PUBLICS)
        self.assertEqual(p['imports'],NATIVE['rfind']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),37)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-reverse-find-boss-build.json')).is_file(),
                         'native original/source OMF and MZ pairs absent')
    def test_literal_order_37_fixups_real_state_offsets_and_japanese_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['rfind']['index']]
        self.assertEqual(m.name,'rfind')
        original=original_library_member(m)
        fields=literal_fields(original)
        self.assertEqual(len(fields),37)
        self.assertEqual(code_publics(original,4),PUBLICS)
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        self.assertEqual([f['site'] for f in fields if f['segment']==1],
                         [61,35,25,15,9])
        sites=[f['site'] for f in fields if f['segment']==4]
        self.assertEqual(len(sites),32)
        self.assertEqual(sites,sorted(sites,reverse=True))
        for site,off in ((12,9),(83,49)):
            f=next(f for f in fields if f['segment']==4 and f['site']==site)
            self.assertEqual((f['target_method'],f['target'],f['addend']),(0,1,off))
        original_code=payload(original)
        self.assertEqual(len(original_code),971)
        rec=json.loads((ROOT/(PREFIX+'string-reverse-find-boss-build.json')).read_text())
        for row in rec['rounds']:
            with self.subTest(round=row['round']):
                obj=(ROOT/row['outputs']['rfind']['path']).read_bytes()
                self.assertEqual(payload(obj),original_code)
                self.assertEqual(literal_fields(obj),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['rfind'])
                self.assertFalse(row['original_program_equal_by_member']['rfind'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
