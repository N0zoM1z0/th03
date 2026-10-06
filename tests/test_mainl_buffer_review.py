"""Buffered file ownership, native far frames and DOS callback boundaries."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_buffer import ALIGNMENT,RANGES,BufferProbe,analyze


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for _,start,size,cleanup in RANGES:
        data[start:start+size]=b'\x90'*size
        data[start+size-3:start+size]=b'\xca'+struct.pack('<H',cleanup)
    for at,value in ALIGNMENT.items():data[at]=value
    return data


class BufferBoundaryTests(unittest.TestCase):
    def test_truncation_cleanup_and_near_return(self):
        with self.assertRaisesRegex(ValueError,'complete body/far cleanup'):analyze(fixture()[:0xac7])
        data=fixture();data[0x6ab]=6
        with self.assertRaisesRegex(ValueError,'complete body/far cleanup'):analyze(data)
        data=fixture();data[0x506]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_branch_and_producer(self):
        for dest in (0x48b,0x4c5):
            data=fixture();data[0x48a:0x48d]=b'\xe9'+struct.pack('<h',dest-0x48d)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x6ad]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_unknown_calls_indirect_and_missing_push_cs(self):
        for code,message in [(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far'),
                             (b'\xe8\x00\x00','unknown near'),(b'\xe8'+struct.pack('<h',0x22b2-0x475),'lacks PUSH CS')]:
            data=fixture();data[0x472:0x472+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_only_owned_int21_sites_and_no_ports(self):
        for code,message in [(b'\xcd\x20','unknown DOS'),(b'\xcd\x21','unknown DOS'),(b'\xe6\x60','unexpected port'),(b'\xe4\x60','unexpected port')]:
            data=fixture();data[0x506:0x506+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class BufferRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x472,patches=()):
        __import__('unicorn');data=fixture();data[at:at+len(code)]=code
        for address,raw in patches:data[address:address+len(raw)]=raw
        return BufferProbe(SimpleNamespace(program_image=data,relocations=[]),{})

    def test_guarded_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x20','unknown DOS request/site'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('close',[0x6000])
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):
            self.probe(b'\xb4\x3f\xcd\x21',0x47d).run('close',[0x6000])

    def test_native_write_span_and_dos_read_destination(self):
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\xc7\x06\x00\x00\x34\x12').run('close',[0x6000])
        code=b'\xb8\x00\x60\x8e\xc0\x26\xc7\x06\x07\x00\x34\x12'
        with self.assertRaisesRegex(ValueError,'outside owned state'):self.probe(code).run('close',[0x6000])
        code=b'\xb8\x01\x60\x8e\xd8\xe9'+struct.pack('<h',0x49c-0x492)
        with self.assertRaisesRegex(ValueError,'read destination'):
            self.probe(code,0x48a,[(0x49c,b'\xb4\x3f\xcd\x21')]).run('fill',[0x6000])

    def test_native_and_modeled_far_frames(self):
        code=b'\x0e\xe8'+struct.pack('<h',0xaae-0x476)
        with self.assertRaisesRegex(ValueError,'native far frame'):self.probe(code).run('close',[0x6000])
        code=b'\x0e\xe8'+struct.pack('<h',0x21ae-0x476)
        with self.assertRaisesRegex(ValueError,'modeled far frame'):self.probe(code).run('close',[0x6000])

    def test_stale_terminal_cleanup_and_segment_aliases(self):
        p=self.probe(b'\xca\x02\x00');p.run('close',[0x6000]);p.uc.mem_write(p.code+0x472,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(b'\xca\x04\x00').run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'model segment alias'):self.probe(b'\xea\xbe\x21\xff\x1f').run('close',[0x6000])


if __name__=='__main__':unittest.main()
