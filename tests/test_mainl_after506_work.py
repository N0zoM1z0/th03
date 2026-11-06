"""Original Borland DOS _creat, dynamic exitclose FAR pointer and OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after506_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after506_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-creat-exitopen-close-callback-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalCreat(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native creat source receipt absent')
    def test_two_original_complete_native_mainl_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,714,179))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(156,187199))
        self.assertEqual((r['profiles']['creat']['CODE_bytes'],
                          r['profiles']['creat']['DATA_bytes']),(156,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original creat OMF missing')
    def test_real_dos_creat_and_nine_literal_callbacks(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['creat']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),156)
        self.assertEqual(code_publics(raw,1),[(31,'_creat')])
        self.assertEqual(externs(raw),['_ioctl','__IOERROR','__openfd',
                                      '__fmode','__exitopen','__xclose','__notUmask'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        bysite={f['site']:f for f in F}
        self.assertEqual(set(bysite),{23,40,79,81,85,87,96,115,145})
        self.assertEqual((bysite[79]['target_method'],bysite[79]['target'],
                          bysite[79]['addend']),(2,5,2))
        self.assertEqual((bysite[81]['target_method'],bysite[81]['target'],
                          bysite[81]['location_type']),(2,6,2))
        self.assertEqual((bysite[85]['target_method'],bysite[85]['target'],
                          bysite[85]['addend']),(2,5,0))
        self.assertEqual((bysite[87]['target_method'],bysite[87]['target'],
                          bysite[87]['location_type']),(2,6,1))
        receipt=json.loads(RECEIPT.read_text())
        for round in receipt['rounds']:
            made=(ROOT/round['outputs']['creat']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(round['literal_omf_fixupp_equal_by_member']['creat'])
            exe=(ROOT/round['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
