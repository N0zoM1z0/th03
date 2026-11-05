"""Original DOS date/time UTC conversion and literal OMF field chronology."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after467_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after467_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-packed-time-to-utc-dst-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDosTimeToUtc(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'source-bound DOS time receipt missing')
    def test_complete_original_and_two_real_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,675,218))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (214,181074))
        self.assertEqual((r['profiles']['dostimu']['CODE_bytes'],
                          r['profiles']['dostimu']['DATA_bytes']),(214,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original DOS packed-time OMF absent')
    def test_exact_month_table_target_and_near_dst_fixup(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['dostimu']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),214)
        self.assertEqual(len(F),5)
        self.assertEqual(code_publics(raw,1),[(0,'__DOSTIMETOU')])
        self.assertEqual(externs(raw),['__ISDST','__daylight','__timezone','__monthDay'])
        sites={f['site']:f for f in F}
        self.assertEqual(set(sites),{10,13,22,73,184})
        self.assertEqual((sites[73]['target_method'],sites[73]['target'],
                          sites[73]['frame_method'],sites[73]['addend']),(2,4,5,65534))
        self.assertEqual((sites[184]['target_method'],sites[184]['target'],
                          sites[184]['frame_method'],sites[184]['frame']),
                         (2,1,0,1))
        self.assertEqual((P[1,57],P[1,134]),(0xcd,0xc1))
        r=json.loads(RECEIPT.read_text())
        for row in r['rounds']:
            made=(ROOT/row['outputs']['dostimu']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(literal_fields(made),F)
            self.assertTrue(row['literal_omf_fixupp_equal_by_member']['dostimu'])
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
