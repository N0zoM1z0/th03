"""Complete file graph, native stack frames, DOS boundaries and memory ownership."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_file import ALIGNMENT,RANGES,FileProbe,analyze


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for _,start,size,cleanup in RANGES:
        data[start:start+size]=b'\x90'*size
        tail=b'\xca'+struct.pack('<H',cleanup) if cleanup else b'\xcb'
        data[start+size-len(tail):start+size]=tail
    for at,value in ALIGNMENT.items():data[at]=value
    return data


class FileBoundaryTests(unittest.TestCase):
    def test_truncation_and_cleanup(self):
        with self.assertRaisesRegex(ValueError,'complete body/cleanup'):analyze(fixture()[:0xac7])
        data=fixture();data[0x9d4]=4
        with self.assertRaisesRegex(ValueError,'complete body/cleanup'):analyze(data)
        data=fixture();data[0x8b2]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_operand_neighbor_and_producer(self):
        for dest in (0x8b3,0x966):
            data=fixture();data[0x8b2:0x8b5]=b'\xe9'+struct.pack('<h',dest-0x8b5)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x845]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_native_call_sites_and_push_cs(self):
        data=fixture();data[0x846:0x84a]=b'\x90\xe8'+struct.pack('<h',0x7da-0x84a)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        for code in (b'\xe8\x00\x00',b'\x0e\xe8'+struct.pack('<h',0xaae-0x84a)):
            data=fixture();data[0x846:0x846+len(code)]=code
            with self.assertRaisesRegex(ValueError,'unknown native call'):analyze(data)
        for code,msg in ((b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x846:0x846+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_interrupt_and_port_catalogue(self):
        for code,msg in ((b'\xcd\x20','unknown DOS'),(b'\xcd\x21','unknown DOS'),(b'\xe6\x60','unexpected port'),(b'\xe4\x60','unexpected port')):
            data=fixture();data[0x846:0x846+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class FileRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x846,patches=(),s=None):
        __import__('unicorn');data=fixture();observed=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return FileProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},observed)

    def test_callback_failures_outside_ffi_and_owned_dos_sites(self):
        __import__('unicorn')
        for code,msg in ((b'\xcd\x20','unknown DOS request/site'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('close')
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):
            self.probe(b'\xb4\x3f\xcd\x21',0x84a).run('close')

    def test_write_span_and_read_destination(self):
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\xc7\x06\x00\x00\x34\x12').run('close')
        with self.assertRaisesRegex(ValueError,'outside owned state'):
            self.probe(b'\xc7\x06\x19\x14\x34\x12').run('close')
        code=b'\xb8\x01\x60\x8e\xd8\xe9'+struct.pack('<h',0x8e4-0x8ba)
        with self.assertRaisesRegex(ValueError,'buffer read destination'):
            self.probe(code,0x8b2,[(0x8e4,b'\xb4\x3f\xcd\x21')]).run('read')

    def test_native_far_frames_and_actual_positive_returns(self):
        code=b'\xe9'+struct.pack('<h',0x7da-0x849)
        with self.assertRaisesRegex(ValueError,'native far frame'):
            self.probe(code).run('close')
        code=b'\x0e\xe8'+struct.pack('<h',0x7da-0x84a)+b'\xe9'+struct.pack('<h',0x854-0x84d)
        p=self.probe(code);p.run('close');self.assertEqual(dict(p.native),{'close':1,'flush':1})
        with self.assertRaisesRegex(ValueError,'native return frame'):
            self.probe(b'\x83\xc4\x02\xe9'+struct.pack('<h',0x854-0x84c)).run('close')

    def test_cleanup_segment_alias_and_stale_completion(self):
        p=self.probe(b'\xe9'+struct.pack('<h',0x854-0x849));p.run('close');p.uc.mem_write(p.code+0x846,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('close',budget=50)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):
            self.probe(b'\xbe\x00\x00\xe9'+struct.pack('<h',0x854-0x84c)).run('close')
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):
            self.probe(b'\xea\x10\xff\xff\x1f').run('close')
        with self.assertRaisesRegex(ValueError,'escaped file bodies/segment alias'):
            self.probe(b'\xea\xea\x07\xff\x1f').run('close')


if __name__=='__main__':unittest.main()
