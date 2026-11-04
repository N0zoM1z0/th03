"""Original Japanese ostrstream default constructor with typed RTTI."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after258_work import PREFIX,WORK
from review_th03_mainl_after258_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalOstrstreamDefaultConstructor(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ostrstream-constructor-build.json')).is_file(),
                         '259-source original Japanese constructor proof absent')
    def test_entire_far_Cplusplus_constructor_and_original_product(self):
        r=review('ostrstream-constructor')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,259,634))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (616,96681))
        p=r['profiles']['osrctr2']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (616,28,0))
        self.assertEqual(p['publics'],[(0,'@ostrstream@$bctr$qv')])
        self.assertEqual(len(p['imports']),11)
        self.assertEqual(len(p['relocation_sites_targets']),27)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'ostrstream-constructor-build.json')).is_file(),
                         'selected native ostrstream OBJ pair absent')
    def test_far_adjustors_and_all_original_27_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'ostrstream-constructor-build.json')).read_text())
        orig=(WORK/'vendor/osrctr2.obj').read_bytes();p=payload(orig)
        self.assertEqual(len([x for x in p if x[0]==1]),616)
        self.assertEqual(len([x for x in p if x[0]==2]),28)
        c=bytes(p[1,i] for i in range(616))
        for st in (b'ostrstream\0',b'ios\0',b'ostream\0',
                   b'strstreambase\0',b'strstreambuf\0',b'streambuf\0'):
            self.assertIn(st,c)
        thunk=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[176:200],176))
        self.assertEqual([x.address for x in thunk if x.mnemonic=='ljmp'],
                         [183,195])
        self.assertEqual((c[183],c[195]),(0xea,0xea))
        ff=literal_fields(orig)
        self.assertEqual(len(ff),27)
        self.assertEqual(len([x for x in ff if x['segment']==2]),4)
        by=lambda f:(f['segment'],f['site'])
        for row in r['rounds']:
            compiled=(ROOT/row['outputs']['osrctr2']['path']).read_bytes()
            self.assertEqual(p,payload(compiled))
            self.assertEqual(sorted(ff,key=by),
                             sorted(literal_fields(compiled),key=by))
            self.assertNotEqual(ff,literal_fields(compiled))
