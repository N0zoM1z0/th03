"""Complete DOS path producers, real startup relocation and DBCS separator ABI."""
from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_path_native import verify,REPORT,DS,PATH_DATA,PATH_INIT,LAYOUT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private path pair absent')
class PathNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files,cls.graph,_=build.sources()
        cls.target=parse_mz((build.WORK/'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate=parse_mz((build.WORK/'bin/th03/mainl.exe').read_bytes())

    def check(self,target=None,candidate=None):
        return verify(ROOT,build.WORK,target or self.target,candidate or self.candidate,self.graph,self.files)

    def test_complete_path_chain_and_fifteen_source_CRT_providers(self):
        p=self.check()
        self.assertEqual((len(p['owners']),p['source_CODE_bytes'],p['source_initialized_DATA_bytes'],p['procedures']),(6,1247,22,9))
        self.assertEqual((p['normal_library_members'],p['untouched_current_library_members'],p['source_CRT_providers_in_selected_library']),(893,884,15))
        self.assertEqual(sum(len(m['native_fields']) for m in p['modules'].values()),31)
        self.assertEqual(sum(len(m['far_calls']) for m in p['modules'].values()),20)
        self.assertEqual(p['modules']['_pathops']['ordered_scope_relocations'],[[0,0x433F]])
        self.assertEqual([q['callee_pop_bytes'] for q in p['owners'][0]['procedures']],[2,8,0])
        self.assertTrue(p['whole_EXE_MAP_equal'])

    def test_equal_corrupted_parent_reduction_cannot_hide_native_body(self):
        image=bytearray(self.target.program_image);image[LAYOUT['fullpath']['base']+0x1E9]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_startup_near_callback_offset_does_not_gain_segment_relocation(self):
        extra=replace(self.target.relocations[0],segment=DS,offset=PATH_INIT+2)
        bad=replace(self.target,relocations=[*self.target.relocations,extra])
        with self.assertRaisesRegex(ValueError,'complete literal ordered MZ vector'):self.check(bad,bad)

    def test_fallback_range_initializer_requires_all_twelve_bytes(self):
        image=bytearray(self.target.program_image);image[DS*16+PATH_DATA+15]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_actual_native_separator_rejects_DBCS_trail_backslash(self):
        # Run only the real near helper and two real DBCS routines. Supply one
        # ordinary DOS-style lead-range table; no DOS/heap/environment model.
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE
        from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_AX
        for path,result in [(b'\x81\\\0',0),(b'A\\\0',1)]:
            with self.subTest(path=path):
                u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000);u.mem_write(0,self.target.program_image)
                u.reg_write(UC_X86_REG_CS,0);u.reg_write(UC_X86_REG_DS,DS);u.reg_write(UC_X86_REG_SS,0x7000);u.reg_write(UC_X86_REG_SP,0xFF00)
                u.mem_write(DS*16+PATH_DATA,struct.pack('<HH',0,0x6200));u.mem_write(0x62000,b'\x81\x9f\0\0');u.mem_write(0x60000,path)
                u.mem_write(0x7FF00,struct.pack('<5H',0xF000,1,0x6000,0,0x6000));returned=[]
                def hook(uc,site,size,data):
                    if site==0xF000:returned.append(True);uc.emu_stop()
                u.hook_add(UC_HOOK_CODE,hook);u.emu_start(LAYOUT['fullpath']['base']+31,0x100000,count=1000)
                self.assertEqual(returned,[True]);self.assertEqual((u.reg_read(UC_X86_REG_AX),u.reg_read(UC_X86_REG_SP)),(result,0xFF0A))


if __name__=='__main__':unittest.main()
