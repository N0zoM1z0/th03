"""Complete title boundaries, external-clock waits and write-attempt guards."""
from importlib.util import find_spec
from pathlib import Path
from types import SimpleNamespace
import struct
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_op_title as d


def fixture():
    image=bytearray(d.DS*16+0x2200)
    for name,a,z,c in d.RANGES:
        at=d.CS*16+a;image[at:at+z]=b'\x90'*z
        end=b'\xc2\x02\x00' if c else b'\xc3';image[at+z-len(end):at+z]=end
    return image


class BoundaryAndScalarTests(unittest.TestCase):
    def test_complete_cleanup_and_interior_return(self):
        b=fixture();self.assertEqual(len(d.analyze(b)['bodies']),5)
        b[d.CS*16+0x180a]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):d.analyze(b)
        b=fixture();b[d.CS*16+0x1866]=0
        with self.assertRaisesRegex(ValueError,'cleanup'):d.analyze(b)

    def test_branch_operands_unknown_calls_and_input_interfaces(self):
        for code,message in [(b'\xeb\xff','operand/neighbor'),(b'\xff\xd0','indirect/operand'),
                             (b'\xe8\x00\x00','unknown native/model'),(b'\xe4\xff','input/interrupt')]:
            b=fixture();b[d.CS*16+0x14e2:d.CS*16+0x14e2+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):d.analyze(b)

    def test_column_reaches_beyond_vram_and_uses_unsigned_full_rank(self):
        for left,count,last in [(0,384,0),(640,385,0),(65535,486,31)]:
            spec=d.TitleSpec(bytes(0x100000),0,dict(tick_visits=3));spec.column(left)
            self.assertEqual(len(spec.writes),4*count);self.assertEqual(len(spec.reads),4*count)
            self.assertEqual(len(spec.events),2*count)
            self.assertEqual(spec.writes[-1][0],0xad000+last)
            self.assertEqual(spec.reads[0][0],0xad000+0x77b0+(left>>3))
            self.assertTrue(any(a>=0xc0000 for a,z,v in spec.writes))

    def test_title_frame_counts_and_brightness_are_preserved(self):
        spec=d.TitleSpec(bytes(0x100000),0,dict(tick_visits=3));spec.intro()
        self.assertEqual(sum(e['name']=='frame' for e in spec.events),162)
        self.assertEqual(spec.memory[d.BG:d.BG+3],bytes([254]*3))
        self.assertEqual(spec.memory[d.SHADOW:d.SHADOW+3],bytes([128]*3))
        self.assertEqual(int.from_bytes(spec.memory[d.TONE:d.TONE+2],'little'),100)
        self.assertEqual(spec.external,[(d.CLOCK,2,16)])
        spec=d.TitleSpec(bytes(0x100000),0,dict(tick_visits=3));spec.fade()
        self.assertEqual(sum(e['name']=='frame' for e in spec.events),26)
        for name,count in [('expand',13),('shrink',14)]:
            spec=d.TitleSpec(bytes(0x100000),0,dict(tick_visits=3));getattr(spec,name)()
            self.assertEqual(spec.native['column'],count)


@unittest.skipUnless(find_spec('unicorn'),'Unicorn unavailable')
class NativeGuardTests(unittest.TestCase):
    def probe(self,prefix=b'',name='intro'):
        b=fixture();a=next(a for n,a,z,c in d.RANGES if n==name);b[d.CS*16+a:d.CS*16+a+len(prefix)]=prefix
        return d.TitleProbe(SimpleNamespace(program_image=bytes(b),relocations=[]),
                            dict(profile=0,reply=0,cf=False,tick_visits=3,**{'if':True,'df':False}))
    def test_native_cleanup_and_stale_instruction_budget(self):
        p=self.probe();p.run('intro');self.assertTrue(p.stop)
        p=self.probe(name='column');p.run('column',[65535]);self.assertTrue(p.stop)
        p=self.probe(b'\x90\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('intro',budget=10)
        self.assertFalse(p.stop)

    def test_store_span_stack_alias_and_ffi_exception_propagation(self):
        for code,message in [(b'\xc7\x06\xd3\x02\x34\x12','complete store span'),
                             (b'\xb8\xff\x3f\x8e\xd0','stack segment alias'),
                             (b'\xb0\x01\xe6\xff','unexpected port interface')]:
            p=self.probe(code)
            with self.assertRaisesRegex(ValueError,message):p.run('intro')
            self.assertTrue(p.errors)

    def test_known_modeled_destination_requires_original_caller(self):
        p=self.probe();p.set('CS',0x2000);p.set('SP',0xffd0);p.uc.mem_write(p.stack+0xffd0,struct.pack('<HH',0xff00,0x2000+d.CS))
        p.uc.emu_start(0x20000+0x1aa4,0x100000,count=10)
        self.assertTrue(any('callee caller' in e for e in p.errors))

    def test_external_clock_reply_is_required_for_the_busy_wait_fixture(self):
        b=fixture();a=d.CS*16+0x14e2
        b[a:a+3]=b'\xe9'+struct.pack('<h',0x1635-0x14e5)
        a=d.CS*16+0x1635;b[a:a+7]=b'\x83\x3e\xe8\x11\x10\x72\xf9'
        for tick in (3,None):
            p=d.TitleProbe(SimpleNamespace(program_image=bytes(b),relocations=[]),
                           dict(profile=0,reply=0,cf=False,tick_visits=tick,**{'if':False,'df':True}))
            p.uc.mem_write(p.data+d.CLOCK,b'\0\0')
            if tick:p.run('intro',budget=1000);self.assertTrue(p.stop)
            else:
                with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('intro',budget=1000)
                self.assertFalse(p.stop)


if __name__=='__main__':unittest.main()
