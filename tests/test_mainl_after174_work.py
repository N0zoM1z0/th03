"""Actual original Japanese C++ strstream constructors and destructor."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after174_work import PREFIX,WORK
from review_th03_mainl_after174_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStrstreamMultipleInheritance(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strstream-family-build.json')).is_file(),
                         '177-source native strstream vectors absent')
    def test_original_strstream_constructors_destructor_and_complete_link(self):
        r=review('strstream-family')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,177,716))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2413,79083))
        expected={'iosrctr1':(795,36,'@strstream@$bctr$qv'),
                  'iosrctr2':(873,37,'@strstream@$bctr$qncii'),
                  'iosrdtr':(745,36,'@strstream@$bdtr$qv')}
        for name,(size,fields,public) in expected.items():
            p=r['profiles'][name]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,36,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['relocation_sites_targets']),fields)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'strstream-family-build.json')).is_file(),
                         'strstream original OMF OBJ evidence absent')
    def test_all_nine_genuine_adjustor_far_jumps_and_original_109_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'strstream-family-build.json')).read_text())
        entries={'iosrctr1':(795,195,36),'iosrctr2':(873,273,37),
                 'iosrdtr':(745,145,36)}
        by=lambda x:(x['segment'],x['site'])
        for name,(size,cut,count) in entries.items():
            orig=(WORK/'vendor'/(name+'.obj')).read_bytes();p=payload(orig)
            self.assertEqual(len([z for z in p if z[0]==1]),size)
            self.assertEqual(len([z for z in p if z[0]==2]),36)
            code=bytes(p[1,i] for i in range(size))
            for string in (b'strstream\0',b'iostream\0',b'streambuf\0',
                           b'istr'[:0]+b'istream\0',b'ostream\0',b'ios\0'):
                self.assertIn(string,code)
            thunks=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[cut:cut+36],cut))
            self.assertEqual([i.address for i in thunks if i.mnemonic=='ljmp'],
                             [cut+7,cut+19,cut+31])
            ff=literal_fields(orig)
            self.assertEqual(len(ff),count)
            self.assertEqual(len([z for z in ff if z['segment']==2]),5)
            if name=='iosrdtr':
                for site in (cut+8,cut+20,cut+32):
                    f=next(f for f in ff if f['segment']==1 and f['site']==site)
                    self.assertEqual((f['target_method'],f['target'],f['addend']),
                                     (0,1,0))
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(p,payload(made),name)
                self.assertEqual(sorted(ff,key=by),
                                 sorted(literal_fields(made),key=by),name)
                self.assertNotEqual(ff,literal_fields(made),name)
