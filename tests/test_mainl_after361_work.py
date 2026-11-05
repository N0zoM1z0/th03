"""Complete original Borland diagnostic boss: native CODE, DATA, RTTI, INIT/EXIT."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after361_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from review_th03_mainl_after361_work import review

class OriginalDiagnosticChecksBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'diagnostic-checks-boss-build.json')).is_file(),
                         'source-bound Japanese 421-member native producer receipts absent')
    def test_complete_borland_diagnostics_and_exact_link(self):
        r=review('diagnostic-checks-boss')
        p=r['profiles']['checks']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,421,472))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1708,135508))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes'],p['INITDATA_bytes'],
                          p['EXITDATA_bytes']),(221,1487,1708,143,0,6,6))
        self.assertEqual(p['publics'],NATIVE['checks']['publics'])
        self.assertEqual(p['data_publics'],NATIVE['checks']['data_publics'])
        self.assertEqual(p['imports'],NATIVE['checks']['imports'])
        self.assertEqual(len(p['relocation_sites_targets']),89)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'diagnostic-checks-boss-build.json')).is_file(),
                         'raw original and TASM OBJ/LIB/EXE vectors absent')
    def test_actual_omf_89_fields_143_materialized_data_and_mz(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['checks']['index']])
        data=payload(original)
        self.assertEqual(len(data),1708+143+6+6)
        self.assertEqual(bytes(data[2,i] for i in range(5,103)),bytes(98))
        self.assertEqual(bytes(data[2,i] for i in range(103,107)),b'Def\x00')
        self.assertEqual(bytes(data[2,i] for i in range(123,131)),b'Warning\x00')
        self.assertEqual(bytes(data[5,i] for i in range(6)),
                         bytes.fromhex('01 20 80 00 00 00'))
        self.assertEqual(bytes(data[6,i] for i in range(6)),
                         bytes.fromhex('01 20 c7 00 00 00'))
        fields=literal_fields(original)
        self.assertEqual(len(fields),89)
        self.assertEqual([f['segment'] for f in fields].count(4),66)
        self.assertEqual([f['segment'] for f in fields].count(1),20)
        receipt=json.loads((ROOT/(PREFIX+'diagnostic-checks-boss-build.json')).read_text())
        for row in receipt['rounds']:
            with self.subTest(round=row['round']):
                obj=(ROOT/row['outputs']['checks']['path']).read_bytes()
                self.assertEqual(payload(obj),data)
                self.assertEqual(sorted(literal_fields(obj),key=lambda f:(f['segment'],f['site'])),
                                 sorted(fields,key=lambda f:(f['segment'],f['site'])))
                self.assertEqual(literal_fields(obj),fields)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member']['checks'])
                self.assertFalse(row['original_program_equal_by_member']['checks'])
                self.assertNotEqual(object_program_records(obj),
                                    members[NATIVE['checks']['index']].program_records)
                exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
