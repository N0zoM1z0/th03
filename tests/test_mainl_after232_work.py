"""Twenty selected original 16-bit DOS, NEC BIOS and low-level CRT functions."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after232_work import PREFIX,WORK
from review_th03_mainl_after232_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalBIOSDOSCoreLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'bios-dos-core-leaves-build.json')).is_file(),
                         'original Japanese 252-source native vectors absent')
    def test_twenty_complete_original_hardware_and_CRT_members(self):
        r=review('bios-dos-core-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,252,641))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1566,93470))
        expected={'longtoa':166,'pc98clk':165,'intr':164,'cnecsond':151,
                  'dosvsfnt':119,'dosvgfnt':119,'ungetc':114,'pc98pfnt':65,
                  'pc98gfnt':65,'bios_dsk':51,'randblk':44,'poke':42,
                  'bios_key':41,'parsfnm':41,'dosvgenv':38,'strupr':38,
                  'biosequ':37,'peek':36,'getcbrk':35,'country':35}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0),n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
        self.assertEqual(r['profiles']['longtoa']['publics'],
                         [(0,'__LONGTOA'),(130,'__UTOA')])
        self.assertEqual(r['profiles']['ungetc']['publics'],
                         [(0,'__Nungetc'),(3,'_ungetc')])
        self.assertEqual(r['profiles']['pc98clk']['publics'],
                         [(55,'_pc98clock')])
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'bios-dos-core-leaves-build.json')).is_file(),
                         'native original BIOS/DOS OBJ vector pairs absent')
    def test_original_bios_omf_groups_and_far_indirect_calls(self):
        from lib.omf import parse_omf
        receipt=json.loads((ROOT/(PREFIX+'bios-dos-core-leaves-build.json')).read_text())
        self.assertEqual(len(receipt['names']),20)
        for name in receipt['names']:
            original=(WORK/'vendor'/(name+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[],name)
            group=[g.data.hex() for g in parse_omf(original) if g.name=='GRPDEF']
            self.assertEqual(len(group),1)
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][name]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made),name)
                self.assertEqual(literal_fields(made),[],name)
                self.assertEqual([g.data.hex() for g in parse_omf(made)
                                  if g.name=='GRPDEF'],group,name)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][name])
        for name in ('intr','dosvsfnt','dosvgfnt'):
            p=payload((WORK/'vendor'/(name+'.obj')).read_bytes())
            self.assertEqual(bytes(p[1,i] for i in (108,109,110)),
                             bytes.fromhex('ff5efc'),name)
