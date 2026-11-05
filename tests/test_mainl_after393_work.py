"""Two full Borland C++ array constructor bosses and native two-round link."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),7000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after393_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after393_work import review
from lib.pc98 import parse_mz

MODE='vector-constructor-bosses'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalCxxVectorConstructors(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source-built vector constructor evidence missing')
    def test_full_bosses_and_reproducible_japanese_native_product(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,534,359))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (658,160990))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native source-built vector constructor evidence missing')
    def test_seven_original_table_fixups_in_each_complete_member(self):
        _,_,_,members,_,_=retained()
        record=json.loads(RECEIPT.read_text())
        for name,index,size,table,table_off in (
                ('vnew',144,313,'bf00c800d100d900e100ee00fb00',299),
                ('vnewv',147,345,'c000cd00da00e500f00001011201',331)):
            with self.subTest(name=name):
                self.assertEqual(NATIVE[name]['index'],index)
                orig=original_library_member(members[index]);P=payload(orig)
                F=literal_fields(orig)
                self.assertEqual(len(P),size)
                self.assertEqual(bytes(P[1,i] for i in range(table_off,table_off+14)),
                                 bytes.fromhex(table))
                self.assertEqual(len(F),9)
                self.assertEqual([f['site'] for f in F[:7]],
                                 list(range(size-2,size-16,-2)))
                for row in record['rounds']:
                    made=(ROOT/row['outputs'][name]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(made)),
                                     sorted(tuple(f[k] for k in KEYS) for f in F))
                    self.assertFalse(row['literal_omf_fixupp_equal_by_member'][name])
                    self.assertFalse(row['original_program_equal_by_member'][name])
        for row in record['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
