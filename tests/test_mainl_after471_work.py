"""Original DOS int86/int86x dynamic interrupt trampoline and FLAGS ABI."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after471_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after471_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-int86-int86x-register-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosInterruptBridge(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS interrupt source receipt missing')
    def test_both_original_far_functions_and_complete_links(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,679,214))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(207,181827))
        self.assertEqual((r['profiles']['int86']['CODE_bytes'],
                          r['profiles']['int86']['DATA_bytes']),(207,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original interrupt OMF unavailable')
    def test_real_runtime_int_trampoline_and_ordered_fixups(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['int86']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),207)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(raw,1),[(0,'_int86'),(53,'_int86x')])
        self.assertEqual(externs(raw),['_segread','__IOERROR'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {14:(2,1),198:(2,2)})
        self.assertEqual(bytes(P[1,i] for i in range(0x47,0x4b)),
                         bytes.fromhex('c646f255'))
        self.assertEqual(bytes(P[1,i] for i in range(0x91,0x95)),
                         bytes.fromhex('f8ff5efc'))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['int86']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['int86'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
