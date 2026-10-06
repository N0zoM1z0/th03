"""Complete screen scopes, real private plane frames, synthetic page banks and services."""
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
from review_th03_mainl_screen import OWN_RANGES,ALIGNMENT,INTERIOR,NEAR,VRAM_WORDS,ScreenProbe,Scalar,analyze


def fixture():
    data=stack_fixture()
    for _,a,z,c in OWN_RANGES:
        data[a:a+z]=b'\x90'*z;tail=b'\xc3' if c=='near' else b'\xca'+struct.pack('<H',c) if c else b'\xcb';data[a+z-len(tail):a+z]=tail
    for a,v in (ALIGNMENT|INTERIOR).items():data[a]=v
    for at,to in NEAR.items():data[at:at+3]=b'\xe8'+struct.pack('<h',to-at-3)
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class ScreenBoundaryTests(unittest.TestCase):
    def test_complete_partitions_near_far_and_pascal_cleanup(self):
        self.assertEqual(analyze(fixture())['new_extent_bytes'],222)
        with self.assertRaisesRegex(ValueError,'complete body|complete include'):analyze(fixture()[:0xf00])
        for a in (0xe70,0xe94,0xeaa,0xefe):
            data=fixture();data[a]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):analyze(data)
        data=fixture();data[0xe96]=0xcb
        with self.assertRaisesRegex(ValueError,'interior cleanup'):analyze(data)

    def test_calls_and_instruction_ownership(self):
        data=fixture();data[0xeb9:0xebc]=b'\xe8'+struct.pack('<h',0x1ec0-0xebc)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        data[0xeb8]=0x0e;analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far'),(jump(0xe24,0xe25),'branch enters')):
            data=fixture();data[0xe24:0xe24+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_service_ports_and_producer_bytes(self):
        for code,a,msg in ((b'\xcd\x21',0xe28,'BIOS site'),(b'\xcd\x18',0xe24,'unknown interrupt'),(b'\xe4\xa6',0xe98,'port/site/width'),(b'\xe7\xa6',0xe98,'port/site/width'),(b'\xe6\xa6',0xe24,'port/site/width')):
            data=fixture();data[a:a+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)
        for a in (0xe71,0xeb7):
            data=fixture();data[a]=0
            with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class ScreenRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0xe24,patches=()):
        __import__('unicorn');data=fixture();meta=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return ScreenProbe(SimpleNamespace(program_image=data,relocations=[]),dict(words=7),meta)

    def test_real_near_frames_private_entry_and_wrong_returns(self):
        p=self.probe(jump(0xeac,0xed1),0xeac,[(0xef2,jump(0xef2,0xefe))]);p.run('copy',[1]);self.assertEqual(dict(p.native),dict(copy=1,plane=8))
        with self.assertRaisesRegex(ValueError,'complete public caller'):p.run('plane')
        with self.assertRaisesRegex(ValueError,'native entry frame'):self.probe(jump(0xe24,0xe96)).run('mode')
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(b'\x83\xc4\x02'+jump(0xe27,0xe70)).run('mode')

    def test_unknown_services_ports_and_full_store_spans(self):
        for code,msg in ((b'\xcd\x18','BIOS/DOS request/site'),(b'\xe6\xa6','output port/site/width'),(b'\xe4\xa6','unexpected input'),(b'\xc7\x06\x21\x05\x01\x00','outside declared state/buffer/aperture'),(b'\xb8\x00\xf0\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12','outside declared state/buffer/aperture')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('mode')
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'BIOS/DOS request/site'):self.probe(jump(0xe24,0xe28),patches=[(0xe28,b'\xcd\x18')]).run('mode')

    def test_page_selector_and_actual_bank_exchange(self):
        p=self.probe(jump(0xe24,0xe98),patches=[(0xe98,b'\xe6\xa6')])
        with self.assertRaisesRegex(ValueError,'page selector'):p.run('mode')
        p=self.probe(b'\xb0\x00'+jump(0xe26,0xe98),patches=[(0xe98,b'\xe6\xa6'+jump(0xe9a,0xe70))]);p.run('mode');self.assertEqual(p.selected,0)
        p.uc.mem_write(0xa8000,b'\x12\x34');p.save_page();p.load_page(1);self.assertNotEqual(bytes(p.uc.mem_read(0xa8000,2)),b'\x12\x34');p.load_page(0);self.assertEqual(bytes(p.uc.mem_read(0xa8000,2)),b'\x12\x34')

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe(jump(0xe24,0xe70));p.run('mode');p.uc.mem_write(p.code+0xe24,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('mode',budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('mode')
        with self.assertRaisesRegex(ValueError,'CODE/stack segment alias'):self.probe(b'\xea\x40\x0e\xff\x1f').run('mode')

    def test_scalar_clear_irq_and_modular_copy_counts(self):
        p=self.probe(jump(0xe24,0xe70))
        for flags in (0x402,0x602):
            spec=Scalar(p);spec.flags=flags;spec.run('clear');self.assertFalse(spec.ports[0]['live_if']);self.assertEqual(spec.ports[-1]['live_if'],bool(flags&512));self.assertTrue(spec.ports[-1]['live_df'])
        spec=Scalar(p);spec.flags=0x402;spec.run('copy',[1]);self.assertEqual(len(spec.writes),131072);self.assertEqual(spec.selected,1);self.assertEqual(spec.get(VRAM_WORDS),7)


if __name__=='__main__':unittest.main()
