"""17 complete original Borland strings APIs, literal OMF relocation order."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after343_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after343_work import review

DATA_VALUES=b'\x01\x00\x00\x00\x01\x00\x3f\x00\x40\x00\x3f\x00'+(
    b'String reference out of range\0'*3)


class OriginalBorlandStringsBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-class-boss-build.json')).is_file(),
                         'retained native 377-source Japanese strings receipts absent')
    def test_complete_two_code_segment_17_method_boss_and_data(self):
        r=review('string-class-boss')
        p=r['profiles']['strings']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,377,516))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2958,124601))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']), (587,2371,2958,102,0))
        self.assertEqual(p['publics'],NATIVE['strings']['publics'])
        self.assertEqual(p['data_publics'],NATIVE['strings']['data_publics'])
        self.assertEqual(p['imports'],NATIVE['strings']['imports'])
        self.assertEqual(len(p['publics']),17)
        self.assertEqual(len(p['data_publics']),6)
        self.assertEqual(len(p['relocation_sites_targets']),166)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-class-boss-build.json')).is_file(),
                         'both native original/full source OBJ programs absent')
    def test_exact_original_166_fixupp_order_real_options_rtti_and_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['strings']['index']]
        self.assertEqual(m.name,'strings')
        original=original_library_member(m)
        op=payload(original)
        self.assertEqual(bytes(op[2,i] for i in range(102)),DATA_VALUES)
        self.assertEqual(code_publics(original,4),NATIVE['strings']['publics'])
        fields=literal_fields(original)
        self.assertEqual(len(fields),166)
        self.assertEqual([v.data.hex() for v in parse_omf(original)
                          if v.name=='GRPDEF'],['0aff02ff03'])
        # Original CODE metadata is in three physical 1K/1K/323B LEDATA
        # runs, each with descending fixup order; none is sorted away.
        for low,high in ((0,1024),(1024,2048),(2048,2371)):
            sites=[f['site'] for f in fields
                   if f['segment']==4 and low<=f['site']<high]
            self.assertEqual(sites,sorted(sites,reverse=True))
            self.assertTrue(len(sites)>0)
        record=json.loads((ROOT/(PREFIX+'string-class-boss-build.json')).read_text())
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['strings']['path']).read_bytes()
                self.assertEqual(payload(made),op)
                self.assertEqual(literal_fields(made),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['strings'])
                self.assertFalse(row['original_program_equal_by_member']['strings'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
