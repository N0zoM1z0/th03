"""Complete gaiji scopes, public callers, private near helpers and font I/O guards."""
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
from review_th03_mainl_gaiji import OWN_RANGES,CONTEXT,NEW_ALIGN,INTERIOR,NEAR,TEMPLATE,GaijiProbe,Scalar,analyze


def fixture():
    data=stack_fixture();data.extend(b'\0'*max(0,0xe3f0+TEMPLATE+8-len(data)))
    for n,a,z,c in OWN_RANGES+CONTEXT[-3:]:
        data[a:a+z]=b'\x90'*z;tail=b'\xc3' if c=='near' else b'\xca'+struct.pack('<H',c) if c else b'\xcb';data[a+z-len(tail):a+z]=tail
    for a,v in {**NEW_ALIGN,**INTERIOR}.items():data[a]=v
    for at,to in NEAR.items():data[at:at+3]=b'\xe8'+struct.pack('<h',to-at-3)
    data[0xe3f0+TEMPLATE:0xe3f0+TEMPLATE+8]=struct.pack('<4H',16,16,0,255)
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class GaijiBoundaryTests(unittest.TestCase):
    def test_complete_partition_and_all_terminal_cleanup(self):
        self.assertEqual(analyze(fixture())['new_extent_bytes'],434)
        with self.assertRaisesRegex(ValueError,'complete body|complete include'):analyze(fixture()[:0xe23])
        for at in (0xc95,0xd45,0xd68,0xe21):
            data=fixture();data[at]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):analyze(data)
        data=fixture();data[0xd48]=0xcb
        with self.assertRaisesRegex(ValueError,'interior cleanup'):analyze(data)

    def test_native_call_frames_and_operand_edges(self):
        data=fixture();data[0xc80:0xc83]=b'\xe8'+struct.pack('<h',0x21c2-0xc83)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        data[0xc7f]=0x0e;analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far'),(jump(0xc72,0xc73),'branch enters')):
            data=fixture();data[0xc72:0xc72+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_exact_port_widths_sites_and_dos_sites(self):
        for code,at,msg in ((b'\xe6\xa1',0xc72,'port site/width'),(b'\xe5\xa9',0xd58,'port site/width'),(b'\xe7\xa1',0xd48,'port site/width'),(b'\xcd\x21',0xc72,'unknown DOS'),(b'\xcd\x18',0xd18,'unknown DOS')):
            data=fixture();data[at:at+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_producer_and_read_only_data_boundaries(self):
        for a in (0xd69,0xc7e):
            data=fixture();data[a]=0
            with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)
        data=fixture();data[0xe3f0+TEMPLATE]^=1
        with self.assertRaisesRegex(ValueError,'header template'):analyze(data)
        data=fixture();data[0xc71]=0xff
        self.assertEqual(analyze(data)['unowned_preceding_byte']['value'],255)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class GaijiRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0xc72,patches=()):
        __import__('unicorn');data=fixture();meta=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return GaijiProbe(SimpleNamespace(program_image=data,relocations=[]),{},meta)

    def test_private_helpers_require_actual_public_frames(self):
        p=self.probe(jump(0xd6a,0xd84),0xd6a);p.run('read',[0,0x5000,17]);self.assertEqual(dict(p.native),dict(read=1,getfont=1))
        with self.assertRaisesRegex(ValueError,'complete public caller'):p.run('getfont')
        with self.assertRaisesRegex(ValueError,'native entry frame'):self.probe(jump(0xc72,0xd48)).run('backup')
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(b'\x83\xc4\x02'+jump(0xc75,0xc95)).run('backup')

    def test_ports_latches_dos_and_whole_store_spans(self):
        for code,msg in ((b'\xe4\xa9','input port/site/width'),(b'\xe6\xa1','output port/site/width'),(b'\xcd\x21','DOS request/site'),(b'\xc7\x06\x5b\x05\x01\x00','outside declared state/pattern/heap'),(b'\xb8\x00\xa0\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12','outside declared state/pattern/heap')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('backup')
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'font latch/mode'):self.probe(jump(0xc72,0xd58),patches=[(0xd58,b'\xe4\xa9')]).run('backup')
        with self.assertRaisesRegex(ValueError,'input port/site/width'):self.probe(jump(0xc72,0xd58),patches=[(0xd58,b'\xe5\xa9')]).run('backup')

    def test_budget_staleness_and_segment_aliases(self):
        p=self.probe(jump(0xc72,0xc95));p.run('backup');p.uc.mem_write(p.code+0xc72,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('backup',budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('backup')
        with self.assertRaisesRegex(ValueError,'CODE/stack segment alias'):self.probe(b'\xea\x90\x0c\xff\x1f').run('backup')

    def test_independent_carry_if_and_font_half_order(self):
        p=self.probe(jump(0xc72,0xc95));spec=Scalar(p);spec.flags=3;spec.df=False;spec.run('read_all',[0,0x5000])
        self.assertEqual(spec.ports[1]['value'],1);self.assertEqual(spec.mem[0x50000:0x50002],spec.fonts[32:34]);self.assertEqual(spec.ports[67]['value'],1)
        spec=Scalar(p);spec.flags=2;spec.run('read',[0,0x5000,256]);self.assertTrue(spec.flags&512);self.assertEqual(spec.ports[1]['value'],0);self.assertEqual(spec.ports[4]['value'],spec.fonts[1])


if __name__=='__main__':unittest.main()
