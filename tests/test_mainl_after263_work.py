"""Twenty selected original Japanese DOS/PC-98 8086 utility leaves."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after263_work import PREFIX,WORK
from review_th03_mainl_after263_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalBIOSDOSShortLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'pc98-dos-small-leaves-build.json')).exists(),
                         '283-source original Japanese selected OBJ vectors unavailable')
    def test_all_twenty_complete_original_members_and_full_japanese_link(self):
        r=review('pc98-dos-small-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,283,610))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (513,98716))
        expected={'movedata':34,'dosext':34,'segread':34,'lrotr':33,
           'lrotl':32,'swab':31,'getswit':31,'getverf':28,'pc98crt':27,
           'biosprin':24,'bios_prn':24,'pc98sfky':21,'pc98mem':21,
           'pc98gfky':21,'dosvgadr':21,'bioscom':20,'bios_com':20,
           'bdos':20,'dosvuscr':19,'cnecwhxy':18}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        for name in expected:
            p=r['profiles'][name]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0))
            self.assertEqual(p['imports'],[])
            self.assertEqual(p['relocation_sites_targets'],[])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'pc98-dos-small-leaves-build.json')).exists(),
                         'original native DOS/PC-98 short OBJ pairs absent')
    def test_exact_original_empty_fixups_and_swab_instruction_encoding(self):
        from lib.omf import parse_omf
        r=json.loads((ROOT/(PREFIX+'pc98-dos-small-leaves-build.json')).read_text())
        self.assertEqual(len(r['names']),20)
        for name in r['names']:
            original=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[])
            origgroup=[z.data.hex() for z in parse_omf(original) if z.name=='GRPDEF']
            for rd in r['rounds']:
                made=(ROOT/rd['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made),name)
                self.assertEqual(literal_fields(made),[],name)
                self.assertEqual([z.data.hex() for z in parse_omf(made)
                                  if z.name=='GRPDEF'],origgroup,name)
                self.assertTrue(rd['literal_omf_fixupp_equal_by_member'][name])
        raw=payload((WORK/'vendor/swab.obj').read_bytes())
        self.assertEqual(bytes(raw[1,i] for i in (21,22)),bytes.fromhex('86e0'))
