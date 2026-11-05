"""Original Borland write/setvbuf/fflush: complete code, data, OMF and link."""
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
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
from review_th03_mainl_after348_work import review

SIZES={'write':(358,0,9),'setvbuf':(289,4,13),'fflush':(209,0,2)}

class OriginalStdioWriteBufferFlush(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).is_file(),
                         'scoped 393-source original Japanese receipts absent')
    def test_all_three_complete_native_functions_and_full_link(self):
        r=review('stdio-write-buffer-flush')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,393,500))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (856,127006))
        self.assertEqual(set(r['profiles']),set(SIZES))
        for n,(code,data,fixups) in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (code,data,0))
                self.assertEqual(p['publics'],NATIVE[n]['publics'])
                self.assertEqual(p['imports'],NATIVE[n]['imports'])
                self.assertEqual(len(p['relocation_sites_targets']),fixups)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).is_file(),
                         'raw original/source OBJ and EXE/MAP receipts unavailable')
    def test_all_raw_omf_fields_include_binding_and_vendor_frame_gap(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'stdio-write-buffer-flush-build.json')).read_text())
        inc='src/mainl/crt/stdio_layout.inc'
        self.assertEqual((rec['include_source_path'],rec['include_sha256']),
                         (inc,sha((ROOT/inc).read_bytes())))
        for n,(code,data,count) in SIZES.items():
            original=original_library_member(members[NATIVE[n]['index']])
            vendor=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(payload(original),payload(vendor))
            self.assertEqual(externs(original),externs(vendor))
            fields=literal_fields(original)
            self.assertEqual(len(fields),count)
            if n=='setvbuf':
                self.assertEqual(bytes(payload(original)[2,i] for i in range(4)),
                                 b'\x00\x00\x00\x00')
            if n=='write':
                o={f['site']:f for f in fields}
                v={f['site']:f for f in literal_fields(vendor)}
                self.assertEqual({k for k in o if o[k]!=v[k]}, {23})
                self.assertEqual((o[23]['frame_method'],v[23]['frame_method']),(0,5))
                self.assertEqual((o[23]['target'],o[23]['site']),(4,23))
            else:
                self.assertEqual(sorted(fields,key=lambda f:f['site']),
                                 sorted(literal_fields(vendor),key=lambda f:f['site']))
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    obj=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(obj),payload(original))
                    self.assertEqual(literal_fields(obj),fields)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(obj),
                                        members[NATIVE[n]['index']].program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
