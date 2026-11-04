"""Selected original Japanese MAINL Borland 11-function locale library boss."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after97_work import PREFIX, WORK
from review_th03_mainl_after97_work import review
from build_th03_mainl_display_work import literal_fields,payload


class OriginalLocaleLibraryBoss(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'lsetlocl-build.json')).is_file(),
                         '98-source original Japanese native receipt absent')
    def test_original_locale_boss_11_public_functions_complete_link(self):
        result=review('lsetlocl')
        self.assertTrue(result['complete'])
        self.assertEqual((result['original_CRT_members'],result['native_source_members'],
                          result['untouched_vendor_members']),(893,98,795))
        self.assertEqual((result['added_CODE_bytes'],result['source_CRT_CODE_bytes']),
                         (4652,43215))
        p=result['profiles']['lsetlocl']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (4652,59,0))
        self.assertEqual(p['publics'],[
            (0,'__lsetlocale'),(1805,'___open_localelib'),
            (2027,'___open_locale'),(2247,'___find_localecat'),
            (2516,'___set_localestring_locale'),(2698,'___locale_error'),
            (2814,'___read_localecat'),(3441,'___read_localeenv'),
            (3573,'___find_localelib'),(3825,'___delete_locale'),
            (3960,'___dup_locale')])
        self.assertEqual(len(p['imports']),29)
        self.assertEqual(len(p['relocation_sites_targets']),227)
        self.assertTrue(result['complete_original_CODE_DATA_equal'])
        self.assertTrue(result['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((result['native_rounds'],result['original_MZ_relocations']),
                         (2,677))
        self.assertFalse(result['original_literal_FIXUPP_equal'])
        self.assertFalse(result['original_cold_rebuilt'])
        self.assertFalse(result['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'lsetlocl-build.json')).is_file(),
                         '98-source original Japanese member OBJ pair absent')
    def test_22_symbolic_dispatch_fields_and_three_near_frame_gaps(self):
        receipt=json.loads((ROOT/(PREFIX+'lsetlocl-build.json')).read_text())
        original=(WORK/'vendor/lsetlocl.obj').read_bytes()
        made=(ROOT/receipt['rounds'][0]['outputs']['lsetlocl']['path']).read_bytes()
        self.assertEqual(payload(original),payload(made))
        lhs=literal_fields(original)
        rhs=literal_fields(made)
        self.assertEqual((len(lhs),len(rhs)),(227,227))
        by=lambda f:(f['segment'],f['site'])
        a,b=sorted(lhs,key=by),sorted(rhs,key=by)
        nonframe=lambda f:tuple((k,v) for k,v in f.items() if k not in ('frame_method','frame'))
        self.assertEqual([nonframe(f) for f in a],[nonframe(f) for f in b])
        table=[f for f in a if (1775<=f['site']<1805) or (3427<=f['site']<3441)]
        self.assertEqual(len(table),22)
        self.assertEqual([f['site'] for f in table],
                         list(range(1775,1805,2))+list(range(3427,3441,2)))
        self.assertTrue(all(f['target_method']==0 and f['target']==1 for f in table))
        different=[(x['site'],x['frame_method'],y['frame_method']) for x,y
                   in zip(a,b) if (x['frame_method'],x['frame'])!=(y['frame_method'],y['frame'])]
        self.assertEqual(different,[(4231,5,0),(4329,5,0),(4427,5,0)])
        self.assertNotEqual(lhs,rhs)
