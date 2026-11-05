"""Native source review of original strstreambuf allocation fallback and setb."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after446_work import PREFIX, WORK, NATIVE, retained, original_library_member
from review_th03_mainl_after446_work import review
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.pc98 import parse_mz
MODE='strstreambuf-dynamic-doallocate'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class StrstreambufDoallocate(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound strstreambuf allocator missing')
    def test_full_original_allocation_and_two_native_rounds(self):
        record=review(MODE)
        self.assertEqual((record['original_CRT_members'],record['native_source_members'],
                          record['untouched_vendor_members']),(893,654,239))
        self.assertEqual((record['added_CODE_bytes'],record['source_CRT_CODE_bytes']),
                         (141,176156))
        self.assertEqual((record['profiles']['srbdalc']['CODE_bytes'],
                          record['profiles']['srbdalc']['DATA_bytes']),(141,0))
        self.assertEqual(record['native_rounds'],2)
        self.assertEqual(record['original_MZ_relocations'],677)
        self.assertTrue(record['complete_original_CODE_DATA_equal'])
        self.assertTrue(record['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(record['original_literal_FIXUPP_equal'])
        self.assertFalse(record['source_acceptance'])
        self.assertFalse(record['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'original allocation OMF missing')
    def test_callback_fallback_and_symbolic_setb_relocations(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['srbdalc']['index']]
        self.assertEqual(m.name,'srbdalc')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),141)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(orig,1),[(0,'@strstreambuf@doallocate$qv')])
        self.assertEqual(externs(orig),['@$bnwa$qui','@streambuf@setb$qnct1i'])
        sites={f['site']:f for f in F}
        self.assertEqual((sites[61]['target_method'],sites[61]['target']), (2,1))
        self.assertEqual((sites[118]['target_method'],sites[118]['target']), (2,2))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        record=json.loads(RECEIPT.read_text())
        for row in record['rounds']:
            made=(ROOT/row['outputs']['srbdalc']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
