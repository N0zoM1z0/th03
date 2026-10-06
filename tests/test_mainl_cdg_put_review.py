"""Adversarial CDG ownership, operand patch and CPU callback controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_cdg_put import CS,DS,RANGES,ALIGNMENTS,PATCHES,CdgProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for name,start,size in RANGES:
        at=CS*16+start;data[at:at+size]=b'\x90'*size
        for p in PATCHES[name]:data[CS*16+p-1:CS*16+p+2]=b'\xb9\x34\x12'
        data[at+size-3:at+size]=b'\xca\x06\x00'
    for at in ALIGNMENTS:data[CS*16+at]=0x90
    return data


class CdgBoundaryTests(unittest.TestCase):
    def test_cleanup_truncation_and_even_byte_rejected(self):
        data=fixture();data[CS*16+0x2a5]=4
        with self.assertRaisesRegex(ValueError,'body/cleanup'):analyze(data)
        with self.assertRaisesRegex(ValueError,'body/cleanup'):analyze(fixture()[:CS*16+0xfa2])
        data=fixture();data[CS*16+0x371]=0
        with self.assertRaisesRegex(ValueError,'EVEN byte'):analyze(data)

    def test_patch_requires_complete_mov_immediate(self):
        data=fixture();at=CS*16+0x256;data[at:at+3]=b'\x90'*3
        with self.assertRaisesRegex(ValueError,'patch not complete MOV'):analyze(data)

    def test_branch_operand_and_neighbor_rejected(self):
        for dest in (0x1f5,0x2a8):
            data=fixture();data[CS*16+0x1f4:CS*16+0x1f7]=b'\xe9'+struct.pack('<h',dest-0x1f7)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)

    def test_unknown_call_and_indirect_edge_rejected(self):
        for code,message in [(b'\x9a\xff\xff\x00\x00','unknown call/interface'),(b'\xe8\x01\x00','unknown call/interface'),(b'\xff\xd0','indirect')]:
            data=fixture();data[CS*16+0x1f4:CS*16+0x1f4+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class CdgRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn')
        data=fixture();data[CS*16+0x1f4:CS*16+0x1f4+len(code)]=code
        return CdgProbe(SimpleNamespace(program_image=data,relocations=[]))

    def test_callbacks_and_outside_data_write_rejected(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x18','interrupt'),(b'\xba\x7c\x00\xef','port/width'),(b'\xba\x6a\x00\xec','input port'),(b'\xc7\x06\x00\x00\x34\x12','data write')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('alpha',0,0,0)
            self.assertEqual(stderr.getvalue(),'')

    def test_color_and_terminal_aliases_rejected(self):
        code=b'\x68\xc0\x00\x6a\x00\x9a\x46\x0c\xff\x1f'
        with self.assertRaisesRegex(ValueError,'color interface segment alias'):self.probe(code).run('alpha',0,0,0)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\x7d\x2c').run('alpha',0,0,0)

    def test_stale_terminal_and_far_cleanup_rejected(self):
        p=self.probe(b'\xca\x06\x00');p.run('alpha',0,0,0);p.uc.mem_write(p.code+0x1f4,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('alpha',0,0,0,budget=20)
        p.run('alpha',0,0,0,budget=20,terminal=False)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(b'\xcb').run('alpha',0,0,0)


if __name__=='__main__':unittest.main()
