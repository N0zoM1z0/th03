"""Adversarial lifecycle checks: cleanup, near/far construction and guards."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_lifecycle import CS,DS,RANGES,LifecycleProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,start,size,cleanup in RANGES:
        at=CS*16+start;data[at:at+size]=b'\x90'*size
        ret=b'\xca'+struct.pack('<H',int(cleanup)) if cleanup else b'\xcb'
        data[at+size-len(ret):at+size]=ret
    return data


class LifecycleBoundaryTests(unittest.TestCase):
    def test_wrong_interior_return_and_truncation_rejected(self):
        data=fixture();data[CS*16+0x700]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)
        with self.assertRaisesRegex(ValueError,'complete body/far cleanup'):analyze(fixture()[:CS*16+0x98f])

    def test_near_call_requires_push_cs_and_far_entry(self):
        data=fixture();at=CS*16+0x700
        data[at:at+3]=b'\xe8'+struct.pack('<h',2-0x703)
        with self.assertRaisesRegex(ValueError,'PUSH CS/far entry'):analyze(data)
        data=fixture();data[at:at+4]=b'\x0e\xe8'+struct.pack('<h',2-0x704)
        analyze(data)
        data[at+2:at+4]=struct.pack('<h',3-0x704)
        with self.assertRaisesRegex(ValueError,'PUSH CS/far entry'):analyze(data)

    def test_operand_neighbor_unknown_calls_rejected(self):
        for code,message in [(b'\xe9'+struct.pack('<h',0x701-0x703),'branch enters operand'),
                             (b'\xe9'+struct.pack('<h',0x98f-0x703),'branch enters operand'),
                             (b'\x9a\xff\xff\x00\x00','unknown.*far interface'),
                             (b'\xff\xd0','indirect')]:
            data=fixture();data[CS*16+0x700:CS*16+0x700+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class LifecycleRuntimeTests(unittest.TestCase):
    def probe(self,code):
        __import__('unicorn')
        data=fixture();data[CS*16+0x700:CS*16+0x700+len(code)]=code
        return LifecycleProbe(SimpleNamespace(program_image=data,relocations=[]))

    def test_callbacks_and_interface_alias_rejected(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x18','interrupt'),(b'\xba\xa4\x00\xef','port/width'),(b'\xba\x6a\x00\xec','input port'),
                             (b'\x6a\x01\x9a\x4e\x21\xff\x1f','interface segment alias')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run(0x700,(0,0))
            self.assertEqual(stderr.getvalue(),'')

    def test_stale_terminal_and_wrong_far_cleanup_rejected(self):
        p=self.probe(b'\xca\x04\x00');p.run(0x700,(0,0));p.uc.mem_write(p.code+0x700,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/caller/budget'):p.run(0x700,(0,0),budget=20)
        p.run(0x700,(0,0),budget=20,terminal=False)
        with self.assertRaisesRegex(ValueError,'return stack/callee-saved'):self.probe(b'\xcb').run(0x700,(0,0))

    def test_push_cs_near_call_executes_actual_far_return(self):
        code=b'\x0e\xe8'+struct.pack('<h',2-0x704)+b'\xca\x04\x00'
        p=self.probe(code);p.run(0x700,(0x1234,0x6000))
        self.assertEqual(p.helper_frames,[[0x704,0x2c7e]])
        self.assertEqual(p.get('SP'),0xffd8)


if __name__=='__main__':unittest.main()
