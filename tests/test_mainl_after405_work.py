"""Original streambuf bulk get/put: all CODE and literal Borland FIXUPPs."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after405_work import (PREFIX,WORK,NATIVE,MODES,
    retained,original_library_member)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after405_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz

MODE='two-streambuf-bulk-transfer-bosses'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalStreambufBulkTransfer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound streambuf pair receipt absent')
    def test_entire_input_output_bosses_and_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,563,330))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (352,164202))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertEqual(len(r['profiles']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'source-bound streambuf pair receipt absent')
    def test_each_exact_texta_public_and_original_ordered_memcpy_fixup(self):
        _,_,_,members,carry,_=retained()
        names=MODES[MODE]
        self.assertEqual(len(names),2)
        self.assertFalse(set(names)&set(carry[0][0]))
        report=json.loads(RECEIPT.read_text())
        for n,size,site,pub in [
                ('stbdsgtn',184,62,'@streambuf@do_sgetn$qnci'),
                ('stbdsptn',168,49,'@streambuf@do_sputn$qnxci')]:
            orig=original_library_member(members[NATIVE[n]['index']])
            P=payload(orig)
            F=literal_fields(orig)
            self.assertEqual(len(P),size)
            self.assertEqual(code_publics(orig,1),[(0,pub)])
            self.assertEqual(externs(orig),['_memcpy'])
            self.assertEqual([(f['site'],f['location_type'],f['frame_method'],
                               f['target_method'],f['target']) for f in F],
                             [(site,3,5,2,1)])
            for row in report['rounds']:
                with self.subTest(name=n,round=row['round']):
                    made=(ROOT/row['outputs'][n]['path']).read_bytes()
                    self.assertEqual(payload(made),P)
                    self.assertEqual(literal_fields(made),F)
                    self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
                    self.assertFalse(row['original_program_equal_by_member'][n])
        for row in report['rounds']:
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__': unittest.main()
