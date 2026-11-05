"""Original complete 2522-byte Borland C++ regexp matching compiler member."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after335_work import PREFIX,WORK,NATIVE,retained,original_library_member
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import object_program_records
from lib.pc98 import parse_mz
from lib.omf import parse_omf
from review_th03_mainl_after335_work import review

PUBLICS=[(0,'@makepat$qnxcnucui'),(911,'@matchs$qnxcnxucnnc'),
         (1087,'@patcmp$qnxcnxuct1'),(1761,'@esc$qnnxc')]
TABLE_RELOCS=[*range(550,560,2),*range(574,588,2),
              *range(1694,1702,2),*range(2497,2517,2)]


class OriginalRegexpMatcher(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'regexp-match-boss-build.json')).is_file(),
                         'original native 361-source regexp receipt absent')
    def test_complete_four_api_match_and_japanese_native_image(self):
        r=review('regexp-match-boss')
        p=r['profiles']['match']
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,361,532))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (2522,117677))
        self.assertEqual((p['TEXT_bytes'],p['TEXTC_bytes'],p['CODE_bytes'],
                          p['DATA_bytes'],p['BSS_bytes']),(5,2517,2522,0,0))
        self.assertEqual(p['publics'],PUBLICS)
        self.assertEqual(p['imports'],['__ctype','_toupper','_memset'])
        self.assertEqual(len(p['relocation_sites_targets']),46)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_library_member_program_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))

    @unittest.skipUnless((ROOT/(PREFIX+'regexp-match-boss-build.json')).is_file(),
                         'original/source native OMF and executable pairs absent')
    def test_typed_jump_tables_original_frame_and_single_test_modrm(self):
        _,_,_,members,_,_=retained()
        m=members[NATIVE['match']['index']]
        self.assertEqual(m.name,'match')
        original=original_library_member(m)
        old_fields=literal_fields(original)
        self.assertEqual(len(old_fields),46)
        local={x['site']:x for x in old_fields if x['segment']==4 and
               x['target_method']==0 and x['location_type']==1}
        self.assertEqual(set(TABLE_RELOCS).issubset(set(local)),True)
        for site in TABLE_RELOCS:
            self.assertEqual((local[site]['target'],local[site]['frame_method']),
                             (4,5))
        self.assertEqual(len(TABLE_RELOCS),26)
        # Four explicit CODE-dispatch keys, with no source-opaque jump blob.
        for site,target in ((149,560),(363,540),(1485,1686),(1836,2477)):
            self.assertEqual((local[site]['target'],local[site]['addend']),
                             (4,target))
        group=[x for x in old_fields if x['target_method']==2 and
               x['location_type']==1]
        self.assertEqual(len(group),4)
        self.assertEqual({(x['frame_method'],x['frame'],x['target'],x['addend'])
                          for x in group},{(1,1,1,1)})
        raw=payload(original)
        self.assertEqual(bytes(raw[4,i] for i in (1628,1629)),b'\x85\xc2')
        self.assertEqual([x.data.hex() for x in parse_omf(original)
                          if x.name=='GRPDEF'],['0aff02ff03'])
        receipt=json.loads((ROOT/(PREFIX+'regexp-match-boss-build.json')).read_text())
        for round_data in receipt['rounds']:
            with self.subTest(round=round_data['round']):
                obj=(ROOT/round_data['outputs']['match']['path']).read_bytes()
                self.assertEqual(payload(obj),raw)
                self.assertEqual(sorted(literal_fields(obj),key=lambda x:(x['segment'],x['site'])),
                                 sorted(old_fields,key=lambda x:(x['segment'],x['site'])))
                self.assertNotEqual(literal_fields(obj),old_fields)
                self.assertFalse(round_data['literal_omf_fixupp_equal_by_member']['match'])
                self.assertNotEqual(object_program_records(obj),m.program_records)
                self.assertEqual(bytes(payload(obj)[4,i] for i in (1628,1629)),b'\x85\xc2')
                exe=(ROOT/round_data['outputs']['exe']['path']).read_bytes()
                self.assertEqual(exe,(WORK/'bin/th03/mainl.target.exe').read_bytes())
                self.assertEqual(len(parse_mz(exe).relocations),677)


if __name__=='__main__':
    unittest.main()
