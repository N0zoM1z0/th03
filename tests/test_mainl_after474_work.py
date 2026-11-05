"""Original DOS file EOF probe, seek restoration and ordered OMF fields."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after474_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after474_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-file-eof-seek-probe-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosEof(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS eof original receipt missing')
    def test_two_complete_native_original_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,682,211))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(125,182280))
        self.assertEqual((r['profiles']['eof']['CODE_bytes'],
                          r['profiles']['eof']['DATA_bytes']),(125,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS EOF OMF absent')
    def test_true_dos_ioctl_seek_and_literal_ioerror(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['eof']['index']]
        self.assertEqual(m.name,'eof')
        orig=original_library_member(m)
        P=payload(orig);F=literal_fields(orig)
        self.assertEqual(len(P),125)
        self.assertEqual(len(F),3)
        self.assertEqual(code_publics(orig,1),[(0,'_eof')])
        self.assertEqual(externs(orig),['__nfile','__IOERROR','__openfd'])
        self.assertEqual([r.data.hex() for r in parse_omf(orig) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual({f['site']:(f['target_method'],f['target']) for f in F},
                         {13:(2,1),30:(2,3),117:(2,2)})
        self.assertEqual((P[1,0x2e],P[1,0x2f],P[1,0x3e],P[1,0x3f]),
                         (0xcd,0x21,0xcd,0x21))
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['eof']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(literal_fields(obj),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['eof'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
