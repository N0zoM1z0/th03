"""Original IBM PC console color 16-bit FAR APIs and exact video state."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after490_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after490_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='ibm-conio-six-color-entrypoints'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
KEYS=('segment','site','location_type','width','segment_relative',
      'frame_method','frame','target_method','target','addend')
PUBLICS=[(0,'___ibm_textcolor'),(43,'___ibm_textbackground'),
         (104,'___ibm_textattr'),(129,'___ibm_highvideo'),
         (139,'___ibm_lowvideo'),(149,'___ibm_normvideo')]
class OriginalIBMColor(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'native IBM original color receipt unavailable')
    def test_original_member_and_two_native_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,698,195))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(160,184995))
        self.assertEqual((r['profiles']['cibmcolr']['CODE_bytes'],
                          r['profiles']['cibmcolr']['DATA_bytes']),(160,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original color OMF missing')
    def test_six_far_publics_and_all_eleven_video_offsets(self):
        _,_,_,members,_,_=retained()
        raw=original_library_member(members[NATIVE['cibmcolr']['index']])
        P=payload(raw);F=literal_fields(raw)
        self.assertEqual(len(P),160)
        self.assertEqual(len(F),11)
        self.assertEqual(code_publics(raw,1),PUBLICS)
        self.assertEqual(externs(raw),['__video'])
        self.assertEqual({f['site']:f['addend'] for f in F},
                         {7:13,23:4,37:4,53:13,91:4,96:4,
                          123:4,133:4,143:4,152:6,155:4})
        self.assertTrue(all(f['target_method']==2 and f['target']==1
                            and f['frame_method']==1 and f['frame']==1 for f in F))
        expected=sorted(tuple(f[k] for k in KEYS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['cibmcolr']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in KEYS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
