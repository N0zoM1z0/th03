"""Complete graphics bodies, port widths, native frames and physical write guards."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_graphics import ALIGNMENT,CONTEXT_ALIGN,RANGES,EDGES,GraphicsProbe,Scalar,analyze,edge,subflags


def fixture():
    data=bytearray(0xe3f0+EDGES+34)
    for n,a,z,c in RANGES:
        data[a:a+z]=b'\x90'*z
        tail=b'\xc3' if c=='near' else b'\xca'+struct.pack('<H',c) if c else b'\xcb'
        data[a+z-len(tail):a+z]=tail
    for a,v in {**ALIGNMENT,**CONTEXT_ALIGN}.items():data[a]=v
    for at,to in ((0x75a,0x724),(0x780,0x73a)):
        data[at:at+4]=b'\x0e\xe8'+struct.pack('<h',to-at-4)
    data[0xe3f0+EDGES:]=struct.pack('<17H',*(edge(i) for i in range(17)))
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class GraphicsBoundaryTests(unittest.TestCase):
    def test_complete_partition_and_near_far_cleanup(self):
        self.assertEqual(analyze(fixture())['new_extent_bytes'],475)
        with self.assertRaisesRegex(ValueError,'complete body'):analyze(fixture()[:0xc70])
        for at in (0x738,0xb9a,0xc32,0xc70):
            data=fixture();data[at]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):analyze(data)
        data=fixture();data[0xc66]=0xcb
        with self.assertRaisesRegex(ValueError,'interior cleanup'):analyze(data)

    def test_native_calls_and_instruction_edges(self):
        data=fixture();data[0x75a]=0x90;data[0x75b:0x75e]=b'\xe8'+struct.pack('<h',0x724-0x75e)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        data[0x75a]=0x0e;analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','indirect edge'),(b'\x9a\x00\x00\x00\x00','unknown far edge'),(jump(0x724,0x725),'branch enters')):
            data=fixture();data[0x724:0x724+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_port_sites_widths_and_read_only_table(self):
        for code,at,msg in ((b'\xe6\x7c',0x724,'unknown port site'),(b'\xef',0xc66,'encoding/width'),(b'\xe4\xa0',0xc66,'unexpected interrupt/input'),(b'\xcd\x21',0x724,'unexpected interrupt/input')):
            data=fixture();data[at:at+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)
        data=fixture();data[0x739]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)
        data=fixture();data[0xe3f0+EDGES+2]^=1
        with self.assertRaisesRegex(ValueError,'edge table'):analyze(data)

    def test_independent_modular_subtraction_and_masks(self):
        self.assertEqual([edge(n) for n in (0,1,8,9,16)],[0,0x80,0xff,0x80ff,0xffff])
        self.assertEqual(subflags(0,1),1|4|16|128)
        self.assertEqual(subflags(0x8000,1),4|16|2048)
        self.assertEqual(subflags(0,0),4|64)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class GraphicsRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x724,patches=()):
        __import__('unicorn');data=fixture();meta=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return GraphicsProbe(SimpleNamespace(program_image=data,relocations=[]),{},meta)

    def test_native_far_call_and_public_near_frame(self):
        p=self.probe(b'\x0e\xe8'+struct.pack('<h',0x724-0x75e),0x75a);p.run('egc_start');self.assertEqual(dict(p.native),dict(egc_start=1,egc_on=1,egc_off=1))
        p=self.probe(b'\x90',0xc66);p.run('gdc');self.assertEqual(p.get('SP'),0xffc2)
        with self.assertRaisesRegex(ValueError,'native entry frame'):self.probe(jump(0x724,0x73a)).run('egc_on')
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(b'\x83\xc4\x02'+jump(0x727,0x738)).run('egc_on')

    def test_runtime_ports_services_and_entire_store_spans(self):
        for code,msg in ((b'\xe6\x7c','unknown port/site/width'),(b'\xe4\x7c','unexpected input'),(b'\xcd\x21','unexpected interrupt'),(b'\xc7\x06\x22\x05\x00\x00','outside declared surface/width'),(b'\xb8\x00\xc0\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12','outside declared surface/width')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('egc_on')
            self.assertEqual(stderr.getvalue(),'')
        p=self.probe(b'\xe7\xa0',0xc66)
        with self.assertRaisesRegex(ValueError,'unknown port/site/width'):p.run('gdc')

    def test_native_terminal_staleness_and_segment_aliases(self):
        p=self.probe(b'\x90');p.run('egc_on');p.uc.mem_write(p.code+0x724,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('egc_on',budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('egc_on')
        with self.assertRaisesRegex(ValueError,'CODE/stack segment alias'):self.probe(b'\xea\x40\x07\xff\x1f').run('egc_on')

    def test_scalar_direction_and_interrupt_contracts(self):
        p=self.probe(b'\x90');spec=Scalar(p)
        spec.s.update(flags=2,df=True);spec.run('box',[0,0,0,0]);self.assertTrue(spec.flags&512);self.assertTrue(spec.flags&1024)
        spec.run('color',[13,192]);self.assertFalse(spec.ports[-1]['live_if']);self.assertFalse(spec.flags&512);self.assertTrue(spec.flags&1024)


if __name__=='__main__':unittest.main()
