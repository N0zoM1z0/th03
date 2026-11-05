"""Complete Japanese Borland streambuf::dbp with true format DATA."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after342_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after342_work import review


class OriginalStreambufDebugPrint(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-debug-printer-build.json')).is_file(),
                         'native 376-source Japanese OBJ/EXE receipts absent')
    def test_complete_streambuf_printer_and_japanese_full_link(self):
        r=review('streambuf-debug-printer')
        p=r['profiles']['stbdbp']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,376,517))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (281,121643))
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (281,126,0))
        self.assertEqual(p['publics'],[(0,'@streambuf@dbp$qv')])
        self.assertEqual(p['imports'],['_write','_sprintf','_strlen'])
        self.assertEqual(len(p['relocation_sites_targets']),16)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-debug-printer-build.json')).is_file(),
                         'original/compiled two-round OMF pair absent')
    def test_all_original_code_and_four_real_debug_strings(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['stbdbp']['index']])
        original_payload=payload(original)
        data=bytes(original_payload[2,i] for i in range(126))
        self.assertEqual(data,b'alloc_ = %d, unbuf_ = %d\n\0'
                         b'base_ = %p, ebuf_ = %p\n\0'
                         b'pbase_ = %p, pptr_ = %p, epptr_ = %p\n\0'
                         b'gptr_ = %p, egptr_ = %p, eback_ = %p\n\0')
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['08ff02ff03'])
        fields=literal_fields(original)
        self.assertEqual(len(fields),16)
        relocs={f['site']:f for f in fields}
        for site,target in ((21,0),(85,26),(157,50),(229,88)):
            self.assertEqual((relocs[site]['target_method'],relocs[site]['target'],
                              relocs[site]['addend'],relocs[site]['frame_method']),
                             (0,2,target,1))
        record=json.loads((ROOT/(PREFIX+'streambuf-debug-printer-build.json')).read_text())
        for row in record['rounds']:
            with self.subTest(round=row['round']):
                made=(ROOT/row['outputs']['stbdbp']['path']).read_bytes()
                self.assertEqual(payload(made),original_payload)
                self.assertEqual(sorted(literal_fields(made),key=lambda f:f['site']),
                                 sorted(fields,key=lambda f:f['site']))
                self.assertNotEqual(literal_fields(made),fields)
                self.assertNotEqual(object_program_records(made),
                                    members[NATIVE['stbdbp']['index']].program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
