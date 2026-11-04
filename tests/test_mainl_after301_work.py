"""Original native iostream and iostream_withassign complete constructors."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after301_work import PREFIX,WORK
from review_th03_mainl_after301_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalIostreamConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'iostream-constructors-build.json')).is_file(),
                         '304-source original Japanese native vectors unavailable')
    def test_all_original_3_constructors_and_complete_native_product(self):
        r=review('iostream-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,304,589))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1465,101381))
        items={'iostctr1':(478,24,'@iostream@$bctr$qn9streambuf'),
               'iostctr2':(460,23,'@iostream@$bctr$qv'),
               'iostctr3':(527,25,'@iostream_withassign@$bctr$qv')}
        for n,(size,fixup,public) in items.items():
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,28,0),n)
            self.assertEqual(p['publics'],[(0,public)],n)
            self.assertEqual(len(p['relocation_sites_targets']),fixup,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'iostream-constructors-build.json')).is_file(),
                         'genuine original iostream OBJ vector unavailable')
    def test_six_executable_far_adjustors_and_72_native_frame_fixups(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'iostream-constructors-build.json')).read_text())
        cases={'iostctr1':(478,184),'iostctr2':(460,166),'iostctr3':(527,147)}
        by=lambda f:(f['segment'],f['site'])
        for n,(size,cut) in cases.items():
            old=(WORK/'vendor'/(n+'.obj')).read_bytes();p=payload(old)
            self.assertEqual(len([f for f in p if f[0]==1]),size)
            self.assertEqual(len([f for f in p if f[0]==2]),28)
            c=bytes(p[1,i] for i in range(size))
            for label in (b'iostream\0',b'ios\0',b'ostream\0',b'istream\0'):
                self.assertIn(label,c)
            thunk=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[cut:cut+24],cut))
            self.assertEqual([i.address for i in thunk if i.mnemonic=='ljmp'],
                             [cut+7,cut+19])
            self.assertEqual((c[cut+7],c[cut+19]),(0xea,0xea))
            ff=literal_fields(old)
            self.assertEqual(len([f for f in ff if f['segment']==2]),4)
            for row in r['rounds']:
                new=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(new),n)
                self.assertEqual(sorted(ff,key=by),sorted(literal_fields(new),key=by))
                self.assertNotEqual(ff,literal_fields(new))
