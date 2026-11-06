"""Original DOS setmode, descriptor bits and exact bounded near-frame gap."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after516_work import PREFIX,WORK,NATIVE,NEAR_FRAME_GAPS,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after516_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='dos-file-descriptor-mode-switch-leaf'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
class OriginalDOSSetmode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not RECEIPT.is_file():raise unittest.SkipTest('original native setmode receipt absent')
        cls.r=review(MODE)
        _,_,_,members,_,_=retained()
        cls.original=original_library_member(members[NATIVE['setmode']['index']])
        cls.receipt=json.loads(RECEIPT.read_text())
    def test_full_original_native_link_twice(self):
        r=self.r
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,724,169))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(83,193815))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    def test_real_openfd_mode_and_only_near_error_frame_exception(self):
        P=payload(self.original);F=literal_fields(self.original)
        self.assertEqual(len(P),83)
        self.assertEqual(code_publics(self.original,1),[(0,'_setmode')])
        self.assertEqual(externs(self.original),['__nfile','__IOERROR','__openfd'])
        self.assertEqual(NEAR_FRAME_GAPS,{'setmode':{77:2}})
        bysite={f['site']:f for f in F}
        self.assertEqual(set(bysite),{13,47,63,77})
        self.assertEqual((bysite[77]['target_method'],bysite[77]['target'],
                          bysite[77]['frame_method'],bysite[77]['frame']),(2,2,5,None))
        for row in self.receipt['rounds']:
            made=(ROOT/row['outputs']['setmode']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            native={f['site']:f for f in literal_fields(made)}
            self.assertEqual(set(native),set(bysite))
            for site,old in bysite.items():
                now=native[site]
                if site==77:
                    self.assertEqual((now['frame_method'],now['frame']),(0,1))
                    for key in set(old)-{'frame_method','frame'}:self.assertEqual(old[key],now[key])
                else:self.assertEqual(old,now)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            mp=(ROOT/row['outputs']['map']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(mp,(WORK/'obj/th03/mainl.map').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
