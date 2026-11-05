"""Original 48-byte Borland localeconv output ABI with 41 symbolic fields."""
import json,sys,unittest
from pathlib import Path
import setuptools
sys.setrecursionlimit(max(sys.getrecursionlimit(),9000))
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after466_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from review_th03_mainl_after466_work import review
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs
from lib.pc98 import parse_mz
MODE='localeconv-far-string-structure-boss'
RECEIPT=ROOT/(PREFIX+MODE+'-build.json')
FIELDS=('segment','site','location_type','width','segment_relative',
        'frame_method','frame','target_method','target','addend')
class OriginalLocaleConv(unittest.TestCase):
    @unittest.skipUnless(RECEIPT.is_file(),'localeconv scope receipt missing')
    def test_complete_native_source_and_two_original_rounds(self):
        r=review(MODE)
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,674,219))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),(212,180860))
        self.assertEqual((r['profiles']['lconv']['CODE_bytes'],
                          r['profiles']['lconv']['DATA_bytes']),(212,0))
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
    @unittest.skipUnless(RECEIPT.is_file(),'original locale metadata OMF absent')
    def test_ten_far_strings_eight_currency_flags_and_exact_41_fixups(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['lconv']['index']]
        self.assertEqual(m.name,'lconv')
        original=original_library_member(m)
        P=payload(original);F=literal_fields(original)
        self.assertEqual(len(P),212)
        self.assertEqual(len(F),41)
        self.assertEqual(code_publics(original,1),[(0,'__llocaleconv')])
        self.assertEqual(externs(original),['__pLocale','__localeconvention'])
        self.assertEqual({f['target'] for f in F},{1,2})
        sites={f['site']:f for f in F}
        self.assertEqual((sites[4]['target'],sites[4]['addend']),(1,2))
        self.assertEqual((sites[7]['target'],sites[7]['addend']),(1,0))
        self.assertEqual((sites[202]['target'],sites[202]['addend']),(2,47))
        self.assertEqual((sites[207]['target'],sites[207]['addend']),(2,0))
        self.assertTrue(all(f['frame_method']==1 and f['frame']==1 for f in F))
        expected=sorted(tuple(f[k] for k in FIELDS) for f in F)
        receipt=json.loads(RECEIPT.read_text())
        for row in receipt['rounds']:
            made=(ROOT/row['outputs']['lconv']['path']).read_bytes()
            self.assertEqual(payload(made),P)
            self.assertEqual(sorted(tuple(f[k] for k in FIELDS)
                                    for f in literal_fields(made)),expected)
            self.assertNotEqual(literal_fields(made),F)
            exe=(ROOT/row['outputs']['exe']['path']).read_bytes()
            self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
            self.assertEqual(len(parse_mz(exe).relocations),677)
if __name__=='__main__':unittest.main()
