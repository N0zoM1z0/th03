"""Five complete original Japanese Borland ofstream lifecycle functions."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after209_work import PREFIX,WORK
from review_th03_mainl_after209_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalOfstreamLifecycle(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ofstream-lifecycle-build.json')).is_file(),
                         '214-source original Japanese native vectors unavailable')
    def test_five_complete_Cplusplus_members_and_original_product(self):
        r=review('ofstream-lifecycle')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,214,679))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2984,90869))
        original={'ofsctr1':(596,'@ofstream@$bctr$qv'),
                  'ofsctr2':(612,'@ofstream@$bctr$qnxcii'),
                  'ofsctr3':(599,'@ofstream@$bctr$qi'),
                  'ofsctr4':(608,'@ofstream@$bctr$qinci'),
                  'ofsdtr':(569,'@ofstream@$bdtr$qv')}
        for n,(size,public) in original.items():
            p=r['profiles'][n]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,28,0),n)
            self.assertEqual(p['publics'],[(0,public)],n)
            self.assertEqual(len(p['imports']),7 if n=='ofsdtr' else 11,n)
            self.assertEqual(len(p['relocation_sites_targets']),27,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'ofstream-lifecycle-build.json')).is_file(),
                         'original ofstream OMF vectors missing')
    def test_ten_far_adjustors_RTTI_and_135_original_FIXUPP_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'ofstream-lifecycle-build.json')).read_text())
        cases={'ofsctr1':(596,166),'ofsctr2':(612,182),
               'ofsctr3':(599,169),'ofsctr4':(608,178),'ofsdtr':(569,139)}
        by=lambda f:(f['segment'],f['site'])
        for n,(size,cut) in cases.items():
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            p=payload(original)
            self.assertEqual(len([v for v in p if v[0]==1]),size)
            self.assertEqual(len([v for v in p if v[0]==2]),28)
            c=bytes(p[1,i] for i in range(size))
            for word in (b'ofstream\0',b'ios\0',b'ostream\0',
                         b'fstreambase\0',b'filebuf\0',b'streambuf\0'):
                self.assertIn(word,c,n)
            thunks=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c[cut:cut+24],cut))
            self.assertEqual([v.address for v in thunks if v.mnemonic=='ljmp'],
                             [cut+7,cut+19],n)
            self.assertEqual((c[cut+7],c[cut+19]),(0xEA,0xEA))
            f=literal_fields(original)
            self.assertEqual(len(f),27)
            self.assertEqual(len([v for v in f if v['segment']==2]),4)
            if n=='ofsdtr':
                for site in (cut+8,cut+20):
                    z=next(v for v in f if v['segment']==1 and v['site']==site)
                    self.assertEqual((z['target_method'],z['target'],z['addend']),
                                     (0,1,0))
            for row in r['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(made),n)
                self.assertEqual(sorted(f,key=by),
                                 sorted(literal_fields(made),key=by),n)
                self.assertNotEqual(f,literal_fields(made),n)
