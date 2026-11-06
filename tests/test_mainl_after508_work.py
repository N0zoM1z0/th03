"""Original Borland DOS dup/dup2, descriptor flags and FAR close handler."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after508_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after508_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-dup-dup2-close-callback-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDup(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'original dup source receipt absent')
    def test_two_complete_native_original_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,716,177))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(116,187412))
        self.assertEqual((r['profiles']['dup2']['CODE_bytes'],
                          r['profiles']['dup2']['DATA_bytes']),(116,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS dup2 OMF absent')
    def test_both_far_entries_and_all_14_literal_fixups(self):
        _,_,_,members,_,_=retained()
        original=original_library_member(members[NATIVE['dup2']['index']])
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),116)
        self.assertEqual(code_publics(original,1),[(0,'_dup2'),(59,'_dup')])
        self.assertEqual(externs(original),['__IOERROR','__openfd','__exitopen','__xclose'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual(len(F),14)
        self.assertEqual({f['site'] for f in F},
                         {24,33,37,39,43,45,53,82,90,94,96,100,102,110})
        bysite={f['site']:f for f in F}
        self.assertEqual((bysite[37]['target_method'],bysite[37]['target'],
                          bysite[37]['addend']),(2,3,2))
        self.assertEqual((bysite[39]['location_type'],bysite[39]['target_method'],
                          bysite[39]['target']),(2,2,4))
        self.assertEqual((bysite[94]['target_method'],bysite[94]['target'],
                          bysite[94]['addend']),(2,3,2))
        for site in (53,110):
            self.assertEqual((bysite[site]['target_method'],bysite[site]['target'],
                              bysite[site]['frame_method']),(2,1,0))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['dup2']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(literal_fields(obj),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['dup2'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
