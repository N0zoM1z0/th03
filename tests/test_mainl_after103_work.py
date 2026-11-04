"""Scoped source-native PC-98 console counted-output recovery."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after103_work import PREFIX,WORK
from review_th03_mainl_after103_work import review
from build_th03_mainl_display_work import payload,literal_fields

class NativeConsoleCountedOutput(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'cputn-build.json')).is_file(),
                         '104-source native console output vectors absent')
    def test_original_console_output_callback_and_full_link(self):
        r=review('cputn')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,104,789))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (546,45964))
        p=r['profiles']['cputn']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (546,2,4))
        self.assertEqual(p['publics'],[(450,'__CPUTN')])
        self.assertEqual(p['data_publics'],[])
        self.assertEqual(p['bss_publics'],[(0,'___col'),(2,'___row')])
        self.assertEqual(len(p['imports']),15)
        self.assertEqual(len(p['relocation_sites_targets']),76)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']), (2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'cputn-build.json')).is_file(),
                         'original native cputn OMF receipt absent')
    def test_seven_symbolic_case_relocs_and_original_near_frame_gaps(self):
        record=json.loads((ROOT/(PREFIX+'cputn-build.json')).read_text())
        original=(WORK/'vendor/cputn.obj').read_bytes()
        candidate=(ROOT/record['rounds'][0]['outputs']['cputn']['path']).read_bytes()
        self.assertEqual(payload(original),payload(candidate))
        o,c=literal_fields(original),literal_fields(candidate)
        self.assertEqual((len(o),len(c)),(76,76))
        by=lambda f:(f['segment'],f['site'])
        a,b=sorted(o,key=by),sorted(c,key=by)
        noframe=lambda f:tuple((k,v) for k,v in f.items() if k not in ('frame','frame_method'))
        self.assertEqual([noframe(f) for f in a],[noframe(f) for f in b])
        fields=[f for f in a if 436<=f['site']<450]
        self.assertEqual([f['site'] for f in fields],list(range(436,450,2)))
        self.assertEqual([f['addend'] for f in fields],[102,182,206,163,235,235,149])
        self.assertTrue(all(f['target_method']==0 and f['target']==1 for f in fields))
        diff=[(x['site'],x['frame_method'],y['frame_method']) for x,y in zip(a,b)
              if x!=y]
        self.assertEqual(len(diff),18)
        self.assertTrue(all((x,y)==(5,0) for _,x,y in diff))
        self.assertNotEqual(o,c)
