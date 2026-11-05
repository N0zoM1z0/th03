"""Original NEC PC98 function-key BIOS + full near/far Japanese MBCS strchr."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after364_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after364_work import review

SIZES={'pc98fkey':80,'MBSCHR':116,'FMBSCHR':116}

class OriginalPC98FunctionKeyMBCS(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'pc98-function-key-and-mbschr-build.json')).is_file(),
                         'Japanese 431-source native PC98 and MBCS receipts absent')
    def test_complete_three_original_members_and_native_links(self):
        r=review('pc98-function-key-and-mbschr')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,431,462))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (312,136836))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),1)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'pc98-function-key-and-mbschr-build.json')).is_file(),
                         'actual original/compiled OBJ and MZ pairs absent')
    def test_nec_bios_escape_sequence_and_mbsctype_relocs(self):
        _,_,_,members,_,_=retained()
        receipt=json.loads((ROOT/(PREFIX+'pc98-function-key-and-mbschr-build.json')).read_text())
        for n in SIZES:
            old=original_library_member(members[NATIVE[n]['index']])
            f=literal_fields(old)
            self.assertEqual(len(f),1)
            if n=='pc98fkey':
                self.assertEqual((f[0]['site'],f[0]['target_method'],
                                  f[0]['target'],f[0]['addend'],f[0]['frame_method']),
                                 (6,0,1,14,5))
                data=payload(old)
                self.assertEqual(bytes(data[1,i] for i in range(14,19)),
                                 b'\x1b[>1\x00')
                self.assertEqual(bytes(data[1,i] for i in range(19,21)),b'\xcd\xdc')
            else:
                self.assertEqual((f[0]['site'],f[0]['target_method'],
                                  f[0]['target'],f[0]['addend'],
                                  f[0]['frame_method'],f[0]['frame']),
                                 (17,2,1,1,1,1))
            for row in receipt['rounds']:
                with self.subTest(member=n,round=row['round']):
                    obj=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(obj),payload(old))
                    self.assertEqual(literal_fields(obj),f)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(obj),
                                        members[NATIVE[n]['index']].program_records)
        for row in receipt['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
