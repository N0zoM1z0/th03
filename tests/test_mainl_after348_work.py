"""Source-bound full original Japanese CRT write/setvbuf/fflush members."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after348_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from build_th03_mainl_resources_work import sha
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after348_work import review

SIZES={'write':358,'setvbuf':289,'fflush':209}

class OriginalStdioWriteBufferFlush(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).exists(),
                         'retained original 393-source native receipts absent')
    def test_complete_original_members_and_native_link(self):
        r=review('stdio-write-buffer-flush')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,393,500))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (856,127006))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,4 if n=='setvbuf' else 0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),NATIVE[n]['fields'])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).exists(),
                         'raw original and native OBJ pair absent')
    def test_each_member_literal_fixups_and_stdio_constants_source_hash(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).read_text())
        self.assertEqual(receipt['include_source_path'],'src/mainl/crt/stdio_layout.inc')
        self.assertEqual(receipt['include_sha256'],sha((ROOT/receipt['include_source_path']).read_bytes()))
        for n in SIZES:
            orig=original_library_member(members[NATIVE[n]['index']])
            for row in receipt['rounds']:
                with self.subTest(member=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),payload(orig))
                    self.assertEqual(literal_fields(made),literal_fields(orig))
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(made),
                                        members[NATIVE[n]['index']].program_records)
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
