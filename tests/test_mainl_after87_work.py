"""Original Japanese DOS signal boss and source-only linked CRT integration."""
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after87_work import PREFIX, WORK
from review_th03_mainl_after87_work import review
from build_th03_mainl_display_work import literal_fields,payload

class NativeOriginalSignal(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'signal-build.json')).is_file(),
                         'two original Japanese signal native rounds not retained')
    def test_original_signal_api_whole_crt_and_final_map(self):
        r=review('signal')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,88,805))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (769,36906))
        p=r['profiles']['signal']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (769,38,4))
        self.assertEqual(p['publics'],[(392,'_signal'),(618,'_raise')])
        self.assertEqual(p['imports'],['__exit','__abort','_errno',
                          '_getvect','_setvect','___SignalPtr'])
        self.assertEqual(len(p['relocation_sites_targets']),55)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'signal-build.json')).is_file(),
                         'source-bound original signal object absent')
    def test_materialized_data_and_full_site_sorted_fixup_frames(self):
        import json
        rep=json.loads((ROOT/(PREFIX+'signal-build.json')).read_text())
        original=(WORK/'vendor/signal.obj').read_bytes()
        source=(ROOT/rep['rounds'][0]['outputs']['signal']['path']).read_bytes()
        self.assertEqual(payload(original),payload(source))
        self.assertEqual(len([k for k in payload(original) if k[0]==2]),38)
        o=literal_fields(original);s=literal_fields(source)
        self.assertEqual(len(o),55)
        self.assertEqual(len(s),55)
        key=lambda f:(f['segment'],f['site'])
        self.assertEqual(sorted(o,key=key), sorted(s,key=key))
        self.assertNotEqual(o,s) # original compiler ordering, not frame drift
        self.assertEqual([f['site'] for f in sorted(o,key=key)],
                         [f['site'] for f in sorted(s,key=key)])

class OriginalHeapDiagnostics(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'signal-fheapchk-build.json')).is_file(),
                         '89-source original Japanese heap diagnostic output absent')
    def test_all_ten_original_heap_diagnostics_publics_and_final_link(self):
        r=review('signal-fheapchk')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,89,804))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1434,37571))
        q=r['profiles']['fheapchk']
        self.assertEqual((q['CODE_bytes'],q['DATA_bytes'],q['BSS_bytes']),
                         (665,0,0))
        self.assertEqual(q['publics'],[
            (0,'_farheapcheck'),(0,'_heapcheck'),
            (251,'_farheapchecknode'),(251,'_heapchecknode'),
            (359,'_farheapfillfree'),(359,'_heapfillfree'),
            (449,'_farheapcheckfree'),(449,'_heapcheckfree'),
            (546,'_farheapwalk'),(546,'_heapwalk')])
        self.assertEqual(q['imports'],['__brk','__sbrk',
                         '___first','___last','___rover'])
        self.assertEqual(len(q['relocation_sites_targets']),19)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

        # The new fheapchk (unlike the combined signal mode) has literal
        # original OMF field order and frames, not merely site equivalence.
        import json
        receipt=json.loads((ROOT/(PREFIX+'signal-fheapchk-build.json')).read_text())
        orig=(WORK/'vendor/fheapchk.obj').read_bytes()
        for roundinfo in receipt['rounds']:
            obj=(ROOT/roundinfo['outputs']['fheapchk']['path']).read_bytes()
            self.assertEqual(payload(orig),payload(obj))
            self.assertEqual(literal_fields(orig),literal_fields(obj))
            self.assertTrue(roundinfo['literal_omf_fixupp_equal_by_member']['fheapchk'])
            self.assertFalse(roundinfo['literal_omf_fixupp_equal_by_member']['signal'])
