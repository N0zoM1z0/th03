"""Original Japanese Borland 16-bit istrstream/ostrstream destructor source."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after153_work import PREFIX,WORK
from review_th03_mainl_after153_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStrstreamDestructorFamily(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'strstream-destructors-build.json')).is_file(),
                         '155-source native destructor pair not retained')
    def test_two_complete_original_destructors_and_Japanese_product(self):
        r=review('strstream-destructors')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,155,738))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1158,71276))
        a,b=r['profiles']['isrdtr'],r['profiles']['osrdtr']
        self.assertEqual((a['CODE_bytes'],a['DATA_bytes'],a['BSS_bytes']),
                         (579,28,0))
        self.assertEqual((b['CODE_bytes'],b['DATA_bytes'],b['BSS_bytes']),
                         (579,28,0))
        self.assertEqual(a['publics'],[(0,'@istrstream@$bdtr$qv')])
        self.assertEqual(b['publics'],[(0,'@ostrstream@$bdtr$qv')])
        self.assertEqual((len(a['imports']),len(b['imports'])),(7,7))
        self.assertEqual((len(a['relocation_sites_targets']),
                          len(b['relocation_sites_targets'])),(27,27))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])

    @unittest.skipUnless((ROOT/(PREFIX+'strstream-destructors-build.json')).is_file(),
                         'actual original destructor OMF vectors absent')
    def test_rtti_data_and_54_site_target_frame_equal_relocations(self):
        r=json.loads((ROOT/(PREFIX+'strstream-destructors-build.json')).read_text())
        for n,string in [('isrdtr',b'istrstream\0'),('osrdtr',b'ostrstream\0')]:
            orig=(WORK/'vendor'/(n+'.obj')).read_bytes()
            p=payload(orig)
            self.assertEqual(len([v for v in p if v[0]==1]),579)
            self.assertEqual(len([v for v in p if v[0]==2]),28)
            c=bytes(p[1,i] for i in range(579))
            self.assertIn(string,c)
            for other in (b'streambuf\0',b'ios\0',b'strstreambuf\0'):
                self.assertIn(other,c)
            fs=literal_fields(orig)
            self.assertEqual(len(fs),27)
            self.assertEqual(len([v for v in fs if v['segment']==2]),4)
            by=lambda f:(f['segment'],f['site'])
            for rd in r['rounds']:
                made=(ROOT/rd['outputs'][n]['path']).read_bytes()
                self.assertEqual(p,payload(made))
                other=literal_fields(made)
                self.assertEqual(sorted(fs,key=by),sorted(other,key=by))
                self.assertNotEqual(fs,other)
                self.assertFalse(rd['literal_omf_fixupp_equal_by_member'][n])
