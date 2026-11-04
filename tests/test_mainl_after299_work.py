"""Original fstreambase and strstreambase far destructors with native RTTI."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after299_work import PREFIX,WORK
from review_th03_mainl_after299_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalBaseDestructorPair(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'base-destructors-build.json')).is_file(),
                         '301-source original Japanese normal link vectors absent')
    def test_both_complete_cpp_destructors_and_full_product(self):
        r=review('base-destructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,301,592))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (784,99916))
        for n,code,public in [('fsdtr',388,'@fstreambase@$bdtr$qv'),
                              ('srdtr',396,'@strstreambase@$bdtr$qv')]:
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (code,20,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['imports']),5)
            self.assertEqual(len(p['relocation_sites_targets']),17)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'base-destructors-build.json')).is_file(),
                         'original native destructor OMF vectors absent')
    def test_real_self_far_adjustor_four_class_names_and_34_original_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'base-destructors-build.json')).read_text())
        for n,size,strings in [('fsdtr',388,(b'fstreambase\0',b'filebuf\0')),
                                ('srdtr',396,(b'strstreambase\0',b'strstreambuf\0'))]:
            old=(WORK/'vendor'/(n+'.obj')).read_bytes()
            p=payload(old)
            self.assertEqual(len([k for k in p if k[0]==1]),size)
            self.assertEqual(len([k for k in p if k[0]==2]),20)
            c=bytes(p[1,i] for i in range(size))
            for string in strings+(b'ios\0',b'streambuf\0'):
                self.assertIn(string,c)
            thunk=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[120:132],120))
            self.assertEqual([i.mnemonic for i in thunk],['mov','add','ljmp'])
            self.assertEqual(c[127],0xEA)
            ff=literal_fields(old)
            self.assertEqual(len(ff),17)
            self.assertEqual(len([f for f in ff if f['segment']==2]),3)
            self.assertEqual([(f['target_method'],f['target'],f['addend'])
                for f in ff if f['segment']==1 and f['site']==128],[(0,1,0)])
            by=lambda f:(f['segment'],f['site'])
            for roundinfo in r['rounds']:
                made=(ROOT/roundinfo['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(made))
                self.assertEqual(sorted(ff,key=by),
                                 sorted(literal_fields(made),key=by))
                self.assertNotEqual(ff,literal_fields(made))
