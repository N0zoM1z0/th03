"""Original Japanese Borland C++ ostream::outstr native full source proof."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after129_work import PREFIX,WORK
from review_th03_mainl_after129_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalOstreamOutputString(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'ostoutst-build.json')).is_file(),
                         'original 130-source ostream native vectors absent')
    def test_full_815_byte_output_boss_and_original_exe_map(self):
        r=review('ostoutst')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,130,763))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (815,60837))
        p=r['profiles']['ostoutst']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (815,0,0))
        self.assertEqual(p['publics'],[(0,'@ostream@outstr$qnxct1')])
        self.assertEqual(p['imports'],['@ios@setstate$qi',
            '@streambuf@sputn$qnxci','@ostream@do_opfx$qv',
            '@ostream@do_osfx$qv','_strlen'])
        self.assertEqual(len(p['relocation_sites_targets']),11)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_cold_rebuilt'])
        self.assertFalse(r['source_acceptance'])

    @unittest.skipUnless((ROOT/(PREFIX+'ostoutst-build.json')).is_file(),
                         'original native ostream OMF vectors absent')
    def test_three_original_virtual_far_calls_and_site_sorted_fixups(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        r=json.loads((ROOT/(PREFIX+'ostoutst-build.json')).read_text())
        original=(WORK/'vendor/ostoutst.obj').read_bytes()
        fs=literal_fields(original)
        self.assertEqual(len(fs),11)
        code=bytes(payload(original)[1,i] for i in range(815))
        instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0))
        far_calls=[x.address for x in instructions if x.bytes==bytes.fromhex('ff5f18')]
        self.assertEqual(far_calls,[218,463,708])
        key=lambda f:(f['segment'],f['site'])
        for rd in r['rounds']:
            made=(ROOT/rd['outputs']['ostoutst']['path']).read_bytes()
            self.assertEqual(payload(original),payload(made))
            other=literal_fields(made)
            self.assertEqual(sorted(fs,key=key),sorted(other,key=key))
            self.assertNotEqual(fs,other)
