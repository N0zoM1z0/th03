"""Complete original DOS text-mode read and exact ordered OMF."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after470_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after470_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from lib.pc98 import parse_mz
MODE='dos-text-file-read-crlf-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosRead(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native DOS read receipt missing')
    def test_full_original_scope_and_reproducible_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,678,215))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(207,181620))
        self.assertEqual((r['profiles']['read']['CODE_bytes'],
                          r['profiles']['read']['DATA_bytes']),(207,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original READ OMF absent')
    def test_translated_eof_crlf_and_eight_literal_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['read']['index']]
        self.assertEqual(m.name,'read')
        raw=original_library_member(m)
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),207)
        self.assertEqual(len(F),8)
        self.assertEqual(code_publics(raw,1),[(0,'___read')])
        self.assertEqual(externs(raw),
                         ['__nfile','_lseek','__rtl_read','__read','__IOERROR','__openfd'])
        self.assertEqual([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF'],
                         ['08ff03ff02'])
        self.assertEqual((P[1,110],P[1,111]),(0x26,0xac))
        sites={f['site']:(f['target_method'],f['target']) for f in F}
        self.assertEqual(sites,{13:(2,1),22:(2,5),43:(2,6),66:(2,3),
                                89:(2,6),142:(2,4),179:(2,2),193:(2,6)})
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            obj=(ROOT/row['outputs']['read']['path']).read_bytes()
            self.assertEqual(payload(obj),P)
            self.assertEqual(literal_fields(obj),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['read'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
