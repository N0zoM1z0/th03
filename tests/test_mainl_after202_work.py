"""Genuine original filebuf 16-bit constructors and their native vtables."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after202_work import PREFIX,WORK
from review_th03_mainl_after202_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalFilebufConstructors(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'filebuf-constructors-build.json')).is_file(),
                         '204-source original filebuf native pair absent')
    def test_both_original_constructors_and_complete_japanese_product(self):
        r=review('filebuf-constructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,204,689))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (719,84901))
        for name,code,public in [('fsbctr1',359,'@filebuf@$bctr$qv'),
                                 ('fsbctr2',360,'@filebuf@$bctr$qi')]:
            p=r['profiles'][name]
            self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                             (code,52,0))
            self.assertEqual(p['publics'],[(0,public)])
            self.assertEqual((len(p['imports']),len(p['relocation_sites_targets'])),
                             (19,23))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'filebuf-constructors-build.json')).is_file(),
                         'selected filebuf OMF proof unavailable')
    def test_typed_vtable_rtti_and_46_original_omf_frames(self):
        rep=json.loads((ROOT/(PREFIX+'filebuf-constructors-build.json')).read_text())
        key=lambda f:(f['segment'],f['site'])
        for n,size in [('fsbctr1',359),('fsbctr2',360)]:
            old=(WORK/'vendor'/(n+'.obj')).read_bytes()
            p=payload(old)
            self.assertEqual(len([k for k in p if k[0]==1]),size)
            self.assertEqual(len([k for k in p if k[0]==2]),52)
            c=bytes(p[1,i] for i in range(size))
            self.assertIn(b'filebuf\0',c)
            self.assertIn(b'streambuf\0',c)
            fields=literal_fields(old)
            self.assertEqual(len(fields),23)
            self.assertEqual(len([f for f in fields if f['segment']==2]),12)
            for row in rep['rounds']:
                candidate=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(candidate))
                actual=literal_fields(candidate)
                self.assertEqual(sorted(fields,key=key),sorted(actual,key=key))
                self.assertNotEqual(fields,actual)
