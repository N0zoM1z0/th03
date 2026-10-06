"""Whole BFNT/super scopes, mutable near dispatch and native service/frame guards."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from test_mainl_smem_review import fixture as stack_fixture
from review_th03_mainl_super import ALIGNMENT,CONTEXT,OWN_RANGES,SuperProbe,analyze


def fixture():
    data=stack_fixture()
    for n,a,z,c in OWN_RANGES+CONTEXT[-2:]:
        data[a:a+z]=b'\x90'*z
        if n!='draw':
            tail=b'\xc3' if c=='near' else b'\xca'+struct.pack('<H',c) if c else b'\xcb';data[a+z-len(tail):a+z]=tail
    for a,v in ALIGNMENT.items():data[a]=v
    data[0x23a9:0x23ad]=b'\xff\x16\x7e\x08';data[0x276b:0x276e]=b'\xe9\x3e\xff';data[0x399]=data[0x23b7]=data[0x25b3]=0x90
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class SuperBoundaryTests(unittest.TestCase):
    def test_complete_body_partition_and_terminal_cleanup(self):
        self.assertEqual(analyze(fixture())['new_extent_bytes'],1542)
        with self.assertRaisesRegex(ValueError,'complete include'):analyze(fixture()[:0x276d])
        for at in (0x3b2,0x26ce):
            data=fixture();data[at]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):analyze(data)
        data=fixture();data[0x286]=0xc3
        with self.assertRaisesRegex(ValueError,'near/far cleanup'):analyze(data)

    def test_native_calls_push_cs_and_branch_ownership(self):
        data=fixture();data[0x371:0x374]=b'\xe8'+struct.pack('<h',0x23c2-0x374)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        data=fixture();data[0x286:0x289]=jump(0x286,0x276c)
        with self.assertRaisesRegex(ValueError,'branch enters'):analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x286:0x286+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_callback_dispatch_operands_and_producers(self):
        data=fixture();data[0x23a9:0x23ad]=b'\xff\x16\x7f\x08'
        with self.assertRaisesRegex(ValueError,'character-free operand'):analyze(data)
        data=fixture();data[0x276c]^=1
        with self.assertRaisesRegex(ValueError,'branch enters|initial mutable dispatch'):analyze(data)
        data=fixture();data[0xaad]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)
        data=fixture();data[0x399]=0
        with self.assertRaisesRegex(ValueError,'instruction partition|interior EVEN'):analyze(data)

    def test_service_and_port_sites(self):
        for code,msg in ((b'\xcd\x21','unknown DOS site'),(b'\xcd\x18','unknown DOS site'),(b'\xe6\x7c','unknown port site'),(b'\xe4\x7c','unknown port site')):
            data=fixture();data[0x286:0x286+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class SuperRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x237e,patches=(),s=None):
        __import__('unicorn');data=fixture();meta=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return SuperProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},meta)

    def test_service_errors_and_whole_write_spans(self):
        for code,msg in ((b'\xcd\x21','unknown DOS request/site'),(b'\xe6\x7c','unknown output port'),(b'\xe4\x7c','unexpected input'),(b'\xc7\x06\x7f\x08\x00\x00','outside declared state'),(b'\x2e\xc7\x06\x6c\x27\x00\x00'+jump(0x2385,0x276b),'mutable dispatch enters')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('free_all')
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'outside declared state'):self.probe(b'\x2e\xc7\x06\x6b\x27\x00\x00').run('free_all')
        p=self.probe(jump(0x237e,0xaa0),patches=[(0xaa0,b'\xcd\x21')])
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):p.run('free_all')

    def test_near_tail_call_and_character_callback_frames(self):
        p=self.probe(jump(0x25bc,0x2677),0x25bc,[(0x2677,b'\xe8'+struct.pack('<h',0x2766-0x267a)),(0x267a,jump(0x267a,0x26a9))])
        p.run('put',[0,0,0]);self.assertEqual(dict(p.native),dict(put=1,draw=1,draw1=1))
        with self.assertRaisesRegex(ValueError,'native entry frame'):self.probe(jump(0x237e,0x246e)).run('free_all')
        p=self.probe(jump(0x237e,0x23a9),patches=[(0x23a9,b'\xff\x16\x7e\x08')],s=dict(charfree=0x8000));p.run('free_all');self.assertEqual(p.char_calls,1)
        p=self.probe(jump(0x237e,0x23a9),patches=[(0x23a9,b'\xff\x16\x7e\x08')],s=dict(charfree=0x8001))
        with self.assertRaisesRegex(ValueError,'undeclared character-free'):p.run('free_all')

    def test_native_returns_and_mutable_counter_span(self):
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(b'\x83\xc4\x02'+jump(0x2381,0x23ad)).run('free_all')
        p=self.probe(b'\x2e\xc6\x06\xc9\x26\x07'+jump(0x2384,0x23ad));p.run('free_all');self.assertEqual(bytes(p.uc.mem_read(p.code+0x26c9,1)),b'\x07')
        with self.assertRaisesRegex(ValueError,'outside declared state'):self.probe(b'\x2e\xc7\x06\xc9\x26\x07\x00').run('free_all')

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe(jump(0x237e,0x23ad));p.run('free_all');p.uc.mem_write(p.code+0x237e,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('free_all',budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('free_all')
        with self.assertRaisesRegex(ValueError,'CODE/stack segment alias'):self.probe(b'\xea\x90\x23\xff\x1f').run('free_all')


if __name__=='__main__':unittest.main()
