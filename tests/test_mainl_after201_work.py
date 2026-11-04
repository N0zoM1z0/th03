"""Complete original Borland 16-bit istrstream constructor overloads (CRT 747)."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after201_work import PREFIX,WORK
from review_th03_mainl_after201_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalIstrstreamLengthConstructorBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'istrstream-more-constructors-build.json')).is_file(),
                         'source-bound Japanese 202-source native vectors absent')
    def test_complete_three_original_far_constructors_and_full_product(self):
        r=review('istrstream-more-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,202,691))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1016,84182))
        p=r['profiles']['isrctr2']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (1016,28,0))
        self.assertEqual(p['publics'],[(0,'@istrstream@$bctr$qnci'),
            (192,'@istrstream@$bctr$qnzci'),(384,'@istrstream@$bctr$qnuci')])
        self.assertEqual((len(p['imports']),len(p['relocation_sites_targets'])),
                         (11,43))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'istrstream-more-constructors-build.json')).is_file(),
                         'original selected isrctr2 OBJ proof unavailable')
    def test_original_class_rtti_exception_data_and_43_fixup_frames(self):
        receipt=json.loads((ROOT/(PREFIX+'istrstream-more-constructors-build.json')).read_text())
        original=(WORK/'vendor/isrctr2.obj').read_bytes()
        p=payload(original)
        self.assertEqual(len([k for k in p if k[0]==1]),1016)
        self.assertEqual(len([k for k in p if k[0]==2]),28)
        c=bytes(p[1,i] for i in range(1016))
        for name in (b'istrstream\0',b'strstreambase\0',b'strstreambuf\0',
                     b'streambuf\0',b'ios\0',b'istream\0'):
            self.assertIn(name,c)
        ff=literal_fields(original)
        self.assertEqual(len(ff),43)
        self.assertEqual(len([x for x in ff if x['segment']==2]),4)
        by=lambda x:(x['segment'],x['site'])
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['isrctr2']['path']).read_bytes()
            self.assertEqual(p,payload(made))
            self.assertEqual(sorted(ff,key=by),sorted(literal_fields(made),key=by))
            self.assertNotEqual(ff,literal_fields(made))
