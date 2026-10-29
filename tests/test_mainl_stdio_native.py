"""Complete stream/write bank,callback relocation and the actual LF chunk boundary."""
from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_stdio_native import verify,REPORT,DS,BUFFER_DATA,SETUP_INIT,LAYOUT


@unittest.skipUnless((ROOT/REPORT).is_file(),'private buffered I/O pair absent')
class StdioNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files,cls.graph,_=build.sources()
        cls.target=parse_mz((build.WORK/'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate=parse_mz((build.WORK/'bin/th03/mainl.exe').read_bytes())

    def check(self,target=None,candidate=None):
        return verify(ROOT,build.WORK,target or self.target,candidate or self.candidate,self.graph,self.files)

    def test_complete_bank_and_twenty_five_source_CRT_providers(self):
        p=self.check()
        self.assertEqual((len(p['owners']),p['source_CODE_bytes'],p['source_initialized_DATA_bytes'],p['procedures']),(12,1808,10,13))
        self.assertEqual((p['normal_library_members'],p['untouched_current_library_members'],p['source_CRT_providers_in_selected_library']),(893,874,25))
        self.assertEqual(sum(len(m['native_fields']) for m in p['modules'].values()),58)
        self.assertEqual(sum(len(m['far_calls']) for m in p['modules'].values()),20)
        self.assertEqual(sum(len(m['near_calls']) for m in p['modules'].values()),3)
        self.assertEqual(p['equivalent_near_IOERROR_frame_sites'],[dict(module='write',site=23)])
        self.assertEqual(p['modules']['setvbuf']['ordered_scope_relocations'],[[0,0x4EA7]])
        self.assertTrue(p['whole_EXE_MAP_equal'])

    def test_equal_corrupted_text_position_helper_cannot_hide_native_body(self):
        image=bytearray(self.target.program_image);image[LAYOUT['fseek']['base']+0x56]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_near_startup_callback_does_not_gain_segment_relocation(self):
        extra=replace(self.target.relocations[0],segment=DS,offset=SETUP_INIT+2)
        bad=replace(self.target,relocations=[*self.target.relocations,extra])
        with self.assertRaisesRegex(ValueError,'complete literal ordered MZ vector'):self.check(bad,bad)

    def test_private_stream_flags_require_both_initialized_words(self):
        image=bytearray(self.target.program_image);image[DS*16+BUFFER_DATA+3]^=1
        bad=replace(self.target,program_image=bytes(image))
        with self.assertRaisesRegex(ValueError,'independently resolved native/target/candidate bytes'):self.check(bad,bad)

    def test_actual_native_LF_can_cross_the_128_byte_flush_threshold(self):
        # Real translated writer calls real raw DOS writer. Only successful
        # DOS AH40h is hooked to capture its buffer; no heap or FILE emulator.
        from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
        from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_AX,UC_X86_REG_BX,UC_X86_REG_CX,UC_X86_REG_DX,UC_X86_REG_EFLAGS
        u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000);u.mem_write(0,self.target.program_image)
        u.reg_write(UC_X86_REG_CS,0);u.reg_write(UC_X86_REG_DS,DS);u.reg_write(UC_X86_REG_SS,0x7000);u.reg_write(UC_X86_REG_SP,0xFF00)
        u.mem_write(DS*16+0xE66+5*2,struct.pack('<H',0x4200));u.mem_write(0x60000,b'A'*127+b'\n')
        u.mem_write(0x7FF00,struct.pack('<6H',0xF000,0,5,0,0x6000,128));writes=[];returned=[]
        def dos(uc,number,data):
            self.assertEqual((number,uc.reg_read(UC_X86_REG_AX)>>8,uc.reg_read(UC_X86_REG_BX)),(0x21,0x40,5))
            count=uc.reg_read(UC_X86_REG_CX);pointer=uc.reg_read(UC_X86_REG_DS)*16+uc.reg_read(UC_X86_REG_DX)
            writes.append(bytes(uc.mem_read(pointer,count)));uc.reg_write(UC_X86_REG_AX,count);uc.reg_write(UC_X86_REG_EFLAGS,uc.reg_read(UC_X86_REG_EFLAGS)&~1)
        def stop(uc,site,size,data):
            if site==0xF000:returned.append(True);uc.emu_stop()
        u.hook_add(UC_HOOK_INTR,dos);u.hook_add(UC_HOOK_CODE,stop);u.emu_start(LAYOUT['write']['base'],0x100000,count=20000)
        self.assertEqual(returned,[True]);self.assertEqual(writes,[b'A'*127+b'\r\n'])
        self.assertEqual((u.reg_read(UC_X86_REG_AX),u.reg_read(UC_X86_REG_DS),u.reg_read(UC_X86_REG_SP)),(128,DS,0xFF04))
        self.assertEqual(struct.unpack('<H',u.mem_read(DS*16+0xE66+5*2,2))[0],0x5000)


if __name__=='__main__':unittest.main()
