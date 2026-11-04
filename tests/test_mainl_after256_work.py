"""Original Borland C++ strstreambase constructors and RTTI native proof."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after256_work import PREFIX,WORK
from review_th03_mainl_after256_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStrstreambaseConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strstreambase-constructors-build.json')).is_file(),
                         '258-source original native vectors missing')
    def test_full_constructors_and_original_Japanese_EXE_MAP(self):
        r=review('strstreambase-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,258,635))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (873,96065))
        for name,size,public in [('srctr1',444,'@strstreambase@$bctr$qncit1'),
                                 ('srctr2',429,'@strstreambase@$bctr$qv')]:
            p=r['profiles'][name]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (size,20,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual(len(p['imports']),9)
            self.assertEqual(len(p['relocation_sites_targets']),18)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'strstreambase-constructors-build.json')).is_file(),
                         'actual selected original strstreambase OMF OBJ absent')
    def test_far_adjustors_RTTI_and_original_36_site_frame_fields(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'strstreambase-constructors-build.json')).read_text())
        for name,cut in [('srctr1',168),('srctr2',153)]:
            obj=(WORK/'vendor'/(name+'.obj')).read_bytes();p=payload(obj)
            size=max(i for seg,i in p if seg==1)+1
            code=bytes(p[1,i] for i in range(size))
            for st in (b'strstreambase\0',b'strstreambuf\0',b'ios\0',b'streambuf\0'):
                self.assertIn(st,code)
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[cut:cut+12],cut))
            self.assertEqual([i.mnemonic for i in ins],['mov','add','ljmp'])
            self.assertEqual(code[cut+7],0xea)
            ff=literal_fields(obj)
            self.assertEqual(len(ff),18)
            self.assertEqual(len([f for f in ff if f['segment']==2]),3)
            by=lambda f:(f['segment'],f['site'])
            for row in receipt['rounds']:
                out=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(obj),payload(out))
                self.assertEqual(sorted(ff,key=by),
                                 sorted(literal_fields(out),key=by))
                self.assertNotEqual(ff,literal_fields(out))
