"""Sound ABI/ownership controls and guarded native interrupt state transitions."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_sound import CS,DS,RANGES,ALIGN,SoundProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,start,size,cleanup in RANGES:
        at=CS*16+start;data[at:at+size]=b'\x90'*size
        ret=b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[at+size-len(ret):at+size]=ret
    for at in ALIGN:data[CS*16+at]=0x90
    return data


class SoundBoundaryTests(unittest.TestCase):
    def test_complete_far_cleanup_and_interior_return(self):
        data=fixture();data[CS*16+0x6a5]=4
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(fixture()[:CS*16+0xc4a])
        data=fixture();data[CS*16+0x2c]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_and_neighbor_branch(self):
        for dest in (0x2d,0x49):
            data=fixture();data[CS*16+0x2c:CS*16+0x2f]=b'\xe9'+struct.pack('<h',dest-0x2f)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)

    def test_native_near_call_and_producer_boundaries(self):
        data=fixture();data[CS*16+0xc1c:CS*16+0xc1f]=b'\xe8'+struct.pack('<h',0x372-0xc1f)
        with self.assertRaisesRegex(ValueError,'near call lacks PUSH CS'):analyze(data)
        data=fixture();data[CS*16+0x49]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_unknown_interrupt_port_and_edges(self):
        for code,message in [(b'\xcd\x21','unknown interrupt'),(b'\xe6\x60','unknown port'),
                             (b'\x9a\xff\xff\x00\x00','unknown far'),(b'\xff\xd0','indirect')]:
            data=fixture();data[CS*16+0x2c:CS*16+0x2c+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class SoundRuntimeTests(unittest.TestCase):
    def probe(self,code,scenario=None):
        __import__('unicorn');data=fixture();data[CS*16+0x2c:CS*16+0x2c+len(code)]=code
        return SoundProbe(SimpleNamespace(program_image=data,relocations=[]),scenario or {})

    def test_interrupt_guards_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x18','unknown interrupt'),(b'\xb4\x04\xcd\x60','mode function'),(b'\xcd\x21','unknown interrupt')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('mode')
            self.assertEqual(stderr.getvalue(),'')

    def test_nonowned_memory_write_rejected(self):
        # Select an ES segment outside both DGROUP and the stack.
        with self.assertRaisesRegex(ValueError,'unexpected memory write'):
            self.probe(b'\xb8\x00\x60\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12').run('mode')

    def test_alias_and_far_cleanup_rejected(self):
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):
            self.probe(b'\xea\x10\xff\x7d\x2c').run('mode')
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):
            self.probe(b'\xca\x02\x00').run('mode')

    def test_stale_terminal_cannot_make_budget_return(self):
        p=self.probe(b'\xcb');p.run('mode');p.uc.mem_write(p.code+0x2c,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('mode',budget=20)
        p.run('mode',terminal=False,budget=20)


if __name__=='__main__':unittest.main()
