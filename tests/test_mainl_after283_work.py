"""Original C++ memory cast, stream manipulators and DOS/V micro algorithms."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after283_work import PREFIX,WORK
from review_th03_mainl_after283_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalCXXDOSUtils(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'cpp-dos-utility-leaves-build.json')).exists(),
                         '299-source original native vectors missing')
    def test_all_16_complete_original_modules_and_full_japanese_link(self):
        r=review('cpp-dos-utility-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,299,594))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (416,99132))
        expected={'castmptr':182,'ostmanip':27,'istmanip':27,'setdta':18,
           'dosvsist':17,'rotr':17,'rotl':17,'divt':16,'dosvgkid':14,
           'dosvgist':14,'getdta':13,'dosvisck':12,'stbskoff':11,
           'getpsp':11,'dosvison':10,'dosvisof':10}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        self.assertEqual(r['profiles']['castmptr']['publics'],
                         [(0,'@_cast_memptr$qnvt1uiuiui')])
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0))
            self.assertEqual(p['imports'],[])
            self.assertEqual(p['relocation_sites_targets'],[])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'cpp-dos-utility-leaves-build.json')).exists(),
                         'original selected C++/DOS OBJ pairs missing')
    def test_original_empty_relocations_and_far_stack_indirect_calls(self):
        from lib.omf import parse_omf
        r=json.loads((ROOT/(PREFIX+'cpp-dos-utility-leaves-build.json')).read_text())
        self.assertEqual(len(r['names']),16)
        for n in r['names']:
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[],n)
            groups=[z.data.hex() for z in parse_omf(original) if z.name=='GRPDEF']
            for row in r['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made),n)
                self.assertEqual(literal_fields(made),[],n)
                self.assertEqual([z.data.hex() for z in parse_omf(made)
                                  if z.name=='GRPDEF'],groups,n)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
        for n in ('istmanip','ostmanip'):
            p=payload((WORK/'vendor'/(n+'.obj')).read_bytes())
            self.assertEqual(bytes(p[1,i] for i in (12,13,14)),
                             bytes.fromhex('ff5e0a'))
