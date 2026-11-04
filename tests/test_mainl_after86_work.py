"""Whole original Japanese long-strftime and ordinal 8086 CRT source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after86_work import PREFIX, WORK
from review_th03_mainl_after86_work import review
from build_th03_mainl_display_work import literal_fields


class OriginalLongDateFormatter(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'lstrftim-build.json')).is_file(),
                         'source-bound long-formatting CRT native rounds absent')
    def test_complete_two_function_1831_byte_original_boss(self):
        r=review('lstrftim')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893,87,806))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1831,36137))
        q=r['profiles']['lstrftim']
        self.assertEqual((q['CODE_bytes'],q['DATA_bytes'],q['BSS_bytes']),
                         (1831,23,0))
        self.assertEqual(q['publics'],
                         [(0,'__lstrftime'),(1730,'__getordinal')])
        self.assertEqual(q['imports'],
                         ['__UTOA','__tzname','_strcpy','_strlen','_strncpy','__pLocale'])
        self.assertEqual(len(q['relocation_sites_targets']),128)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'lstrftim-build.json')).is_file(),
                         'original 87-source OBJ vector not retained')
    def test_symbolic_code_table_all_85_relocations_and_single_near_frame_gap(self):
        raw=json.loads((ROOT/(PREFIX+'lstrftim-build.json')).read_text())
        orig=literal_fields((WORK/'vendor/lstrftim.obj').read_bytes())
        new=literal_fields((ROOT/raw['rounds'][0]['outputs']['lstrftim']['path']).read_bytes())
        self.assertEqual((len(orig),len(new)),(128,128))
        key=lambda f:(f['segment'],f['site'])
        original=sorted(orig,key=key)
        candidate=sorted(new,key=key)
        self.assertEqual([(f['segment'],f['site']) for f in original],
                         [(f['segment'],f['site']) for f in candidate])
        dispatch=[f for f in original if f['segment']==1 and
                  1560<=f['site']<1730]
        self.assertEqual(len(dispatch),85)
        self.assertEqual([f['site'] for f in dispatch],list(range(1560,1730,2)))
        self.assertTrue(all(f['target_method']==0 and f['target']==1 for f in dispatch))
        differing=[(a,b) for a,b in zip(original,candidate) if a!=b]
        self.assertEqual(len(differing),1)
        before,after=differing[0]
        self.assertEqual(before['site'],1377)
        self.assertEqual((before['frame_method'],after['frame_method']),(5,0))
        self.assertEqual((before['target_method'],before['target']), (2,1))
        self.assertEqual((after['target_method'],after['target']), (2,1))
