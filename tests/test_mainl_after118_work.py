"""Selected original Japanese 119-source Borland ostream long integer code."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after118_work import PREFIX,WORK
from review_th03_mainl_after118_work import review
from build_th03_mainl_display_work import payload,literal_fields


class OriginalOstreamLongInteger(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ostint-build.json')).is_file(),
                         'original 119-source ostream native proof unavailable')
    def test_complete_original_long_output_and_full_link(self):
        r=review('ostint')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,119,774))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (884,58160))
        p=r['profiles']['ostint']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (884,54,0))
        self.assertEqual(p['publics'],
                         [(242,'@ostream@$blsh$ql'),(618,'@ostream@$blsh$qul')])
        self.assertEqual(p['imports'],
                         ['@ostream@outstr$qnxct1','F_LUMOD@','F_LUDIV@','F_LXURSH@'])
        self.assertEqual(len(p['relocation_sites_targets']),17)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'ostint-build.json')).is_file(),
                         'raw original ostint OMF vector absent')
    def test_54_bytes_of_symbols_and_original_site_sorted_frames(self):
        raw=json.loads((ROOT/(PREFIX+'ostint-build.json')).read_text())
        original=(WORK/'vendor/ostint.obj').read_bytes()
        f=literal_fields(original)
        self.assertEqual(len(f),17)
        data=payload(original)
        b=bytes(data[2,i] for i in range(54))
        self.assertEqual(b[:32],b'0123456789abcdef0123456789ABCDEF')
        key=lambda z:(z['segment'],z['site'])
        for rd in raw['rounds']:
            made=(ROOT/rd['outputs']['ostint']['path']).read_bytes()
            self.assertEqual(payload(original),payload(made))
            g=literal_fields(made)
            self.assertEqual(sorted(f,key=key),sorted(g,key=key))
            self.assertNotEqual(f,g)
            self.assertFalse(rd['literal_omf_fixupp_equal_by_member']['ostint'])

    def test_topologically_verified_selected_CRT_ancestry(self):
        from build_th03_mainl_after118_work import retained
        base,files,accepted,members,carrier,parent_hash=retained()
        self.assertEqual(len(members),893)
        self.assertEqual(len(carrier),2)
        self.assertEqual(len(carrier[0][0]),118)
        self.assertEqual(carrier[0][0],carrier[1][0])
        self.assertIn('pc98com',carrier[0][0])
