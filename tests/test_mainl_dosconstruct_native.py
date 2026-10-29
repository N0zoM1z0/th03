"""Constructor ownership, callee-pop ABI and the concrete empty-environment branch."""
from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_dosconstruct_native import verify,REPORT,LAYOUT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private constructor pair absent')
class DosConstructorsNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files,cls.graph,_=build.sources()
        cls.target=parse_mz((build.WORK/'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate=parse_mz((build.WORK/'bin/th03/mainl.exe').read_bytes())

    def check(self,target=None,candidate=None):
        return verify(ROOT,build.WORK,target or self.target,candidate or self.candidate,self.graph,self.files)

    def test_complete_constructors_and_eleven_source_library_providers(self):
        p=self.check()
        self.assertEqual((len(p['owners']),p['source_CODE_bytes'],p['procedures']),(2,676,2))
        self.assertEqual([o['procedures'][0]['callee_pop_bytes'] for o in p['owners']],[12,12])
        self.assertEqual((p['normal_library_members'],p['untouched_current_library_members'],p['source_CRT_providers_in_selected_library']),(893,888,11))
        for row in p['modules'].values():
            self.assertEqual((len(row['native_fields']),len(row['far_calls'])),(5,5))
            self.assertNotEqual([f['site'] for f in row['native_fields']],[f['site'] for f in row['original_literal_native_fields']])
        self.assertTrue(p['whole_EXE_MAP_equal'])

    def test_equal_corrupted_callee_pop_immediate_cannot_hide_native_body(self):
        image=bytearray(self.target.program_image);base,size,*_=LAYOUT['doscmd'];image[base+size-2]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_far_call_relaxation_does_not_invent_segment_relocation(self):
        extra=replace(self.target.relocations[0],segment=0,offset=LAYOUT['dosenv'][0]+51)
        bad=replace(self.target,relocations=[*self.target.relocations,extra])
        with self.assertRaisesRegex(ValueError,'complete literal ordered MZ vector'):self.check(bad,bad)

    def test_native_empty_environment_branches_keep_terminators_and_return_offset(self):
        # One deterministic successful allocator hook isolates the actual branch
        # and RET12 question; it does not model allocation or DOS correctness.
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE
        from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_IP,UC_X86_REG_AX,UC_X86_REG_DX
        image=self.target.program_image
        self.assertEqual(image[0x3D0E],0xCB)  # actual shared allocator RETF
        for case,expected_size,expected_bytes,return_offset in [('null-vector',17,b'\0\0\xa5',0x10),('null-first',16,b'\0\0\xa5',0x11),('empty-string',16,b'\0\xa5\xa5',0x10)]:
            with self.subTest(case=case):
                u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000);u.mem_write(0,image)
                u.reg_write(UC_X86_REG_CS,0);u.reg_write(UC_X86_REG_DS,0xE3F);u.reg_write(UC_X86_REG_SS,0x7000);u.reg_write(UC_X86_REG_SP,0xFF00)
                u.mem_write(0x50004,b'\xa5'*64);u.mem_write(0x61000,struct.pack('<HH',0,0 if case=='null-first' else 0x6200));u.mem_write(0x62000,b'\0')
                u.mem_write(0x7FF00,struct.pack('<7H',0xF000,0,0x6000,0,0,0,0 if case=='null-vector' else 0x6100))
                allocations=[];returned=[]
                def hook(uc,site,size,data):
                    if site==0x3C88:
                        sp=uc.reg_read(UC_X86_REG_SP);allocations.append(struct.unpack('<H',uc.mem_read(0x70000+sp+4,2))[0])
                        uc.reg_write(UC_X86_REG_AX,4);uc.reg_write(UC_X86_REG_DX,0x5000);uc.reg_write(UC_X86_REG_IP,0x3D0E)
                    elif site==0xF000:returned.append(True);uc.emu_stop()
                u.hook_add(UC_HOOK_CODE,hook);u.emu_start(LAYOUT['dosenv'][0],0x100000,count=10000)
                self.assertEqual(allocations,[expected_size]);self.assertEqual(returned,[True])
                self.assertEqual((u.reg_read(UC_X86_REG_DX),u.reg_read(UC_X86_REG_AX),u.reg_read(UC_X86_REG_SP)),(0x5000,return_offset,0xFF0E))
                self.assertEqual(bytes(u.mem_read(0x60000,4)),struct.pack('<HH',4,0x5000))
                self.assertEqual(bytes(u.mem_read(0x50010,3)),expected_bytes)


if __name__=='__main__':unittest.main()
