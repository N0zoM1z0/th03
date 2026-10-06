"""Adversarial text owner, native far frames and guarded ROM/port boundaries."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_text import CS,DS,RANGES,TextProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,segment,start,size,cleanup in RANGES:
        at=segment*16+start;data[at:at+size]=b'\x90'*size
        ret=b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[at+size-len(ret):at+size]=ret
    return data


class TextBoundaryTests(unittest.TestCase):
    def test_truncation_wrong_cleanup_and_interior_returns(self):
        data=fixture();data[CS*16+0xc1a]=8
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(fixture()[:CS*16+0xc19])
        data=fixture();data[CS*16+0x9b7]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_branch_operand_and_unowned_neighbors(self):
        for dest in (0x9b8,0xc1c):
            data=fixture();data[CS*16+0x9b7:CS*16+0x9ba]=b'\xe9'+struct.pack('<h',dest-0x9ba)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)

    def test_unknown_edges_ports_and_interrupt(self):
        for code,message in [(b'\x9a\x00\x00\x00\x00','unknown call/interface'),(b'\xff\xd0','indirect edge'),
                             (b'\xcd\x21','unknown interrupt'),(b'\xe7\xa1','port encoding')]:
            data=fixture();data[CS*16+0x9b7:CS*16+0x9b7+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_helper_cleanup_and_external_edge(self):
        data=fixture();data[0xc5d]=2
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        data=fixture();data[0xc36:0xc3b]=b'\x9a\x36\x0c\x00\x00'
        with self.assertRaisesRegex(ValueError,'unknown call/interface'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class TextRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn');data=fixture();data[CS*16+0x9b7:CS*16+0x9b7+len(code)]=code
        return TextProbe(SimpleNamespace(program_image=data,relocations=[]),{})

    def test_callback_errors_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x18','unexpected interrupt'),(b'\xe6\x60','unknown output'),
                             (b'\xe7\xa1','unknown output'),(b'\xe4\xa9','unknown input'),
                             (b'\xb0\x10\xe6\xa5','unknown ROM row')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run()
            self.assertEqual(stderr.getvalue(),'')

    def test_dgroup_and_wide_vram_writes_rejected(self):
        for code,message in [(b'\xc7\x06\x00\x00\x34\x12','unexpected memory write'),
                             (b'\xb8\x00\xa8\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12','flat store width')]:
            with self.assertRaisesRegex(ValueError,message):self.probe(code).run()

    def test_converter_frame_and_physical_alias(self):
        for code,message in [(b'\x9a\x4c\x92\x00\x20','converter return frame'),
                             (b'\x9a\x5c\x92\xff\x1f','converter segment alias'),
                             (b'\xea\x10\xff\x7d\x2c','terminal segment alias')]:
            with self.assertRaisesRegex(ValueError,message):self.probe(code).run()

    def test_stale_terminal_and_far_cleanup(self):
        p=self.probe(b'\xca\x0a\x00');p.run();p.uc.mem_write(p.code+0x9b7,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run(budget=20)
        p.run(terminal=False,budget=20)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(b'\xca\x08\x00').run()


if __name__=='__main__':unittest.main()
