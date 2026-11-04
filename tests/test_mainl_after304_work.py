"""Full original iostream and iostream_withassign destructors with RTTI."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after304_work import PREFIX,WORK
from review_th03_mainl_after304_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalIostreamDestructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'iostream-destructors-build.json')).is_file(),
                         '306-source Japanese original product vectors absent')
    def test_both_complete_original_cpp_destructors_and_full_EXE_MAP(self):
        r=review('iostream-destructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,306,587))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (934,102315))
        for n,code,num,public in [('iostdtr1',433,23,'@iostream@$bdtr$qv'),
                                  ('iostdtr2',501,25,'@iostream_withassign@$bdtr$qv')]:
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (code,28,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['relocation_sites_targets']),num)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'iostream-destructors-build.json')).is_file(),
                         'original iostream destructor native OBJ vectors missing')
    def test_four_original_far_self_adjustors_and_48_relocation_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'iostream-destructors-build.json')).read_text())
        for n,size,cut in [('iostdtr1',433,139),('iostdtr2',501,121)]:
            original=(WORK/'vendor'/(n+'.obj')).read_bytes();p=payload(original)
            self.assertEqual(len([x for x in p if x[0]==1]),size)
            self.assertEqual(len([x for x in p if x[0]==2]),28)
            c=bytes(p[1,i] for i in range(size))
            for st in (b'iostream\0',b'ios\0',b'istream\0',b'ostream\0'):
                self.assertIn(st,c)
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[cut:cut+24],cut))
            self.assertEqual([z.address for z in ins if z.mnemonic=='ljmp'],
                             [cut+7,cut+19])
            self.assertEqual((c[cut+7],c[cut+19]),(0xEA,0xEA))
            ff=literal_fields(original)
            self.assertEqual(len([f for f in ff if f['segment']==2]),4)
            for site in (cut+8,cut+20):
                f=next(x for x in ff if x['segment']==1 and x['site']==site)
                self.assertEqual((f['target_method'],f['target'],f['addend']),(0,1,0))
            by=lambda f:(f['segment'],f['site'])
            for roundinfo in r['rounds']:
                made=(ROOT/roundinfo['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(made))
                self.assertEqual(sorted(ff,key=by),
                                 sorted(literal_fields(made),key=by))
                self.assertNotEqual(ff,literal_fields(made))
