"""PFOPEN complete-body, native helper and callback ownership controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_pfopen import RANGES,PfProbe,analyze


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for _,start,size,kind,cleanup in RANGES:
        data[start:start+size]=b'\x90'*size
        data[start+size-3:start+size]=bytes([0xca if kind=='retf' else 0xc2])+struct.pack('<H',int(cleanup))
    data[0x2c2f]=0x90
    return data


class PfOpenBoundaryTests(unittest.TestCase):
    def test_truncation_cleanup_and_interior_return(self):
        with self.assertRaisesRegex(ValueError,'complete body/cleanup'):analyze(fixture()[:0x2c67])
        data=fixture();data[0x2c2d]=6
        with self.assertRaisesRegex(ValueError,'complete body/cleanup'):analyze(data)
        data=fixture();data[0x2b16]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_and_producer(self):
        for dest in (0x2b17,0x2c2f):
            data=fixture();data[0x2b16:0x2b19]=b'\xe9'+struct.pack('<h',dest-0x2b19)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x2c2f]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_unknown_call_indirect_edge_and_push_cs(self):
        for code,message in [(b'\x9a\x00\x00\x00\x00','unknown far interface'),(b'\xff\xd0','indirect edge'),
                             (b'\xe8\x00\x00','unknown near call'),(b'\xe8'+struct.pack('<h',0x21ae-0x2b19),'lacks PUSH CS')]:
            data=fixture();data[0x2b16:0x2b16+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_compare_near_cleanup_and_port_opcode(self):
        data=fixture();data[0x2c65]=0xca
        with self.assertRaisesRegex(ValueError,'complete body/cleanup'):analyze(data)
        for code in (b'\xcd\x21',b'\xe6\x60',b'\xe4\x60'):
            data=fixture();data[0x2c30:0x2c30+len(code)]=code
            with self.assertRaisesRegex(ValueError,'port/interrupt'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class PfOpenRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn');data=fixture();data[0x2b16:0x2b16+len(code)]=code
        return PfProbe(SimpleNamespace(program_image=data,relocations=[]),{})

    def test_guarded_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x21','unexpected interrupt'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run()
            self.assertEqual(stderr.getvalue(),'')

    def test_write_bounds_include_whole_word_span(self):
        for offset in (0,0x5b1,0x5b3,0x855,0x857):
            with self.assertRaisesRegex(ValueError,'outside owned state'):
                self.probe(b'\xc7\x06'+struct.pack('<H',offset)+b'\x34\x12').run()

    def test_stale_terminal_far_cleanup_and_aliases(self):
        p=self.probe(b'\xca\x08\x00');p.run();p.uc.mem_write(p.code+0x2b16,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run()
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(b'\xca\x06\x00').run()
        # These segment:offset pairs alias the physical terminal/model hook.
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run()
        with self.assertRaisesRegex(ValueError,'model segment alias'):self.probe(b'\xea\xbe\x21\xff\x1f').run()

    def test_model_return_segment_and_native_compare_frame(self):
        # Change the outer return segment then enter a modeled far interface.
        code=b'\x89\xe5\xc7\x46\x02\xff\x1f\xe9'+struct.pack('<h',0x21ae-0x2b20)
        with self.assertRaisesRegex(ValueError,'model return segment'):self.probe(code).run()
        code=b'\xe8'+struct.pack('<h',0x2c30-0x2b19)
        with self.assertRaisesRegex(ValueError,'compare native near frame'):self.probe(code).run()


if __name__=='__main__':unittest.main()
