"""Natural C++ must preserve whole native modules, inline data and MZ order."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_exception_native import verify,REPORT,DS,NEW_DATA,LAYOUT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private optimizing C++ pair absent')
class ExceptionNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files,cls.graph,_=build.sources()
        cls.target=parse_mz((build.WORK/'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate=parse_mz((build.WORK/'bin/th03/mainl.exe').read_bytes())

    def check(self,target=None,candidate=None):
        return verify(ROOT,build.WORK,target or self.target,candidate or self.candidate,self.graph,self.files)

    def test_complete_three_cpp_providers_and_actual_static_reserve(self):
        p=self.check()
        self.assertEqual((len(p['owners']),sum(o['size'] for o in p['owners']),p['procedures']),(6,2258,16))
        self.assertEqual((p['source_CODE_bytes'],p['source_inline_CS_DATA_bytes'],p['source_initialized_DATA_bytes'],p['source_uninitialized_file_DATA_bytes']),(1563,659,689,6))
        self.assertEqual((p['normal_library_members'],p['untouched_current_library_members'],p['source_CRT_providers_in_selected_library']),(893,871,28))
        self.assertEqual(sum(len(m['native_fields']) for m in p['modules'].values()),122)
        self.assertTrue(p['whole_EXE_MAP_equal']);self.assertTrue(p['static_object_reserve_bytes_from_two_actual_links'])
        self.assertFalse(p['source_initializer_added']);self.assertEqual(p['BSS_file_byte_credit'],0)
        self.assertEqual(p['modules']['xalloc']['ordered_scope_relocations'][:2],[[0,0x543A],[0,0x53BB]])

    def test_equal_corrupt_inline_cleanup_record_is_not_code_or_equality(self):
        image=bytearray(self.target.program_image);image[LAYOUT['xmsg']['base']+203+5]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_uninitialized_static_object_uses_actual_link_bytes(self):
        image=bytearray(self.target.program_image);image[DS*16+NEW_DATA+4]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_reversed_module_MZ_order_is_rejected(self):
        relocs=list(self.target.relocations);positions=[i for i,q in enumerate(relocs) if LAYOUT['xalloc']['base']<=q.linear<LAYOUT['xalloc']['base']+LAYOUT['xalloc']['size']]
        relocs[positions[0]],relocs[positions[1]]=relocs[positions[1]],relocs[positions[0]]
        bad=replace(self.target,relocations=relocs)
        with self.assertRaisesRegex(ValueError,'complete literal ordered MZ vector'):self.check(bad,bad)


if __name__=='__main__':unittest.main()
