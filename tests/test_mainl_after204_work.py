"""Original Japanese Borland ifstream full constructor/destructor family."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_th03_mainl_after204_work import PREFIX, WORK
from review_th03_mainl_after204_work import review
from build_th03_mainl_display_work import payload, literal_fields

class OriginalIfstreamLifecycle(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ifstream-lifecycle-build.json')).is_file(),
                         'native Japanese 209-source original vectors absent')
    def test_five_complete_cpp_methods_and_full_product(self):
        r=review('ifstream-lifecycle')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,209,684))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2984,87885))
        expected={'ifsctr1':(596,'@ifstream@$bctr$qv'),
                  'ifsctr2':(612,'@ifstream@$bctr$qnxcii'),
                  'ifsctr3':(599,'@ifstream@$bctr$qi'),
                  'ifsctr4':(608,'@ifstream@$bctr$qinci'),
                  'ifsdtr':(569,'@ifstream@$bdtr$qv')}
        for name,(size,public) in expected.items():
            p=r['profiles'][name]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,28,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['relocation_sites_targets']),27)
            self.assertEqual(len(p['imports']),7 if name=='ifsdtr' else 11)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'ifstream-lifecycle-build.json')).is_file(),
                         'original native ifstream OMF evidence absent')
    def test_all_ten_adjustors_and_all_135_original_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'ifstream-lifecycle-build.json')).read_text())
        sizes={'ifsctr1':(596,166),'ifsctr2':(612,182),
               'ifsctr3':(599,169),'ifsctr4':(608,178),'ifsdtr':(569,139)}
        key=lambda f:(f['segment'],f['site'])
        for name,(size,cut) in sizes.items():
            original=(WORK/'vendor'/(name+'.obj')).read_bytes()
            p=payload(original)
            self.assertEqual(len([x for x in p if x[0]==1]),size)
            self.assertEqual(len([x for x in p if x[0]==2]),28)
            code=bytes(p[1,i] for i in range(size))
            for cls in (b'ifstream\0',b'fstreambase\0',b'filebuf\0',
                        b'istream\0',b'ios\0',b'streambuf\0'):
                self.assertIn(cls,code,name)
            thunk=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[cut:cut+24],cut))
            self.assertEqual([x.address for x in thunk if x.mnemonic=='ljmp'],
                             [cut+7,cut+19],name)
            self.assertEqual((code[cut+7],code[cut+19]),(0xEA,0xEA))
            ff=literal_fields(original)
            self.assertEqual(len(ff),27)
            self.assertEqual(len([f for f in ff if f['segment']==2]),4)
            if name=='ifsdtr':
                for off in (cut+8,cut+20):
                    f=next(x for x in ff if x['segment']==1 and x['site']==off)
                    self.assertEqual((f['target_method'],f['target'],f['addend']),
                                     (0,1,0))
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(p,payload(made),name)
                actual=literal_fields(made)
                self.assertEqual(sorted(ff,key=key),sorted(actual,key=key),name)
                self.assertNotEqual(ff,actual,name)
