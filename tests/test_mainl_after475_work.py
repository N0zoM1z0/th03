"""Original DOS chsize growth, truncation, position restoration and OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after475_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after475_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-file-chsize-grow-truncate-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosChsize(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native resize receipt missing')
    def test_complete_original_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,683,210))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(199,182479))
        self.assertEqual((r['profiles']['chsize']['CODE_bytes'],
                          r['profiles']['chsize']['DATA_bytes']),(199,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original chsize member unavailable')
    def test_zero_fill_loop_and_literal_two_original_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['chsize']['index']]
        self.assertEqual(m.name,'chsize')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),199)
        self.assertEqual(len(F),2)
        self.assertEqual(code_publics(original,1),[(0,'_chsize')])
        self.assertEqual(externs(original),['__IOERROR','__openfd'])
        self.assertEqual([r.data.hex() for r in parse_omf(original)
                          if r.name=='GRPDEF'],['08ff03ff02'])
        self.assertEqual({f['site']:(f['target_method'],f['target'])
                          for f in F},{138:(2,1),187:(2,2)})
        self.assertEqual(P[1,133],0xcc)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['chsize']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['chsize'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
