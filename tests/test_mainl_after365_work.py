"""Full original BCC string operator+ and 8 original RTTI descriptors."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after365_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_boss_marisa_cpp import code_publics
from review_th03_mainl_after365_work import review


class OriginalStringPlusBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'string-plus-exception-boss-build.json')).is_file(),
                         'original Japanese 432-source OBJ/EXE receipts absent')
    def test_complete_operator_plus_exception_helpers_and_native_link(self):
        r=review('string-plus-exception-boss')
        p=r['profiles']['oprplus']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,432,461))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (999,137835))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(253,746,999,0,0))
        self.assertEqual(p['publics'],[(0,'@$badd$qnxcmx6string')])
        self.assertEqual(p['imports'],NATIVE['oprplus']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),38)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'string-plus-exception-boss-build.json')).is_file(),
                         'original and both TASM OMF programs absent')
    def test_all_38_original_fixupp_sites_typed_rtti_and_japanese_mz(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['oprplus']['index']]
        self.assertEqual(m.name,'oprplus')
        original=original_library_member(m)
        po=payload(original)
        self.assertEqual(len(po),999)
        self.assertEqual(code_publics(original,4),[(0,'@$badd$qnxcmx6string')])
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        fields=literal_fields(original)
        self.assertEqual(len(fields),38)
        for segment,count in ((1,16),(4,22)):
            sites=[f['site'] for f in fields if f['segment']==segment]
            self.assertEqual(len(sites),count)
            self.assertEqual(sites,sorted(sites,reverse=True))
        for offset,fragment in ((340,b'TStringRef *\0'),(363,b'string *\0'),
                                (410,b'string\0\0'),
                                (468,b'string::lengtherror\0'),
                                (546,b'xalloc\0\0'),(612,b'xmsg\0\0'),
                                (668,b'TStringRef\0\0'),
                                (726,b'TReference\0\0')):
            self.assertEqual(bytes(po[4,j] for j in range(offset,offset+len(fragment))),
                             fragment)
        receipt=json.loads((ROOT/(PREFIX+'string-plus-exception-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(native_round=row['round']):
                made=(ROOT/row['outputs']['oprplus']['path']).read_bytes()
                self.assertEqual(payload(made),po)
                self.assertEqual(literal_fields(made),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['oprplus'])
                self.assertFalse(row['original_program_equal_by_member']['oprplus'])
                self.assertNotEqual(object_program_records(made),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
