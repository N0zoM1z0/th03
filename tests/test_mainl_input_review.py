"""Adversarial input ownership, hardware callback and native far-frame controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_input import CS,DS,RANGES,InputProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,start,size,cleanup in RANGES:
        at=CS*16+start;data[at:at+size]=b'\x90'*size
        ret=b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[at+size-len(ret):at+size]=ret
    return data


class InputBoundaryTests(unittest.TestCase):
    def test_cleanup_truncation_and_interior_return_rejected(self):
        data=fixture();data[CS*16+0xc99]=2
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(fixture()[:CS*16+0xf30])
        data=fixture();data[CS*16+0x388]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_and_unowned_neighbor_branch_rejected(self):
        for dest in (0x389,0x529):
            data=fixture();data[CS*16+0x388:CS*16+0x38b]=b'\xe9'+struct.pack('<h',dest-0x38b)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)

    def test_near_call_requires_push_cs_and_entry(self):
        for code in (b'\xe8'+struct.pack('<h',0x388-0xdc5),b'\x0e\xe8'+struct.pack('<h',0x389-0xdc6)):
            data=fixture();data[CS*16+0xdc2:CS*16+0xdc2+len(code)]=code
            with self.assertRaisesRegex(ValueError,'near call lacks PUSH CS/far entry'):analyze(data)

    def test_unknown_interrupt_port_far_and_indirect_edges_rejected(self):
        for code,message in [(b'\xcd\x18','unknown interrupt'),(b'\xe6\x60','unknown output'),
                             (b'\x9a\xff\xff\x00\x00','unknown far'),(b'\xff\xd0','indirect')]:
            data=fixture();data[CS*16+0x388:CS*16+0x388+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class InputRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn');data=fixture();data[CS*16+0x388:CS*16+0x388+len(code)]=code
        return InputProbe(SimpleNamespace(program_image=data,relocations=[]),{})

    def test_hardware_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x18','unknown interrupt'),(b'\xb4\x04\xcd\x60','unknown interrupt/function'),
                             (b'\xe7\x5f','port/width/value'),(b'\xe4\x5f','unexpected input port')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('sense',{})
            self.assertEqual(stderr.getvalue(),'')

    def test_outside_state_write_rejected(self):
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\xc7\x06\x00\x00\x34\x12').run('sense',{})

    def test_joystick_and_terminal_segment_aliases_rejected(self):
        for code,message in [(b'\x9a\xfa\x2a\xff\x1f','joystick segment alias'),
                             (b'\xea\x10\xff\x7d\x2c','terminal segment alias')]:
            with self.assertRaisesRegex(ValueError,message):self.probe(code).run('sense',{})

    def test_stale_terminal_and_far_cleanup_rejected(self):
        p=self.probe(b'\xcb');p.run('sense',{});p.uc.mem_write(p.code+0x388,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('sense',{},budget=20)
        p.run('sense',{},terminal=False,budget=20)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):
            self.probe(b'\xca\x02\x00').run('sense',{})


if __name__=='__main__':unittest.main()
