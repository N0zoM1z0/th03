"""Source-bound original Japanese DOS system and scanner Borland CRT links."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after100_work import PREFIX, WORK
from review_th03_mainl_after100_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalSystemAndScanners(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'system-build.json')).is_file(),
                         '101-source system native pair not retained')
    def test_original_DOS_environment_system_and_full_link(self):
        r=review('system')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']), (101,792,45243))
        p=r['profiles']['system']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (385,19,0))
        self.assertEqual(p['publics'],[(0,'_system')])
        self.assertEqual(p['imports'],['_errno','__environ','_free','_getenv',
            '_malloc','__exitbuf','__DOSENV','__getswitchar','__spawn',
            '_strlen','__stpcpy'])
        self.assertEqual(len(p['relocation_sites_targets']),23)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'system-scanners-build.json')).is_file(),
                         'complete 103-source scanner native pair absent')
    def test_original_sscanf_vsscanf_scanf_callback_ABI_and_full_link(self):
        r=review('system-scanners')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,103,790))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (560,45418))
        self.assertEqual((r['profiles']['sscanf']['CODE_bytes'],
                          r['profiles']['scanf']['CODE_bytes']),(136,39))
        self.assertEqual(r['profiles']['sscanf']['publics'],
                         [(57,'_sscanf'),(96,'_vsscanf')])
        self.assertEqual(r['profiles']['sscanf']['imports'],['__scanner'])
        self.assertEqual(r['profiles']['scanf']['imports'],
                         ['__streams','__Nfgetc','__Nungetc','__scanner'])
        self.assertEqual(len(r['profiles']['sscanf']['relocation_sites_targets']),6)
        self.assertEqual(len(r['profiles']['scanf']['relocation_sites_targets']),4)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'system-scanners-build.json')).is_file(),
                         'original scoped OMF vectors not retained')
    def test_all_33_original_fixup_sites_and_five_near_frame_differences(self):
        receipt=json.loads((ROOT/(PREFIX+'system-scanners-build.json')).read_text())
        differences={'system':{274,333},'sscanf':{87,127},'scanf':{30}}
        for name,expected in differences.items():
            original=(WORK/'vendor'/(name+'.obj')).read_bytes()
            source=(ROOT/receipt['rounds'][0]['outputs'][name]['path']).read_bytes()
            self.assertEqual(payload(original),payload(source),name)
            lhs,rhs=literal_fields(original),literal_fields(source)
            key=lambda f:(f['segment'],f['site'])
            a,b=sorted(lhs,key=key),sorted(rhs,key=key)
            noframe=lambda f:tuple((k,v) for k,v in f.items() if k not in ('frame','frame_method'))
            self.assertEqual([noframe(v) for v in a],[noframe(v) for v in b],name)
            found={x['site'] for x,y in zip(a,b) if x!=y}
            self.assertEqual(found,expected,name)
            self.assertTrue(all((x['frame_method'],y['frame_method'])==(5,0)
                                for x,y in zip(a,b) if x!=y),name)
