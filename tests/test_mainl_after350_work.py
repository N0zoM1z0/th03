"""Complete original Japanese Borland flushall/xfflush CRT source members."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after350_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from build_th03_mainl_resources_work import sha
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after350_work import review

SIZES={'flushall':76,'xfflush':63}

class OriginalFlushFinalizers(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'stdio-flush-finalizers-build.json')).is_file(),
                         'native 397-source Japanese CRT receipt absent')
    def test_entire_original_139_bytes_and_two_native_links(self):
        r=review('stdio-flush-finalizers')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,397,496))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (139,127393))
        for n,size in SIZES.items():
            with self.subTest(member=n):
                p=r['profiles'][n]
                self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                                 (size,0,0))
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

    @unittest.skipUnless((ROOT/(PREFIX+'stdio-flush-finalizers-build.json')).is_file(),
                         'original/source full OMF raw pair absent')
    def test_original_vendor_reversed_fixup_order_and_include_hash(self):
        _,_,_,members,_,_=retained()
        rec=json.loads((ROOT/(PREFIX+'stdio-flush-finalizers-build.json')).read_text())
        self.assertEqual(rec['include_source_path'],'src/mainl/crt/stdio_layout.inc')
        self.assertEqual(rec['include_sha256'],sha((ROOT/rec['include_source_path']).read_bytes()))
        for n in SIZES:
            orig=original_library_member(members[NATIVE[n]['index']])
            vendor=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(payload(orig),payload(vendor))
            self.assertEqual(sorted(literal_fields(orig),key=lambda f:(f['segment'],f['site'])),
                             sorted(literal_fields(vendor),key=lambda f:(f['segment'],f['site'])))
            self.assertNotEqual(literal_fields(orig),literal_fields(vendor))
            self.assertEqual([r.data.hex() for r in parse_omf(orig)
                              if r.name=='GRPDEF'],[NATIVE[n]['group']])
            for row in rec['rounds']:
                with self.subTest(member=n,round=row['round']):
                    obj=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(obj),payload(orig))
                    self.assertEqual(literal_fields(obj),literal_fields(orig))
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
                    self.assertNotEqual(object_program_records(obj),
                                        members[NATIVE[n]['index']].program_records)
        for row in rec['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
