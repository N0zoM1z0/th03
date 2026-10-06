"""Root tail partitions, native frames, complete service/store guards and prefixes."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_mainl_root_tail as d


def fixture():
    data=bytearray(0xe3f0+0x3400)
    for _,a,z,c in d.RANGES+[('pfopen',0x2b16,281,8),('compare',0x2c30,56,'compare')]:
        data[a:a+z]=b'\x90'*z
        tail=b'\xc3' if c=='near' else b'\xc2\x08\x00' if c=='compare' else b'\xca'+struct.pack('<H',c) if c else b'\xcb'
        data[a+z-len(tail):a+z]=tail
    for a,v in d.PRODUCERS.items():data[a]=v
    for site,target in d.CALLS.items():
        data[site:site+3]=b'\xe8'+struct.pack('<h',target-site-3)
        if site in d.FAR:data[site-1]=0x0e
    return data


def jump(address,target):return b'\xe9'+struct.pack('<h',target-address-3)


class RootBoundaryTests(unittest.TestCase):
    def test_complete_bodies_cleanup_and_explicit_zero_producers(self):
        meta=d.analyze(fixture());self.assertEqual((meta['new_body_bytes'],meta['new_extent_bytes']),(701,722))
        for _,a,z,c in d.RANGES:
            data=fixture();data[a+z-1]=0x90
            with self.assertRaisesRegex(ValueError,'complete body/cleanup'):d.analyze(data)
        for address in d.PRODUCERS:
            data=fixture();data[address]^=1
            with self.assertRaisesRegex(ValueError,'producer byte'):d.analyze(data)

    def test_native_calls_branch_boundaries_and_far_prefixes(self):
        for code,message in ((jump(0xc36,0xc37),'branch enters'),(jump(0xc36,0xc71),'branch enters'),
                             (b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),
                             (b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0xc36:0xc36+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)
        data=fixture();data[0x17cb]=0x90
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):d.analyze(data)

    def test_interrupt_and_port_sites_widths(self):
        for code,message in ((b'\xcd\x21','unknown interrupt'),(b'\xcd\x29','unknown interrupt'),(b'\xe6\x7c','unknown port site')):
            data=fixture();data[0xc36:0xc36+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(data)
        data=fixture();data[0xc45:0xc47]=b'\xe7\x7c'
        with self.assertRaisesRegex(ValueError,'port width'):d.analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class RootRuntimeTests(unittest.TestCase):
    def probe(self,code=b'',address=0xc36,patches=(),scenario=None):
        __import__('unicorn');data=fixture();meta=d.analyze(data);data[address:address+len(code)]=code
        for a,code in patches:data[a:a+len(code)]=code
        return d.TailProbe(SimpleNamespace(program_image=data,relocations=[]),scenario or {},meta)

    def test_private_helpers_require_real_public_frames(self):
        p=self.probe(address=0x17ca);p.run('end')
        self.assertEqual(dict(p.native),dict(end=1,keyclear=1))
        for name in d.PRIVATE:
            with self.assertRaisesRegex(ValueError,'complete public caller'):p.run(name)
        with self.assertRaisesRegex(ValueError,'native entry frame'):
            self.probe(jump(0xc36,0x1ef6)).run('color',[7,192])
        with self.assertRaisesRegex(ValueError,'native return frame'):
            self.probe(b'\x83\xc4\x02'+jump(0xc39,0xc5c)).run('color',[7,192])

    def test_service_errors_raise_outside_ffi_and_full_store_spans(self):
        for code,message in ((b'\xcd\x21','unknown DOS request/site'),(b'\xcd\x29','unknown console'),(b'\xe6\x7c','unknown output'),
                             (b'\xe4\x60','unknown input'),(b'\xb8\x00\x90\x8e\xc0\x26\xc7\x06\x00\x00\x01\x00','outside declared')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('color',[7,192])
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'unknown divide trap'):
            self.probe(b'\x33\xdb\xf7\xf3').run('color',[7,192])

    def test_stale_completion_budget_and_segment_aliases(self):
        p=self.probe(jump(0xc36,0xc5c));p.run('color',[7,192]);p.uc.mem_write(p.code+0xc36,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('color',[7,192],budget=50)
        for code,message in ((b'\xea\x10\xff\xff\x1f','terminal segment alias'),(b'\xea\x46\x0c\xff\x1f','CODE/stack segment alias'),
                             (jump(0xc36,0xc71),'instruction boundaries')):
            with self.assertRaisesRegex(ValueError,message):self.probe(code).run('color',[7,192])

    def test_palette_alias_reads_blue_after_word_store(self):
        p=self.probe(scenario=dict(resident=0x2f80,palette=[0xf0,0xa0,0x70]+[0]*45));m=d.Scalar(p)
        m.run('set')
        self.assertEqual(m.writes[1],[0x2f810,2,0xf0a])
        self.assertEqual(m.writes[2],[0x2f812,1,0])
        self.assertFalse(m.flags&1024)

    def test_absent_joystick_ors_saved_si_and_returns_initial_ax(self):
        p=self.probe(scenario=dict(joystick=0,state=0x8000,df=True));m=d.Scalar(p)
        self.assertEqual(m.run('sense'),(0x1111,0))
        self.assertEqual(m.word(m.data+d.STAT),0x9357)
        self.assertFalse(m.ports);self.assertTrue(m.flags&1024)

    def test_unchecked_second_allocation_can_modify_low_dos_memory(self):
        p=self.probe(scenario=dict(allocations=[dict(ax=0x6000),dict(ax=8,cf=1)]));m=d.Scalar(p)
        self.assertEqual(m.run('create'),(1,0))
        self.assertEqual(m.word(0x71),65535)
        self.assertEqual(m.mem[0x80:0x8a],b'\0'*10)
        self.assertEqual(m.word(m.data+d.RESIDENT),8)

    def test_poll_prefix_is_an_open_native_call(self):
        p=self.probe(jump(0x2aae,0x2ac3),0x2aae,[(0x1f0c,b'\xba\x88\x01'),(0x1f0f,b'\xec\xeb\xfd')],dict(statuses=[128],pause_after_status=3))
        p.run('start',terminal=False)
        self.assertTrue(p.paused);self.assertFalse(p.stop)
        self.assertEqual((p.status_index,p.get('IP'),len(p.frames)),(3,0x1f0f,2))


if __name__=='__main__':unittest.main()
