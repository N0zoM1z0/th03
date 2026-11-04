"""Scoped source-only Japanese MAINL Borland CRT recovery after 77 owners."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_th03_mainl_after77_work import PREFIX
from review_th03_mainl_after77_work import review

class OriginalAfter77CRT(unittest.TestCase):
    @unittest.skipUnless((ROOT / (PREFIX + 'strings-build.json')).is_file(),
                         'source-bound 82-source native result absent')
    def test_five_whole_original_far_string_members_and_full_link(self):
        r = review('strings')
        self.assertTrue(r['complete'])
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']), (893, 82, 811))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (284, 34058))
        expected = {'stricmp':65, 'strnicmp':68, 'strncmp':56,
                    'strcoll':29, 'strxfrm':66}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected}, expected)
        self.assertEqual({n:r['profiles'][n]['relocation_sites_targets'] for n in
                          ['stricmp','strnicmp','strncmp']},
                         {'stricmp':[], 'strnicmp':[], 'strncmp':[]})
        self.assertEqual(r['profiles']['strcoll']['imports'], ['_strcmp'])
        self.assertEqual(r['profiles']['strxfrm']['imports'], ['_memcpy','_strlen'])
        self.assertEqual(len(r['profiles']['strxfrm']['relocation_sites_targets']),2)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'], r['original_MZ_relocations']), (2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT / (PREFIX + 'strings-ctype-build.json')).is_file(),
                         'original 84-source ctype CRT rounds absent')
    def test_ctype_toupper_and_atol_atoi_full_84_source_link(self):
        r=review('strings-ctype')
        self.assertEqual((r['native_source_members'],r['untouched_vendor_members'],
                          r['source_CRT_CODE_bytes']),(84,809,34244))
        self.assertEqual(r['profiles']['toupper']['CODE_bytes'],48)
        self.assertEqual(r['profiles']['atol']['CODE_bytes'],138)
        self.assertEqual(r['profiles']['atol']['publics'],
                         [(0,'_atol'),(117,'_atoi')])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])

    @unittest.skipUnless((ROOT / (PREFIX + 'strings-ctype-math-build.json')).is_file(),
                         'original 86-source math/ctype CRT rounds absent')
    def test_abs_labs_and_all_five_numeric_publics_with_original_link(self):
        r=review('strings-ctype-math')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,86,807))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (532,34306))
        self.assertEqual((r['profiles']['abs']['CODE_bytes'],
                          r['profiles']['labs']['CODE_bytes']),(18,44))
        self.assertEqual(r['profiles']['abs']['publics'],[(0,'_abs')])
        self.assertEqual(r['profiles']['labs']['publics'],[(0,'_labs')])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        # The new numeric units match literal ordered fields (including the
        # original external ctype frames); strxfrm is a distinct older gap.
        from build_th03_mainl_after77_work import WORK
        from build_th03_mainl_display_work import literal_fields
        import json
        receipt=json.loads((ROOT/(PREFIX+'strings-ctype-math-build.json')).read_text())
        for name in ['toupper','atol','abs','labs']:
            source=(ROOT/receipt['rounds'][0]['outputs'][name]['path']).read_bytes()
            target=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(literal_fields(source),literal_fields(target),name)

    @unittest.skipUnless((ROOT / (PREFIX + 'strings-ctype-math-build.json')).is_file(),
                         'original 86-source scoped source-pair absent')
    def test_original_omf_field_order_exceptions_are_reported(self):
        # Check literal original OMF fields rather than silently canonicalizing
        # each record's order or equating CODE identity with OBJ identity.
        from build_th03_mainl_display_work import literal_fields
        from build_th03_mainl_after77_work import WORK
        r=review('strings-ctype-math')
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        names=('stricmp','strnicmp','strncmp','strcoll','strxfrm',
               'toupper','atol','abs','labs')
        for n in names:
            original=literal_fields((WORK/'vendor'/(n+'.obj')).read_bytes())
            native=literal_fields((ROOT/'.analysis/work'/
                ('after77-strings-ctype-math-round1-'+n+'.obj')).read_bytes())
            by=lambda f:(f['segment'],f['site'])
            self.assertEqual(sorted(original,key=by), sorted(native,key=by), n)
            self.assertEqual(original==native, n!='strxfrm', n)
