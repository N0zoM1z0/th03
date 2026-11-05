"""Complete original 333-byte Borland filebuf::overflow virtual I/O routine."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after359_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after359_work import review

class OriginalFilebufOverflow(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'filebuf-overflow-boss-build.json')).is_file(),
                         'original 412-source native Japanese receipts absent')
    def test_complete_filebuf_overflow_and_native_full_link(self):
        r=review('filebuf-overflow-boss')
        p=r['profiles']['fsboflow']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,412,481))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (333,133078))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (333,0,0))
        self.assertEqual(p['publics'],[(0,'@filebuf@overflow$qi')])
        self.assertEqual(p['imports'],['_write','@streambuf@setp$qnct1',
                                        '@streambuf@setg$qnct1t1'])
        self.assertEqual(len(p['relocation_sites_targets']),3)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'filebuf-overflow-boss-build.json')).is_file(),
                         'native source OBJ/linked EXE pairs absent')
    def test_three_original_borland_import_fixups_and_literal_order(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsboflow']['index']]
        self.assertEqual(m.name,'fsboflow')
        old=original_library_member(m)
        original=payload(old)
        fields=literal_fields(old)
        self.assertEqual([(f['site'],f['target_method'],f['target'],f['frame_method'])
                          for f in fields],[(244,2,3,5),(210,2,2,5),(82,2,1,5)])
        self.assertEqual(len(original),333)
        receipt=json.loads((ROOT/(PREFIX+'filebuf-overflow-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(native_round=row['round']):
                obj=(ROOT/row['outputs']['fsboflow']['path']).read_bytes()
                self.assertEqual(payload(obj),original)
                self.assertEqual(literal_fields(obj),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['fsboflow'])
                self.assertFalse(row['original_program_equal_by_member']['fsboflow'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
