"""Actual original Japanese Borland C++ ios::sync_with_stdio lifecycle."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_th03_mainl_after168_work import PREFIX,WORK
from review_th03_mainl_after168_work import review
from build_th03_mainl_display_work import payload,literal_fields

class OriginalStandardIOStreamSynchronization(unittest.TestCase):
    @unittest.skipUnless((ROOT/(PREFIX+'stsync-build.json')).is_file(),
                         'source-bound original 169-source stsync pair absent')
    def test_complete_stdiosync_boss_and_native_Japanese_product(self):
        r=review('stsync')
        self.assertEqual((r['original_CRT_members'],r['native_source_members'],
                          r['untouched_vendor_members']),(893,169,724))
        self.assertEqual((r['added_CODE_bytes'],r['source_CRT_CODE_bytes']),
                         (761,72814))
        p=r['profiles']['stsync']
        self.assertEqual((p['CODE_bytes'],p['DATA_bytes'],p['BSS_bytes']),
                         (761,2,0))
        self.assertEqual(p['publics'],[(96,'@ios@sync_with_stdio$qv')])
        self.assertEqual(len(p['imports']),19)
        self.assertEqual(len(p['relocation_sites_targets']),66)
        self.assertTrue(r['complete_original_CODE_DATA_equal'])
        self.assertTrue(r['complete_native_link_EXE_MAP_equal'])
        self.assertEqual((r['native_rounds'],r['original_MZ_relocations']),(2,677))
        self.assertFalse(r['original_literal_FIXUPP_equal'])
        self.assertFalse(r['source_acceptance'])
        self.assertFalse(r['original_cold_rebuilt'])

    @unittest.skipUnless((ROOT/(PREFIX+'stsync-build.json')).is_file(),
                         'complete native stdio sync OBJ pair absent')
    def test_three_original_exception_frames_and_66_native_fixup_frames(self):
        from capstone import Cs,CS_ARCH_X86,CS_MODE_16
        receipt=json.loads((ROOT/(PREFIX+'stsync-build.json')).read_text())
        original=(WORK/'vendor/stsync.obj').read_bytes()
        p=payload(original)
        self.assertEqual(len([k for k in p if k[0]==1]),761)
        self.assertEqual(len([k for k in p if k[0]==2]),2)
        code=bytes(p[1,i] for i in range(761))
        for st in (b'stdiobuf *\0',b'stdiobuf\0',b'streambuf\0'):
            self.assertIn(st,code)
        instr={x.address:x.bytes.hex() for x in
               Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[96:612],96)}
        self.assertEqual(instr[160],'ff5f24')
        f=literal_fields(original)
        self.assertEqual(len(f),66)
        self.assertEqual(sorted(x['site'] for x in f if x['site'] in (0,14,28)),
                         [0,14,28])
        # Original BCC FIXUPP records are not serialized in site order.
        self.assertEqual([x['site'] for x in f if x['site'] in (0,14,28)],
                         [28,14,0])
        key=lambda f:(f['segment'],f['site'])
        for rd in receipt['rounds']:
            candidate=(ROOT/rd['outputs']['stsync']['path']).read_bytes()
            self.assertEqual(p,payload(candidate))
            made=literal_fields(candidate)
            self.assertEqual(sorted(f,key=key),sorted(made,key=key))
            self.assertNotEqual(f,made)
            self.assertFalse(rd['literal_omf_fixupp_equal_by_member']['stsync'])
