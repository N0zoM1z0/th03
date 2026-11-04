"""Original PC-98 NEC textmode boss, symbolic jump tables and OMF exception."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after260_work import PREFIX,WORK
from review_th03_mainl_after260_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalNECTextmode(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'nec-textmode-build.json')).exists(),
                         '261-source original native textmode pair unavailable')
    def test_505_code_35_esc_data_and_two_native_product_rounds(self):
        r=review('nec-textmode')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,261,632))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (505,97661))
        p=r['profiles']['cnectxmd']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),(505,35,0))
        self.assertEqual(p['publics'],[(87,'___nec_textmode')])
        self.assertEqual(p['imports'],['__video','__GOTOXY',
             '___nec_get_screen_height','__NEC_VIDEOINTDC'])
        self.assertEqual(len(p['relocation_sites_targets']),51)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'nec-textmode-build.json')).exists(),
                         'actual native OMF vector not retained')
    def test_51_original_relocations_and_one_explicit_near_call_frame_gap(self):
        r=json.loads((ROOT/(PREFIX+'nec-textmode-build.json')).read_text())
        original=(WORK/'vendor/cnectxmd.obj').read_bytes()
        p=payload(original)
        data=bytes(p[2,i] for i in range(35))
        self.assertEqual(data,b'\x1b[?5h\0\x1b[?5l\0\x1b[>3h\0'
                              b'\x1b[>3n\0\x1b[>3l\0\x1b[2J\0')
        original_fields=literal_fields(original)
        self.assertEqual(len(original_fields),51)
        self.assertEqual(len([f for f in original_fields if f['segment']==1
                              and 451<=f['site']<505]),20)
        by=lambda f:(f['segment'],f['site'])
        logical=('segment','site','location_type','width','segment_relative',
                 'target_method','target','addend')
        for rd in r['rounds']:
            compiled=(ROOT/rd['outputs']['cnectxmd']['path']).read_bytes()
            self.assertEqual(p,payload(compiled))
            made=literal_fields(compiled)
            self.assertEqual(sorted([tuple(f[k] for k in logical) for f in original_fields]),
                             sorted([tuple(f[k] for k in logical) for f in made]))
            a,b=sorted(original_fields,key=by),sorted(made,key=by)
            diff=[(x['site'],x['frame_method'],y['frame_method'])
                  for x,y in zip(a,b) if x!=y]
            self.assertEqual(diff,[(18,5,0)])
            self.assertFalse(rd['literal_omf_fixupp_equal_by_member']['cnectxmd'])
