"""Heap include boundaries, shared tails, native frames and DOS ownership."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_heap import ALIGNMENT,BUILD_REMAPS,RANGES,HeapProbe,analyze,cached_provider


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for name,start,size,cleanup in RANGES:
        data[start:start+size]=b'\x90'*size
        tail=b'\xeb\x07' if name=='byte' else b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[start+size-len(tail):start+size]=tail
    data[0x2379:0x237d]=b'\x33\xc0\xf9\xcb'
    for a,v in ALIGNMENT.items():data[a]=v
    return data


class HeapBoundaryTests(unittest.TestCase):
    def test_complete_partition_and_shared_return_cleanup(self):
        with self.assertRaisesRegex(ValueError,'complete include'):analyze(fixture()[:0x22b1])
        data=fixture();data[0x21c0:0x21c2]=b'\xeb\x06'
        with self.assertRaisesRegex(ValueError,'shared-tail jump'):analyze(data)
        data=fixture();data[0x22b0]=4
        with self.assertRaisesRegex(ValueError,'final far cleanup'):analyze(data)
        data=fixture();data[0x210a]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_shared_branch_operand_neighbor_and_unreachable_tail(self):
        for dest in (0x22ad,0x21c9):
            data=fixture();data[0x22b2:0x22b5]=b'\xe9'+struct.pack('<h',dest-0x22b5)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x22c4:0x22c6]=b'\x72\xe6';analyze(data)
        data=fixture();data[0x237a]=0xdb
        with self.assertRaisesRegex(ValueError,'unreachable failure tail'):analyze(data)
        data=fixture();data[0x21ad]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_calls_push_cs_indirect_interrupts_and_ports(self):
        data=fixture();data[0x212f:0x2132]=b'\xe8'+struct.pack('<h',0x21c2-0x2132)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far'),(b'\xcd\x21','unknown DOS'),(b'\xcd\x20','unknown DOS'),(b'\xe6\x60','unexpected port')):
            data=fixture();data[0x210a:0x210a+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_scaffold_remaps_stay_inside_main(self):
        source=b'prefix\nth03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'M\'" })\n'+b'\n'.join(b'"'+p.encode()+b'"' for p in BUILD_REMAPS)+b'\nth03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'L\'" })\n"th02/snd_mode.c"\n'
        actual=cached_provider('Tupfile.lua',source);self.assertTrue(actual.endswith(b'"th02/snd_mode.c"\n'))
        self.assertIn(b'"th03/snd_mode_main.asm"',actual)
        with self.assertRaisesRegex(ValueError,'MAIN remap'):
            cached_provider('Tupfile.lua',source.replace(b'"th03/mrs.cpp"',b'"th03/other.cpp"'))


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class HeapRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x22b2,patches=(),s=None):
        __import__('unicorn');data=fixture();observed=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return HeapProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},observed)

    def test_callback_guards_outside_ffi(self):
        __import__('unicorn')
        for code,msg in ((b'\xcd\x20','unknown DOS request/site'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('free',[0x6001])
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):
            self.probe(b'\xb4\x49\xcd\x21',0x2145).run('assign_dos',[1])

    def test_header_whole_span_and_data_ownership(self):
        for code in (b'\xc7\x06\x58\x08\x01\x00',b'\xc7\x06\x5f\x14\x01\x00'):
            with self.assertRaisesRegex(ValueError,'outside owned state/header'):self.probe(code).run('free',[0x6001])
        code=b'\xb8\x00\x60\x8e\xc0\x26\xc7\x06\x05\x00\x01\x00'
        with self.assertRaisesRegex(ValueError,'outside owned state/header'):self.probe(code).run('free',[0x6001])

    def test_shared_tail_and_nested_actual_far_returns(self):
        code=b'\xe9'+struct.pack('<h',0x22af-0x22b5)
        p=self.probe(code);p.run('free',[0x6001]);self.assertEqual(dict(p.native),{'free':1})
        code=b'\x50\x0e\xe8'+struct.pack('<h',0x21c2-0x2132)+b'\xe9'+struct.pack('<h',0x213b-0x2135)
        p=self.probe(code,0x212d);p.run('long',[1,0]);self.assertEqual(dict(p.native),{'long':1,'allocate':1})
        code=b'\xe9'+struct.pack('<h',0x21c2-0x22b5)
        with self.assertRaisesRegex(ValueError,'native far frame'):self.probe(code).run('free',[0x6001])
        code=b'\x83\xc4\x02\xe9'+struct.pack('<h',0x2357-0x22b8)
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(code).run('free',[0x6001])

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe(b'\xe9'+struct.pack('<h',0x2357-0x22b5));p.run('free',[0x6001]);p.uc.mem_write(p.code+0x22b2,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('free',[0x6001],budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):
            self.probe(b'\xea\x10\xff\xff\x1f').run('free',[0x6001])
        with self.assertRaisesRegex(ValueError,'escaped heap bodies/segment alias'):
            self.probe(b'\xea\x70\x21\xff\x1f').run('free',[0x6001])

    def test_unassign_only_permits_es_clobber(self):
        code=b'\xb8\x00\x60\x8e\xc0\xe9'+struct.pack('<h',0x2378-0x2362)
        p=self.probe(code,0x235a);p.run('unassign');self.assertEqual(p.get('ES'),0x6000)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):
            self.probe(b'\xbb\x00\x00\xe9'+struct.pack('<h',0x2357-0x22b8)).run('free',[0x6001])


if __name__=='__main__':unittest.main()
