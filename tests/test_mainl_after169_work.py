"""Four original selected C++ fstream constructors and executable adjustors."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after169_work import PREFIX,WORK
from review_th03_mainl_after169_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFourFstreamConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'fstream-constructors-build.json')).is_file(),
                         '173-source original fstream native pair absent')
    def test_four_complete_original_fstream_cpp_constructors_and_product(self):
        r=review('fstream-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,173,720))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (3121,75935))
        expected={'iofsctr1':(772,'@fstream@$bctr$qv'),
                  'iofsctr2':(787,'@fstream@$bctr$qnxcii'),
                  'iofsctr3':(775,'@fstream@$bctr$qi'),
                  'iofsctr4':(787,'@fstream@$bctr$qinci')}
        for n,(count,public) in expected.items():
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (count,36,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual((len(p['imports']),len(p['relocation_sites_targets'])),
                             (13,36))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])

    @unittest.skipUnless((ROOT/(PREFIX+'fstream-constructors-build.json')).is_file(),
                         'original fstream OMF OBJ vectors unavailable')
    def test_typed_rtti_three_real_far_adjustors_and_144_original_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'fstream-constructors-build.json')).read_text())
        sizes=dict(iofsctr1=772,iofsctr2=787,iofsctr3=775,iofsctr4=787)
        ret=dict(iofsctr1=182,iofsctr2=197,iofsctr3=185,iofsctr4=197)
        by=lambda f:(f['segment'],f['site'])
        for n,size in sizes.items():
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            p=payload(original)
            self.assertEqual(len([x for x in p if x[0]==1]),size)
            self.assertEqual(len([x for x in p if x[0]==2]),36)
            c=bytes(p[1,i] for i in range(size))
            for label in (b'fstream\0',b'iostream\0',b'fstreambase\0',
                          b'filebuf\0',b'istream\0',b'ostream\0',b'ios\0'):
                self.assertIn(label,c)
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[ret[n]:ret[n]+36],ret[n]))
            self.assertEqual([x.address for x in ins if x.mnemonic=='ljmp'],
                             [ret[n]+7,ret[n]+19,ret[n]+31])
            f=literal_fields(original)
            self.assertEqual(len(f),36)
            self.assertEqual(len([x for x in f if x['segment']==2]),5)
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(made),n)
                g=literal_fields(made)
                self.assertEqual(sorted(f,key=by),sorted(g,key=by),n)
                self.assertNotEqual(f,g,n)
