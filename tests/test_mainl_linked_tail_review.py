"""Direct-link tail partitions, real IRQ frames, prefixes and producer OMF."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_mainl_linked_tail as d


def fixture():
    data=bytearray(0xe3f0+0x2200)
    for name,a,z,c in d.vsync.RANGES:
        data[a:a+z]=b'\x90'*z
        tail=b'\xcf' if c is None else b'\xca'+struct.pack('<H',c) if c else b'\xcb'
        data[a+z-len(tail):a+z]=tail
    for site,target in d.vsync.CALLS.items():
        data[site-1]=0x0e;data[site:site+3]=b'\xe8'+struct.pack('<h',target-site-3)
    for a,v in d.vsync.ALIGNMENT.items():data[a]=v
    for a,v in d.vsync.INDIRECT.items():data[a:a+len(v)]=v
    data[0x1ffa:0x2001]=b'\x83\x3e\x44\x08\x00\x74\x12'
    data[0x1fe2:0x1fe9]=b'\x50\x1e\xb8\x3f\x0e\x8e\xd8'
    data[0x2013:0x201c]=b'\x1f\xb0\x20\xe6\x00\xe6\x64\x58\xcf'
    for name,a,z,c in d.RANGES:
        at=d.CS*16+a;data[at:at+z]=b'\x90'*z
        tail=b'\xca'+struct.pack('<H',c) if c else b'\xcb';data[at+z-len(tail):at+z]=tail
    at=d.CS*16+0x372
    data[at:at+21]=b'\x55\x8b\xec\xc7\x06'+struct.pack('<H',d.COUNT1)+b'\x00\x00\xa1'+struct.pack('<H',d.COUNT1)+b'\x3b\x46\x06\x72\xf8\x5d\xca\x02\x00'
    for a in d.PRODUCERS:data[d.CS*16+a]=0x90
    return data


def jump(address,target):return b'\xe9'+struct.pack('<h',target-address-3)
def record(kind,payload):
    block=bytes([kind])+struct.pack('<H',len(payload)+1)+payload
    return block+bytes([-sum(block)&255])
def object_fixture(code=b'\x90',offset=0,duplicate=False):
    obj=record(0x80,b'\x04test')+record(0x96,b'\x06SHARED\x04CODE')
    obj+=record(0x98,b'\x28'+struct.pack('<H',len(code))+b'\x01\x02\x00')
    data=record(0xa0,b'\x01'+struct.pack('<H',offset)+code);obj+=data*(2 if duplicate else 1)
    return obj+record(0x8a,b'\x00')


class BoundaryTests(unittest.TestCase):
    def test_complete_functions_cleanup_and_all_producer_bytes(self):
        self.assertEqual(d.analyze(fixture())['new_bytes'],70)
        for _,a,z,_ in d.RANGES:
            data=fixture();data[d.CS*16+a+z-1]=0x90
            with self.assertRaisesRegex(ValueError,'complete body'):d.analyze(data)
        for a in d.PRODUCERS:
            data=fixture();data[d.CS*16+a]=0
            with self.assertRaisesRegex(ValueError,'producer byte'):d.analyze(data)

    def test_edges_reject_operands_neighbors_and_unknown_interfaces(self):
        for code,message in ((jump(2,3),'operand/neighbor'),(jump(2,0x372),'operand/neighbor'),(b'\xff\xe0','operand/neighbor'),
                             (b'\xcd\x21','unknown interface'),(b'\xe8\x00\x00','unknown interface')):
            data=fixture();data[d.CS*16+2:d.CS*16+2+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)

    def test_omf_complete_emission_checksums_overlap_and_bounds(self):
        self.assertEqual(d.object_code(object_fixture()),b'\x90')
        with self.assertRaisesRegex(ValueError,'overlap/bounds'):d.object_code(object_fixture(duplicate=True))
        with self.assertRaisesRegex(ValueError,'overlap/bounds'):d.object_code(object_fixture(offset=1))
        data=bytearray(object_fixture());data[8]^=1
        with self.assertRaisesRegex(ValueError,'checksum'):d.object_code(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class NativeTests(unittest.TestCase):
    def probe(self,patches=(),scenario=None):
        __import__('unicorn');data=fixture()
        for a,code in patches:data[a:a+len(code)]=code
        return d.TailProbe(SimpleNamespace(program_image=data,relocations=[]),scenario or {})

    def test_real_irq_iret_resumes_nonzero_shared_segment_and_open_frame(self):
        p=self.probe(scenario=dict(limit=4,df=True));p.run('delay',[1])
        self.assertFalse(p.stop);self.assertEqual((p.polls,p.native['irq']),(4,4))
        self.assertTrue(p.frame);self.assertIsNone(p.irq);self.assertEqual(p.get('CS'),0x2c7e)
        self.assertEqual(p.ports,[[0,32,False,True],[100,32,False,True]]*4)
        with self.assertRaisesRegex(ValueError,'complete public caller'):p.run('irq')

    def test_if_zero_delivers_no_irq_and_zero_frames_return(self):
        p=self.probe(scenario=dict(limit=4,**{'if':False}));p.run('delay',[65535])
        self.assertEqual(dict(p.native),dict(delay=1));self.assertFalse(p.stop);self.assertFalse(p.ports)
        p=self.probe(scenario=dict(**{'if':False}));p.run('delay',[0]);self.assertTrue(p.stop)

    def test_iret_mutations_reject_restoration_and_bad_flags(self):
        for patch,message in ((b'\x43','restoration differs'),(b'\x44','IRET frame differs')):
            p=self.probe([(0x1fe9,patch)],dict(limit=2))
            with self.assertRaisesRegex(ValueError,message):p.run('delay',[1])

    def test_stores_interfaces_and_segment_aliases_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in ((b'\xc7\x06'+struct.pack('<H',d.PLANES+15)+b'\x01\x00','complete planes/IRQ state span'),
                             (b'\xcd\x21','unexpected interrupt/input'),
                             (b'\xea\x12\x00\x7d\x2c','CODE segment alias')):
            p=self.probe();p.uc.mem_write(p.code+2,code);stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):p.run('planes')
            self.assertEqual(stderr.getvalue(),'')

    def test_stale_completion_and_native_return_frames(self):
        p=self.probe();p.run('planes');p.uc.mem_write(p.code+2,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('planes',budget=20)
        p=self.probe();p.uc.mem_write(p.code+2,b'\x83\xc4\x02')
        with self.assertRaisesRegex(ValueError,'far return frame'):p.run('planes')


if __name__=='__main__':unittest.main()
