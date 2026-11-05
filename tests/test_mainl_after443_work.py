"""Original filebuf::attach descriptor, buffer allocation and get/put setup."""
import json
import sys
import unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(), 9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after443_work import PREFIX, WORK, NATIVE, retained, original_library_member
from build_th03_mainl_display_work import payload, literal_fields
from review_th03_mainl_after443_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='filebuf-attach-descriptor-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')

class OriginalFilebufAttach(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original filebuf attach receipt missing')
    def test_full_original_code_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,651,242))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (238,175516))
        self.assertEqual((r['profiles']['fsbattch']['CODE_bytes'],
                          r['profiles']['fsbattch']['DATA_bytes']), (238,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless(RECEIPT.is_file(),'native filebuf attach OMF missing')
    def test_original_symbolic_allocation_and_put_get_calls(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['fsbattch']['index']]
        self.assertEqual(m.name,'fsbattch')
        orig=original_library_member(m)
        P=payload(orig)
        F=literal_fields(orig)
        self.assertEqual(len(P),238)
        self.assertEqual(len(F),4)
        self.assertEqual(code_publics(orig,1),[(0,'@filebuf@attach$qi')])
        self.assertEqual(externs(orig),NATIVE['fsbattch']['imports'])
        sites={f['site']:f for f in F}
        self.assertEqual([(site,sites[site]['target_method'],sites[site]['target'])
                          for site in sorted(sites)],[(71,2,1),(110,2,4),(185,2,2),(219,2,3)])
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['fsbattch']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)

if __name__=='__main__':
    unittest.main()
