"""Original Borland stdio startup, FILE modes and exact INITDATA OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after493_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after493_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='stdio-startup-stream-initdata-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalStdioInitializer(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original __setupio receipt absent')
    def test_two_complete_original_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,701,192))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(164,185517))
        self.assertEqual((r['profiles']['setupio']['CODE_bytes'],
                          r['profiles']['setupio']['DATA_bytes'],
                          r['profiles']['setupio']['INITDATA_bytes']),(164,0,6))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original __setupio INITDATA OMF missing')
    def test_real_initdata_function_pointer_and_stream_state_targets(self):
        _,_,_,members,_,_=retained()
        orig=original_library_member(members[NATIVE['setupio']['index']])
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),170)
        self.assertEqual(len(F),18)
        self.assertEqual(code_publics(orig,1),[(0,'__setupio')])
        self.assertEqual(externs(orig),
                         ['__streams','__nfile','_setvbuf','_isatty','__openfd'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig)
                          if r.name=='GRPDEF'],['0aff03ff02'])
        self.assertEqual(bytes(P[4,i] for i in range(6)),
                         bytes.fromhex('000200000000'))
        refs={(f['segment'],f['site']):f for f in F}
        self.assertEqual((refs[1,13]['target_method'],refs[1,13]['target']),(2,5))
        for site in (28,32,38,48,64,74,93,105,121,131,150):
            self.assertEqual((refs[1,site]['target_method'],refs[1,site]['target']),
                             (2,1))
        self.assertEqual((refs[4,2]['location_type'],refs[4,2]['target_method'],
                          refs[4,2]['target'],refs[4,2]['addend']),
                         (1,0,1,0))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['setupio']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['setupio'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
