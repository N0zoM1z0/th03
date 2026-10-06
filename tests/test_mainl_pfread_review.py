"""Archive reader boundaries, native pointer dispatch and real callback failures."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_pfread import ALIGNMENT,RANGES,ReadProbe,analyze,state_for


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for _,start,size,kind,cleanup in RANGES:
        data[start:start+size]=b'\x90'*size
        ret=(b'\xca'+struct.pack('<H',int(cleanup))) if kind=='retf' else b'\xc3'
        data[start+size-len(ret):start+size]=ret
    for at,value in ALIGNMENT.items():data[at]=value
    return data


class ArchiveReadBoundaryTests(unittest.TestCase):
    def test_truncated_and_wrong_cleanup_or_return(self):
        with self.assertRaisesRegex(ValueError,'complete body/return'):analyze(fixture()[:0x1a3d])
        data=fixture();data[0x19d0]=6
        with self.assertRaisesRegex(ValueError,'complete body/return'):analyze(data)
        data=fixture();data[0x1904]=0xcb
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_branches_and_declared_zero(self):
        for dest in (0x1905,0x1952):
            data=fixture();data[0x1904:0x1907]=b'\xe9'+struct.pack('<h',dest-0x1907)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x19a3]=0x90
        with self.assertRaisesRegex(ValueError,'producer bytes'):analyze(data)

    def test_indirect_slot_opcode_and_unknown_interface(self):
        data=fixture();data[0x18fa:0x18ff]=b'\x26\xff\x16\x04\x00'
        with self.assertRaisesRegex(ValueError,'indirect field'):analyze(data)
        for code,message in [(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far'),(b'\xe8\x00\x00','unknown near')]:
            data=fixture();data[0x18da:0x18da+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_push_cs_ports_and_interrupt_rejected(self):
        code=b'\xe8'+struct.pack('<h',0x472-0x18dd);data=fixture();data[0x18da:0x18dd]=code
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        for code in (b'\xcd\x21',b'\xe6\x60',b'\xe4\x60'):
            data=fixture();data[0x1904:0x1906]=code
            with self.assertRaisesRegex(ValueError,'port/interrupt'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class ArchiveReadRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x18da):
        __import__('unicorn');data=fixture();data[at:at+len(code)]=code
        p=ReadProbe(SimpleNamespace(program_image=data,relocations=[]),{})
        p.uc.mem_write(p.pfile,bytes(state_for({})));return p

    def test_guarded_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x21','unexpected interrupt'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('close',[0x6000])
            self.assertEqual(stderr.getvalue(),'')

    def test_whole_store_span_and_native_field_pointer(self):
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\xc7\x06\x00\x00\x34\x12').run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\x26\xc7\x06\x1e\x00\x34\x12').run('close',[0x6000])
        p=self.probe(b'\x26\xff\x16\x02\x00',0x18fa);p.uc.mem_write(p.pfile+2,b'\x05\x19')
        with self.assertRaisesRegex(ValueError,'pointer destination'):p.run('getc',[0x6000])
        p=self.probe(b'\x26\xff\x16\x02\x00',0x18fa);p.set('ES',0x6001)
        with self.assertRaisesRegex(ValueError,'pointer segment'):p.run('getc',[0x6000])

    def test_native_and_modeled_frame_guards(self):
        code=b'\xe8'+struct.pack('<h',0x1952-0x18dd)
        with self.assertRaisesRegex(ValueError,'native near frame'):self.probe(code).run('close',[0x6000])
        code=b'\x0e\xe8'+struct.pack('<h',0x472-0x18de)
        with self.assertRaisesRegex(ValueError,'modeled far frame'):self.probe(code).run('close',[0x6000])

    def test_stale_completion_far_cleanup_and_segment_aliases(self):
        p=self.probe(b'\xca\x02\x00');p.run('close',[0x6000]);p.uc.mem_write(p.code+0x18da,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('close',[0x6000],budget=10000)
        with self.assertRaisesRegex(ValueError,'cleanup/callee-saved'):self.probe(b'\xca\x04\x00').run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('close',[0x6000])
        with self.assertRaisesRegex(ValueError,'model segment alias'):self.probe(b'\xea\x82\x04\xff\x1f').run('close',[0x6000])


if __name__=='__main__':unittest.main()
