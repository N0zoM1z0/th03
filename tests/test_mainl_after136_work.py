"""Original Japanese Borland ostream single-character insertion source."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after136_work import PREFIX,WORK
from review_th03_mainl_after136_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalOstreamCharOutput(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ostischr-build.json')).is_file(),
                         '137-source Japanese ostream char native pair unavailable')
    def test_complete_597_byte_stream_char_insertion_and_full_link(self):
        r=review('ostischr')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,137,756))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (597,65165))
        p=r['profiles']['ostischr']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (597,0,0))
        self.assertEqual(p['publics'],[(0,'@ostream@$blsh$qc')])
        self.assertEqual(p['imports'],['@ios@setstate$qi',
            '@ostream@do_opfx$qv','@ostream@do_osfx$qv'])
        self.assertEqual(len(p['relocation_sites_targets']),5)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'ostischr-build.json')).is_file(),
                         'selected original native ostream character OBJ absent')
    def test_three_virtual_far_calls_and_original_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        report=json.loads((ROOT/(PREFIX+'ostischr-build.json')).read_text())
        original=(WORK/'vendor/ostischr.obj').read_bytes()
        c=bytes(payload(original)[1,i] for i in range(597))
        all_instr=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(c,0))
        self.assertEqual([i.address for i in all_instr if
                         i.bytes==bytes.fromhex('ff5f18')],[157,317,484])
        original_fields=literal_fields(original)
        self.assertEqual(len(original_fields),5)
        key=lambda f:(f['segment'],f['site'])
        for roundinfo in report['rounds']:
            made=(ROOT/roundinfo['outputs']['ostischr']['path']).read_bytes()
            self.assertEqual(payload(original),payload(made))
            self.assertEqual(sorted(original_fields,key=key),
                             sorted(literal_fields(made),key=key))
            self.assertNotEqual(original_fields,literal_fields(made))
