"""Complete original NEC PC-98 text scroll and five specific near frames."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after413_work import (PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,
    retained,original_library_member,scope)
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after413_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='nec-console-scroll-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalNecConsoleScroll(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound NEC scroll receipt absent')
    def test_entire_original_nec_scroll_and_native_link(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,589,304))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (170,166254))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native original NEC scroll pair absent')
    def test_exact_code_only_five_external_near_call_frame_gaps(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cnecscrl']['index']]
        self.assertEqual(m.name,'cnecscrl')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),170)
        self.assertEqual(code_publics(orig,1),[(0,'__NEC_SCROLL')])
        self.assertEqual(externs(orig),['__MOVETEXT','__NEC_ZAP_LINE'])
        self.assertEqual([x['site'] for x in F],[150,136,93,79,34])
        self.assertEqual(NEAR_FRAME_GAPS['cnecscrl'],
                         {34:2,79:1,93:2,136:1,150:2})
        raw=bytes(P[1,i] for i in range(170))
        self.assertEqual(raw[-3:],bytes.fromhex('c20c00'))
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['cnecscrl']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(scope('cnecscrl',made),scope('cnecscrl',orig))
            G=literal_fields(made)
            self.assertEqual(len(G),5)
            self.assertNotEqual(G,F)
            self.assertFalse(row['literal_omf_fixupp_equal_by_member']['cnecscrl'])
            original_by_site={f['site']:f for f in F}
            new_by_site={f['site']:f for f in G}
            self.assertEqual(set(original_by_site),set(new_by_site))
            for site in NEAR_FRAME_GAPS['cnecscrl']:
                before=original_by_site[site];after=new_by_site[site]
                self.assertEqual((before['frame_method'],before['frame']),(5,None))
                self.assertEqual((after['frame_method'],after['frame']),(0,1))
                self.assertEqual(before['target'],after['target'])
                self.assertEqual(before['target'],NEAR_FRAME_GAPS['cnecscrl'][site])
                self.assertEqual(before['addend'],after['addend'])
                self.assertEqual(before['location_type'],after['location_type'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
