"""Ten complete Japanese Borland DBCS copy/reverse/case algorithms."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after307_work import PREFIX,WORK
from review_th03_mainl_after307_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalJapaneseMultibyteCopyCase(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'jis-copy-case-build.json')).is_file(),
                         'original Japanese 317-source native vectors absent')
    def test_ten_complete_original_multibyte_algorithms_and_link(self):
        r=review('jis-copy-case')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,317,576))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1356,104320))
        sizes={'MBSREV':144,'FMBSREV':144,'MBSNCPY':133,'FMBSNCPY':133,
               'MBSNBCPY':137,'FMBSNBCP':137,'JSTRLWR':132,'JSTRUPR':132,
               'FJSTRLWR':132,'FJSTRUPR':132}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in sizes},sizes)
        for n in sizes:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0))
            self.assertEqual(p['imports'],['__mbctype'])
            self.assertEqual(len(p['relocation_sites_targets']),1)
            self.assertEqual(len(p['publics']),1)
            self.assertEqual(p['publics'][0][0],0)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'jis-copy-case-build.json')).is_file(),
                         'literal selected Japanese DBCS OBJ vectors absent')
    def test_all_ten_literal_original_omf_fields_and_source_bytes(self):
        r=json.loads((ROOT/(PREFIX+'jis-copy-case-build.json')).read_text())
        self.assertEqual(len(r['names']),10)
        for name in r['names']:
            obj=(WORK/'vendor'/(name+'.obj')).read_bytes()
            f=literal_fields(obj)
            self.assertEqual(len(f),1)
            self.assertEqual((f[0]['target_method'],f[0]['target'],
                              f[0]['addend'],f[0]['frame_method']),(2,1,1,1))
            self.assertEqual(f[0]['site'],56 if 'JSTR' in name else
                             34 if name.endswith('REV') else 37)
            for roundinfo in r['rounds']:
                made=(ROOT/roundinfo['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(obj),payload(made),name)
                self.assertEqual(f,literal_fields(made),name)
                self.assertTrue(roundinfo['literal_omf_fixupp_equal_by_member'][name])
