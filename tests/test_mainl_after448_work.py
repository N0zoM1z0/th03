"""IBM console scroll, DBCS edge clearing and seven near-frame OMF gaps."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after448_work import (
    PREFIX, WORK, NATIVE, NEAR_FRAME_GAPS, retained, original_library_member)
from review_th03_mainl_after448_work import review
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='ibm-console-scroll-dbcs-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalIBMScroll(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'IBM scroll source receipt missing')
    def test_original_code_and_both_complete_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,656,237))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (184,176605))
        self.assertEqual((r['profiles']['cibmscrl']['CODE_bytes'],
                          r['profiles']['cibmscrl']['DATA_bytes']),(184,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original IBM scroll OMF missing')
    def test_original_global_targets_and_only_seven_proved_frame_gaps(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['cibmscrl']['index']]
        self.assertEqual(m.name,'cibmscrl')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),184)
        self.assertEqual(len(F),13)
        self.assertEqual(code_publics(orig,1),[(0,'__IBM_SCROLL')])
        self.assertEqual(externs(orig),NATIVE['cibmscrl']['imports'])
        sites={f['site']:f for f in F}
        self.assertEqual((sites[10]['target_method'],sites[10]['target']),
                         (2,2))   # wgarbage, first scroll guard
        self.assertEqual((sites[140]['target_method'],sites[140]['target']),
                         (2,1))   # wclrnorm, second color guard
        self.assertEqual([(s,NEAR_FRAME_GAPS['cibmscrl'][s])
                          for s in sorted(NEAR_FRAME_GAPS['cibmscrl'])],
                         [(43,4),(59,5),(68,5),(89,4),
                          (105,5),(114,5),(174,6)])
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            out=(ROOT/row['outputs']['cibmscrl']['path']).read_bytes()
            self.assertEqual(payload(out),P)
            made={f['site']:f for f in literal_fields(out)}
            self.assertEqual(set(made),set(sites))
            for site,original in sites.items():
                observed=made[site]
                remaining=set(original)-{'frame_method','frame'}
                self.assertEqual({k:original[k] for k in remaining},
                                 {k:observed[k] for k in remaining})
                if site in NEAR_FRAME_GAPS['cibmscrl']:
                    self.assertEqual((original['frame_method'],original['frame']),
                                     (5,None))
                    self.assertEqual((observed['frame_method'],observed['frame']),
                                     (0,1))
                else:
                    self.assertEqual(observed,original)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
