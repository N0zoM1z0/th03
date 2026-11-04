"""Selected Japanese Borland multibyte/JIS leaf algorithms: 232-source MAINL."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after214_work import PREFIX, WORK
from review_th03_mainl_after214_work import review
from build_th03_mainl_display_work import payload, literal_fields

class OriginalJapaneseJISMultibyteLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'jis-multibyte-leaves-build.json')).is_file(),
                         '232-source original Japanese native pair absent')
    def test_all_eighteen_native_members_and_linked_Japanese_product(self):
        r=review('jis-multibyte-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,232,661))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (1035,91904))
        expected={'FMBSNBSE':143,'MBSNBSET':143,'FMBSSET':127,'MBSSET':127,
            'MBJMSJIS':64,'MBJISJMS':48,'MBTOHIRA':40,'MBTOKATA':31,
            'JISALPHA':39,'JISUPPER':29,'JISLOWER':29,'JISDIGIT':29,
            'JISSPACE':23,'JTOLOWER':33,'JTOUPPER':33,'MBISSYM':34,
            'MBISKATA':34,'MBISHIRA':29}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},expected)
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0),n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
            self.assertEqual(len(p['publics']),1,n)
            self.assertEqual(p['publics'][0][0],0,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'jis-multibyte-leaves-build.json')).is_file(),
                         'raw original native JIS member pairs absent')
    def test_real_original_CODE_and_empty_OMF_fields_and_group_per_module(self):
        from lib.omf import parse_omf
        receipt=json.loads((ROOT/(PREFIX+'jis-multibyte-leaves-build.json')).read_text())
        self.assertEqual(len(receipt['names']),18)
        for n in receipt['names']:
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[],n)
            original_group=[z.data.hex() for z in parse_omf(original)
                            if z.name=='GRPDEF']
            self.assertEqual(len(original_group),1)
            for roundinfo in receipt['rounds']:
                compiled=(ROOT/roundinfo['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(original),payload(compiled),n)
                self.assertEqual(literal_fields(compiled),[],n)
                self.assertEqual([z.data.hex() for z in parse_omf(compiled)
                                  if z.name=='GRPDEF'],original_group,n)
                self.assertTrue(roundinfo['literal_omf_fixupp_equal_by_member'][n],n)
