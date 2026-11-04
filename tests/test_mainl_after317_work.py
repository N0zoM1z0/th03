"""Original NEC delay and five standard multibyte converter functions."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after317_work import PREFIX,WORK
from review_th03_mainl_after317_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalNECDelayAndMultibyte(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'nec-delay-mbyte-build.json')).is_file(),
                         '319-source original Japanese native vectors absent')
    def test_full_nec_delay_and_five_original_multibyte_apis(self):
        r=review('nec-delay-mbyte')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,319,574))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (518,104838))
        nec,mb=r['profiles']['cnecdely'],r['profiles']['mbyte1']
        self.assertEqual((nec['CODE_bytes'],mb['CODE_bytes']),(278,240))
        self.assertEqual(nec['publics'],[(233,'___nec_delay')])
        self.assertEqual(mb['publics'],[(0,'_mblen'),(44,'_mbtowc'),
            (109,'_wctomb'),(152,'_mbstowcs'),(192,'_wcstombs')])
        for p in (nec,mb):
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0))
            self.assertEqual(p['imports'],[])
            self.assertEqual(p['relocation_sites_targets'],[])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'nec-delay-mbyte-build.json')).is_file(),
                         'selected original NEC/multibyte raw OBJ pairs missing')
    def test_natural_code_data_and_original_empty_FIXUPP_inventories(self):
        from lib.omf import parse_omf
        receipt=json.loads((ROOT/(PREFIX+'nec-delay-mbyte-build.json')).read_text())
        for n in receipt['names']:
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[])
            group=[x.data.hex() for x in parse_omf(original) if x.name=='GRPDEF']
            self.assertEqual(group,['08ff03ff02'])
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made))
                self.assertEqual(literal_fields(made),[])
                self.assertEqual([x.data.hex() for x in parse_omf(made)
                                  if x.name=='GRPDEF'],group)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])
        c=payload((WORK/'vendor/cnecdely.obj').read_bytes())
        for offset in (103,108):
            self.assertEqual(bytes(c[1,i] for i in (offset,offset+1)),
                             bytes.fromhex('84c4'))
