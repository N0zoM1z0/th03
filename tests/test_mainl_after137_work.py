"""Twelve selected complete native Borland C++ streambuf/ios leaf methods."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after137_work import PREFIX,WORK
from review_th03_mainl_after137_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStreambufAndIOSLeaves(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-ios-leaves-build.json')).is_file(),
                         '149-source original Japanese streambuf CRT vectors absent')
    def test_all_twelve_complete_original_methods_and_full_product(self):
        r=review('streambuf-ios-leaves')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,149,744))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (843,66008))
        expected={'stbsetg':107,'stbsetp':80,'stbskpos':39,'stbdnext':48,
                  'stbsync':80,'stbuflow':55,'stsetst':42,'stclear':62,
                  'stflags':81,'stunset':86,'stskip':73,'stinit':90}
        self.assertEqual({n:r['profiles'][n]['CODE_bytes'] for n in expected},
                         expected)
        for n in expected:
            p=r['profiles'][n]
            self.assertEqual((p['DATA_bytes'],p['BSS_bytes']),(0,0),n)
            self.assertEqual(p['relocation_sites_targets'],[],n)
            self.assertEqual(p['imports'],[],n)
            self.assertEqual(len(p['publics']),1,n)
            self.assertEqual(p['publics'][0][0],0,n)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertTrue(r['original_literal_FIXUPP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'streambuf-ios-leaves-build.json')).is_file(),
                         'original OBJ vectors not retained')
    def test_selected_original_12_member_code_and_empty_fixups(self):
        receipt=json.loads((ROOT/(PREFIX+'streambuf-ios-leaves-build.json')).read_text())
        for n in receipt['names']:
            original=(WORK/'vendor'/(n+'.obj')).read_bytes()
            self.assertEqual(literal_fields(original),[],n)
            for row in receipt['rounds']:
                made=(ROOT/row['outputs'][n]['path']).read_bytes()
                self.assertEqual(payload(original),payload(made),n)
                self.assertEqual(literal_fields(made),[],n)
                self.assertTrue(row['literal_omf_fixupp_equal_by_member'][n])

    def test_original_far_virtual_calls_are_not_near(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        for n,location,opcode in [('stbskpos',29,'ff5f1c'),
                                   ('stbdnext',17,'ff5f0c')]:
            raw=(WORK/'vendor'/(n+'.obj')).read_bytes()
            code=payload(raw)
            size=max(i for seg,i in code if seg==1)+1
            instr={x.address:x.bytes.hex() for x in Cs(CS_ARCH_X86,CS_MODE_16)
                   .disasm(bytes(code[1,i] for i in range(size)),0)}
            self.assertEqual(instr[location],opcode)
