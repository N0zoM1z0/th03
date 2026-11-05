"""Original Borland clock() BSS baseline and CRT INITDATA registration."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after500_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after500_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-clock-baseline-initdata-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosClock(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native clock receipt absent')
    def test_complete_source_and_two_original_native_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,708,185))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(113,186434))
        self.assertEqual((r['profiles']['clock0']['CODE_bytes'],
                          r['profiles']['clock0']['BSS_bytes'],
                          r['profiles']['clock0']['INITDATA_bytes']),(113,6,6))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original clock OMF missing')
    def test_symbolic_initializer_and_single_near_frame_exception(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['clock0']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),119)
        self.assertEqual(code_publics(original,1),[(0,'_clock')])
        self.assertEqual(externs(original),['__ftime','N_LXMUL@'])
        self.assertEqual(segment_definitions(original)[2]['size'],6)
        self.assertEqual(bytes(P[4,i] for i in range(6)),bytes.fromhex('011f44000000'))
        self.assertEqual(NEAR_FRAME_GAPS,{'clock0':{40:2}})
        self.assertEqual(len(F),10)
        by_key={(f['segment'],f['site']):f for f in F}
        self.assertEqual((by_key[4,2]['target_method'],by_key[4,2]['target'],
                          by_key[4,2]['addend']),(0,1,68))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['clock0']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            actual={(f['segment'],f['site']):f for f in literal_fields(made)}
            self.assertEqual(set(actual),set(by_key))
            for key,old in by_key.items():
                new=actual[key]
                if key==(1,40):
                    self.assertEqual((old['frame_method'],old['frame']),(5,None))
                    self.assertEqual((new['frame_method'],new['frame']),(0,1))
                    for f in set(old)-{'frame_method','frame'}:self.assertEqual(old[f],new[f])
                else:self.assertEqual(old,new)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
