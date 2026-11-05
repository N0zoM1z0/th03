"""Large original x87 CRT OMF frames: validate before any source acceptance."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from probe_th03_mainl_large_fixups import original_literal_fixups,original_member
from build_th03_mainl_display_work import literal_fields,payload
from lib.borland_library import library_members
from lib.omf import parse_omf

class OriginalLargeX87LocationFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB'
        if not path.exists(): raise unittest.SkipTest('pinned original Borland CL.LIB not installed')
        cls.members=library_members(path.read_bytes())
    def original(self,name):
        return original_member(self.members,name)
    def test_exhaustive_large_frame4_recovery_without_normalization(self):
        for name,total,location,other5,other1 in [
            ('isteldbl',112,85,11,16),
            ('cplx2',860,734,88,38)
        ]:
            with self.subTest(name=name):
                fields=original_literal_fixups(self.original(name))
                self.assertEqual(len(fields),total)
                self.assertEqual(sum(f['frame_method']==4 for f in fields),location)
                self.assertEqual(sum(f['frame_method']==5 for f in fields),other5)
                self.assertEqual(sum(f['frame_method']==1 for f in fields),other1)
                self.assertTrue(all(f['frame'] is None for f in fields if
                                    f['frame_method'] in (4,5)))
    def test_cplx2_real_initdata_pointer_and_installed_code_boundaries(self):
        raw=self.original('cplx2')
        f=original_literal_fixups(raw)
        init=[x for x in f if x['segment']==4]
        self.assertEqual(len(init),1)
        self.assertEqual((init[0]['site'],init[0]['target_method'],
                          init[0]['target'],init[0]['addend']), (2,0,1,5575))
        p=payload(raw)
        self.assertEqual(len([1 for seg,offset in p if seg==1]),5598)
        self.assertEqual(len([1 for seg,offset in p if seg==2]),47)
        self.assertEqual(sorted(set(range(63))-{offset for seg,offset in p if seg==2}),
                         list(range(16)))
        self.assertEqual(len([1 for seg,offset in p if seg==4]),6)
        self.assertEqual([r.name for r in parse_omf(raw)].count('PUBDEF'),22)
    def test_isteldbl_no_fabricated_non_code_frame(self):
        raw=self.original('isteldbl')
        f=original_literal_fixups(raw)
        self.assertTrue(all(x['segment']==1 for x in f))
        self.assertEqual(len([1 for seg,offset in payload(raw) if seg==1]),1947)
        self.assertEqual(len([1 for seg,offset in payload(raw) if seg==2]),14)
        self.assertEqual({x['target'] for x in f if x['frame_method']==4},
                         {9,10,11})
    def test_backward_equality_for_existing_original_small_members(self):
        for name in ('bcd1','cplx1','dostimu','_pathops'):
            with self.subTest(name=name):
                raw=self.original(name)
                self.assertEqual(original_literal_fixups(raw),literal_fields(raw))

if __name__=='__main__':unittest.main()
