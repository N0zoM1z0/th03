"""Original strstreambuf destructor with callback/array cleanup and vtable."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after435_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after435_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='strstreambuf-complete-destructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative','frame_method','frame','target_method','target','addend')

class OriginalStrstreambufDestructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound destructor native receipt absent')
    def test_complete_source_and_two_original_japanese_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,643,250))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(265,173686))
        self.assertEqual((r['profiles']['srbdtr']['CODE_bytes'],r['profiles']['srbdtr']['DATA_bytes']),(265,52))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original destructor source/OBJ absent')
    def test_original_far_delete_callback_and_twenty_full_omf_fields(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['srbdtr']['index']]
        self.assertEqual(m.name,'srbdtr')
        orig=original_library_member(m);P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),317)
        self.assertEqual(len(F),20)
        self.assertEqual(code_publics(orig,1),[(0,'@strstreambuf@$bdtr$qv')])
        self.assertEqual(externs(orig),NATIVE['srbdtr']['imports'])
        code=bytes(P[1,i] for i in range(265))
        self.assertIn(bytes.fromhex('26ff5f2a'),code) # real far cleanup callback
        self.assertEqual(bytes(P[2,i] for i in range(52)),
                         bytes.fromhex('8500')+bytes(50))
        by={(f['segment'],f['site']):f for f in F}
        self.assertEqual((by[(1,37)]['target_method'],by[(1,37)]['target'],by[(1,37)]['addend']),
                         (0,2,8))
        self.assertEqual((by[(1,87)]['target_method'],by[(1,87)]['target']),(2,2)) # delete[]
        self.assertEqual((by[(1,103)]['target_method'],by[(1,103)]['target']),(2,4)) # base destructor
        self.assertEqual((by[(1,123)]['target_method'],by[(1,123)]['target']),(2,1)) # delete object
        self.assertEqual((by[(2,8)]['target_method'],by[(2,8)]['target'],by[(2,8)]['addend']),
                         (0,1,0))
        self.assertEqual((by[(2,28)]['target_method'],by[(2,28)]['target']),(2,7))
        self.assertEqual((by[(2,32)]['target_method'],by[(2,32)]['target']),(2,10))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        record=json.loads(RECEIPT.read_text())
        for q in record['rounds']:
            blob=(ROOT/q['outputs']['srbdtr']['path']).read_bytes()
            self.assertEqual(payload(blob),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS) for f in literal_fields(blob)),expected)
            self.assertNotEqual(literal_fields(blob),F)
            self.assertFalse(q['literal_omf_fixupp_equal_by_member']['srbdtr'])
            exe=(ROOT/q['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':unittest.main()
