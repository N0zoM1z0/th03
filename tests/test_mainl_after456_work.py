"""Video-mode translation and complete gettextinfo native source."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after456_work import (
    PREFIX, WORK, NATIVE, NEAR_FRAME_GAPS, retained, original_library_member)
from review_th03_mainl_after456_work import review
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz

MODE='pc98-video-textinfo-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')

class OriginalVideoInfo(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native source receipt missing')
    def test_original_pc98_video_scope_and_two_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,664,229))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (231,178363))
        self.assertEqual((r['profiles']['vidinfo']['CODE_bytes'],
                          r['profiles']['vidinfo']['DATA_bytes']),(231,16))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original native OMF absent')
    def test_true_mode_table_and_exact_one_near_call_frame_exception(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['vidinfo']['index']]
        self.assertEqual(m.name,'vidinfo')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),247)
        self.assertEqual(len(F),14)
        self.assertEqual(code_publics(original,1),[(89,'_gettextinfo')])
        self.assertEqual(externs(original),NATIVE['vidinfo']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(16)),
                         bytes.fromhex('00000100040005000200030006000700'))
        self.assertEqual([r.data.hex() for r in parse_omf(original) if r.name=='GRPDEF'],
                         ['08ff02ff03'])
        self.assertEqual(NEAR_FRAME_GAPS, {'vidinfo':{192:2}})
        original_fields={f['site']:f for f in F}
        self.assertEqual((original_fields[27]['target_method'],
                          original_fields[27]['target']), (0,2))
        self.assertEqual((original_fields[192]['target_method'],
                          original_fields[192]['target']), (2,2))
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['vidinfo']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            fields={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(fields),set(original_fields))
            for site,orig in original_fields.items():
                actual=fields[site]
                if site==192:
                    self.assertEqual((orig['frame_method'],orig['frame']),(5,None))
                    self.assertEqual((actual['frame_method'],actual['frame']),(0,1))
                    keys=set(orig)-{'frame_method','frame'}
                    self.assertEqual({k:orig[k] for k in keys},
                                     {k:actual[k] for k in keys})
                else:
                    self.assertEqual(actual,orig)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
