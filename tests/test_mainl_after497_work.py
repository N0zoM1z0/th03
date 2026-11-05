"""Original DOS no-echo getpass, nine-byte BSS and exact nine OMF fields."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after497_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after497_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-getpass-noecho-bss-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
class OriginalGetpass(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'getpass native receipt missing')
    def test_complete_original_two_native_mainl_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,705,188))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(168,185995))
        self.assertEqual((r['profiles']['getpass']['CODE_bytes'],
                          r['profiles']['getpass']['DATA_bytes'],
                          r['profiles']['getpass']['BSS_bytes']),(168,3,9))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original getpass OMF missing')
    def test_typed_prompt_static_buffer_and_real_dos_bdos(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['getpass']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),171)
        self.assertEqual(code_publics(original,1),[(24,'_getpass')])
        self.assertEqual(externs(original),['__streams','_fprintf','_bdos'])
        self.assertEqual(bytes(P[2,i] for i in range(3)),b'%s\x00')
        self.assertEqual((segment_definitions(original)[2]['name'],
                          segment_definitions(original)[2]['size']),('_BSS',9))
        self.assertFalse(any(s==3 for s,i in P))
        self.assertEqual(len(F),9)
        original_fields=sorted(tuple(f[k] for k in KEYS) for f in F)
        self.assertEqual({f['site'] for f in F},{14,40,45,49,66,82,130,146,160})
        self.assertEqual({f['site']:f['target'] for f in F if f['target_method']==2},
                         {14:3,45:1,49:2,82:3,130:3,146:3})
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['getpass']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),original_fields)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
