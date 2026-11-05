"""Original ostream() default constructor, embedded ios and typed RTTI."""
import sys
import json
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after445_work import PREFIX, WORK, NATIVE, retained, original_library_member
from review_th03_mainl_after445_work import review
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz

MODE='ostream-default-constructor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalOstreamDefaultConstructor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native ostream constructor receipt missing')
    def test_complete_original_scope_and_two_native_rounds(self):
        result=review(MODE)
        self.assertEqual((result['original_CRT_members'], result['native_source_members'],
                          result['untouched_vendor_members']),(893,653,240))
        self.assertEqual((result['added_CODE_bytes'], result['source_CRT_CODE_bytes']),
                         (245,176015))
        self.assertEqual((result['profiles']['ostctr1']['CODE_bytes'],
                          result['profiles']['ostctr1']['DATA_bytes']),(245,20))
        self.assertEqual(result['native_rounds'],2)
        self.assertEqual(result['original_MZ_relocations'],677)
        self.assertTrue(result['complete_original_CODE_DATA_equal'])
        self.assertTrue(result['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(result['original_literal_FIXUPP_equal'])
        self.assertFalse(result['source_acceptance'])
        self.assertFalse(result['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original ostream object OMF missing')
    def test_real_typed_rtti_dual_vtable_and_this_adjuster(self):
        _,_,_,members,_,_=retained()
        member=members[NATIVE['ostctr1']['index']]
        self.assertEqual(member.name,'ostctr1')
        original=original_library_member(member)
        P=payload(original); F=literal_fields(original)
        self.assertEqual(len(P),265)
        self.assertEqual(len(F),12)
        self.assertEqual(code_publics(original,1),[(0,'@ostream@$bctr$qv')])
        self.assertEqual(externs(original),NATIVE['ostctr1']['imports'])
        self.assertEqual(bytes(P[2,i] for i in range(20)),
                         bytes.fromhex('7d00000000000000000000000400080071000000'))
        self.assertIn(b'ostream\0',bytes(P[1,i] for i in range(245)))
        sites={(f['segment'],f['site']):f for f in F}
        self.assertEqual((sites[1,75]['target_method'],sites[1,75]['target'],
                          sites[1,75]['addend']),(0,2,8))
        self.assertEqual((sites[1,83]['target_method'],sites[1,83]['target'],
                          sites[1,83]['addend']),(0,2,16))
        self.assertEqual((sites[2,0]['target_method'],sites[2,0]['target'],
                          sites[2,0]['addend']),(0,1,125))
        self.assertEqual((sites[2,16]['target_method'],sites[2,16]['target'],
                          sites[2,16]['addend']),(0,1,113))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['ostctr1']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
