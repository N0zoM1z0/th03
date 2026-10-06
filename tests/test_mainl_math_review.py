"""Adversarial math ownership/far ABI/fault boundaries; engine state is isolated."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_math import CS,DS,RANGES,MathProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,segment,start,size,cleanup in RANGES:
        at=segment*16+start;data[at:at+size]=b'\x90'*size
        ret=b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[at+size-len(ret):at+size]=ret
    data[CS*16+0x155]=0x90
    return data


class MathBoundaryTests(unittest.TestCase):
    def test_truncation_cleanup_and_interior_return(self):
        data=fixture();data[CS*16+0x153]=10
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(fixture()[:CS*16+0xfc1])
        data=fixture();data[CS*16+0x110]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_and_producer_byte(self):
        for dest in (0x111,0x155):
            data=fixture();data[CS*16+0x110:CS*16+0x113]=b'\xe9'+struct.pack('<h',dest-0x113)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[CS*16+0x155]=0
        with self.assertRaisesRegex(ValueError,'producer byte'):analyze(data)

    def test_unknown_edges_interrupts_ports(self):
        for code,message in [(b'\x9a\x00\x00\x00\x00','unknown call/interface'),(b'\xff\xd0','indirect edge'),
                             (b'\xcd\x00','port/interrupt'),(b'\xe6\x60','port/interrupt')]:
            data=fixture();data[CS*16+0x156:CS*16+0x156+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_library_helper_cleanup_and_external_branch(self):
        data=fixture();data[0x17c7]=2
        with self.assertRaisesRegex(ValueError,'body/far cleanup'):analyze(data)
        data=fixture();data[0x175e:0x1761]=b'\xe9'+struct.pack('<h',0x17c9-0x1761)
        with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class MathRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn');data=fixture();data[CS*16+0x110:CS*16+0x110+len(code)]=code
        p=MathProbe(SimpleNamespace(program_image=data,relocations=[]));p.reset();return p

    def test_guarded_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x00','unexpected interrupt/fault'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('vector')
            self.assertEqual(stderr.getvalue(),'')

    def test_writes_outside_output_ownership_rejected(self):
        with self.assertRaisesRegex(ValueError,'outside owned output'):
            self.probe(b'\xc7\x06\x00\x00\x34\x12').run('vector')

    def test_stale_terminal_and_native_far_frames(self):
        p=self.probe(b'\xca\x0c\x00');p.run('vector');p.uc.mem_write(p.code+0x110,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/divide fault'):p.run('vector')
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(b'\xca\x0a\x00').run('vector')
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\x7d\x2c').run('vector')
        with self.assertRaisesRegex(ValueError,'atan native far frame'):
            self.probe(b'\x9a\x5e\x17\x00\x20').run('vector')

    def test_divide_fault_isolated_from_next_native_case(self):
        __import__('unicorn');data=fixture()
        # Only a real DIV BX at an owned fault site may be reported as INT0.
        data[0x175e:0x1764]=b'\x31\xdb\xe9'+struct.pack('<h',0x1791-0x1763)+b'\x90'
        data[0x1791:0x1793]=b'\xf7\xf3'
        mz=SimpleNamespace(program_image=data,relocations=[]);p=MathProbe(mz);p.reset();p.run('atan',[0,1],fault=True)
        self.assertEqual(p.fault,{'vector':0,'cs':0x2000,'ip':0x1791})
        # A fresh instance avoids Unicorn's retained post-trap exception state.
        q=MathProbe(mz);q.reset();q.run('vector');self.assertTrue(q.stop);self.assertIsNone(q.fault)


if __name__=='__main__':unittest.main()
