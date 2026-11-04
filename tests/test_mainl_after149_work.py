"""Complete original Japanese istream and ostream constructors including RTTI."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after149_work import PREFIX,WORK
from review_th03_mainl_after149_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalIOStreamConstructorBosses(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'constructors-build.json')).is_file(),
                         'original Japanese 151-source constructor receipts absent')
    def test_complete_two_CPP_istream_ostream_owners_and_product(self):
        r=review('constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,151,742))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1898,67906))
        inp,out=r['profiles']['istx'],r['profiles']['ostx']
        self.assertEqual((inp['CODE_bytes'],inp['DATA_bytes'],inp['BSS_bytes']),
                         (971,20,0))
        self.assertEqual((out['CODE_bytes'],out['DATA_bytes'],out['BSS_bytes']),
                         (927,20,0))
        self.assertEqual(inp['publics'],[(36,'@istream@$bctr$qinci'),
                            (329,'@istream@$bctr$qiin7ostream')])
        self.assertEqual(out['publics'],[(36,'@ostream@$bctr$qi'),
                            (306,'@ostream@$bctr$qinc')])
        self.assertEqual((len(inp['imports']),len(out['imports'])),(15,13))
        self.assertEqual((len(inp['relocation_sites_targets']),
                          len(out['relocation_sites_targets'])),(47,44))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'constructors-build.json')).is_file(),
                         'typed original RTTI OBJ vectors absent')
    def test_rtti_and_exception_records_91_fixups_full_target_frame(self):
        r=json.loads((ROOT/(PREFIX+'constructors-build.json')).read_text())
        by=lambda f:(f['segment'],f['site'])
        targets={
          'istx':(971,47,[b'filebuf *\0',b'strstreambuf *\0',b'istream\0',
                             b'streambuf\0',b'ios\0']),
          'ostx':(927,44,[b'filebuf *\0',b'strstreambuf *\0',b'ostream\0',
                             b'streambuf\0',b'ios\0'])}
        for name,(size,count,strings) in targets.items():
            original=(WORK/'vendor'/(name+'.obj')).read_bytes()
            p=payload(original)
            self.assertEqual(len([z for z in p if z[0]==1]),size)
            self.assertEqual(len([z for z in p if z[0]==2]),20)
            code=bytes(p[1,i] for i in range(size))
            for string in strings:self.assertIn(string,code,name)
            ff=literal_fields(original)
            self.assertEqual(len(ff),count)
            self.assertEqual(len([f for f in ff if f['segment']==2]),3)
            for row in r['rounds']:
                made=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(p,payload(made),name)
                gg=literal_fields(made)
                self.assertEqual(sorted(ff,key=by),sorted(gg,key=by),name)
                self.assertNotEqual(ff,gg,name)
                self.assertFalse(row['literal_omf_fixupp_equal_by_member'][name])
