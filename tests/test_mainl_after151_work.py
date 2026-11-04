"""Six original Japanese 16-bit istrstream/ostrstream constructors with RTTI."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after151_work import PREFIX,WORK
from review_th03_mainl_after151_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStrstreamConstructorFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strstream-constructors-build.json')).is_file(),
                         '153-source native strstream constructor pair absent')
    def test_all_six_far_constructors_and_original_Japanese_product(self):
        r=review('strstream-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,153,740))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2212,70118))
        ip,op=r['profiles']['isrctr1'],r['profiles']['osrctr1']
        self.assertEqual((ip['CODE_bytes'],ip['DATA_bytes'],ip['BSS_bytes']),
                         (1001,28,0))
        self.assertEqual((op['CODE_bytes'],op['DATA_bytes'],op['BSS_bytes']),
                         (1211,28,0))
        self.assertEqual(ip['publics'],[(0,'@istrstream@$bctr$qnc'),
            (187,'@istrstream@$bctr$qnzc'),(374,'@istrstream@$bctr$qnuc')])
        self.assertEqual(op['publics'],[(0,'@ostrstream@$bctr$qncii'),
            (257,'@ostrstream@$bctr$qnzcii'),(514,'@ostrstream@$bctr$qnucii')])
        self.assertEqual((len(ip['imports']),len(op['imports'])),(11,12))
        self.assertEqual((len(ip['relocation_sites_targets']),
                          len(op['relocation_sites_targets'])),(43,46))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])

    @unittest.skipUnless((ROOT/(PREFIX+'strstream-constructors-build.json')).is_file(),
                         'selected original strstream OBJ vectors unavailable')
    def test_complete_typed_rtti_and_original_89_fixup_frames(self):
        receipt=json.loads((ROOT/(PREFIX+'strstream-constructors-build.json')).read_text())
        cases={
            'isrctr1':(1001,43,[b'istrstream\x00',b'istream\x00',b'ios\x00',
                                  b'strstreambase\x00',b'streambuf\x00']),
            'osrctr1':(1211,46,[b'ostrstream\x00',b'ostream\x00',b'ios\x00',
                                  b'strstreambase\x00',b'streambuf\x00'])}
        key=lambda f:(f['segment'],f['site'])
        for name,(size,fields,strings) in cases.items():
            obj=(WORK/'vendor'/(name+'.obj')).read_bytes()
            p=payload(obj)
            self.assertEqual(len([z for z in p if z[0]==1]),size)
            self.assertEqual(len([z for z in p if z[0]==2]),28)
            code=bytes(p[1,i] for i in range(size))
            for st in strings:self.assertIn(st,code,name)
            f=literal_fields(obj)
            self.assertEqual(len(f),fields)
            self.assertEqual(len([z for z in f if z['segment']==2]),4)
            for rd in receipt['rounds']:
                candidate=(ROOT/rd['outputs'][name]['path']).read_bytes()
                self.assertEqual(p,payload(candidate),name)
                self.assertEqual(sorted(f,key=key),
                                 sorted(literal_fields(candidate),key=key),name)
                self.assertNotEqual(f,literal_fields(candidate),name)
                self.assertFalse(rd['literal_omf_fixupp_equal_by_member'][name])

    @unittest.skipUnless((ROOT/(PREFIX+'strstream-constructors-build.json')).is_file(),
                         'native ostream constructor vectors absent')
    def test_three_virtual_calls_are_genuinely_far(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        p=payload((WORK/'vendor/osrctr1.obj').read_bytes())
        code=bytes(p[1,i] for i in range(1211))
        ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[:771],0))
        self.assertEqual([i.address for i in ins if i.bytes==bytes.fromhex('ff5f1c')],
                         [221,478,735])
