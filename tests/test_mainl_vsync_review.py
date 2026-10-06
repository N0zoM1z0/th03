"""VSYNC whole includes, ISR/far frames, vector and hardware guard controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_vsync import ALIGNMENT,INDIRECT,RANGES,RAW,VsyncProbe,analyze


def fixture():
    data=bytearray(b'\x90'*0x237e)
    for _,a,z,c in RANGES:
        tail=b'\xcf' if c is None else b'\xca'+struct.pack('<H',c) if c else b'\xcb'
        data[a+z-len(tail):a+z]=tail
    data[RAW:RAW+4]=b'\0'*4;data[0x1fe4:0x1fe7]=b'\xb8\x3f\x0e'
    for a,b in INDIRECT.items():data[a:a+len(b)]=b
    for a,v in ALIGNMENT.items():data[a]=v
    return data


def jump(at,to):return b'\xe9'+struct.pack('<h',to-at-3)


class VsyncBoundaryTests(unittest.TestCase):
    def test_complete_includes_and_iret_far_cleanup(self):
        self.assertEqual(analyze(fixture())['new_include_bytes'],368)
        with self.assertRaisesRegex(ValueError,'complete include'):analyze(fixture()[:0x2089])
        for at in (0x201b,0x722):
            data=fixture();data[at]=0x90
            with self.assertRaisesRegex(ValueError,'terminal cleanup'):analyze(data)
        data=fixture();data[0x1f6e]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)

    def test_branches_native_calls_and_push_cs(self):
        for dest in (0x1f6f,RAW):
            data=fixture();data[0x1f6e:0x1f71]=jump(0x1f6e,dest)
            with self.assertRaisesRegex(ValueError,'branch enters data/operand/neighbor'):analyze(data)
        data=fixture();data[0x1f73:0x1f76]=b'\xe8'+struct.pack('<h',0xf02-0x1f76)
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)
        for code,msg in ((b'\xe8\x00\x00','unknown native call'),(b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x1f6e:0x1f6e+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_declared_far_operands_state_relocation_and_producers(self):
        for at in (0x1fdc,0x200a):
            data=fixture();data[at]^=1
            with self.assertRaisesRegex(ValueError,'declared indirect operand'):analyze(data)
        data=fixture();data[RAW]=1
        with self.assertRaisesRegex(ValueError,'initial CS saved-vector'):analyze(data)
        data=fixture();data[0x1fe5]=0
        with self.assertRaisesRegex(ValueError,'DGROUP relocation operand'):analyze(data)
        data=fixture();data[0x723]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)

    def test_service_and_port_sites(self):
        for code,msg in ((b'\xcd\x18','unknown interrupt'),(b'\xcd\x21','unknown interrupt'),(b'\xe6\x02','unknown port'),(b'\xe4\x02','unknown port')):
            data=fixture();data[0x1f6e:0x1f6e+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class VsyncRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x1f6e,patches=(),s=None):
        __import__('unicorn');data=fixture();observed=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return VsyncProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},observed)

    def test_callback_errors_and_unowned_write_spans(self):
        __import__('unicorn')
        for code,msg in ((b'\xcd\x18','unknown BIOS request/site'),(b'\xcd\x21','unknown DOS request/site'),(b'\xe6\x02','unknown output port/site/width'),(b'\xe4\x02','unknown input port/site/width'),(b'\xc7\x06\x57\x14\x00\x00','outside owned state/span'),(b'\x2e\xc7\x06\x6d\x1f\x00\x00','outside owned state/span')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('start')
            self.assertEqual(stderr.getvalue(),'')
        with self.assertRaisesRegex(ValueError,'unknown DOS request/site'):self.probe(jump(0x704,0x712),0x704,[(0x712,b'\xcd\x21')]).run('vector',[1,0,10])
        with self.assertRaisesRegex(ValueError,'unknown BIOS request/site'):self.probe(jump(0xf02,0xf1a),0xf02,[(0xf1a,b'\xcd\x18')]).run('mode',[0,0])
        with self.assertRaisesRegex(ValueError,'unknown output port/site/width'):self.probe(jump(0x1f6e,0x1fb4),patches=[(0x1fb4,b'\xe7\x02')]).run('start')

    def test_native_call_and_interrupt_return_frames(self):
        with self.assertRaisesRegex(ValueError,'native entry frame'):self.probe(jump(0x1f6e,0x704)).run('start')
        code=b'\x83\xc4\x02'+jump(0x1f71,0x1fd7)
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(code).run('start')
        code=b'\x8b\xdc\x36\x81\x77\x04\x01\x00'+jump(0x1fea,0x201b)
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(code,0x1fe2).run('irq')
        p=self.probe(jump(0x1fe2,0x201b),0x1fe2,s=dict(df=True,flags=0xad7,entry_ds=0x5000));p.run('irq');self.assertEqual(p.get('DS'),0x5000);self.assertEqual(p.get('EFLAGS')&0xfd5,0xed5)
        p=self.probe(b'\x9c',0x1fd8,s=dict(entry_ax=0x0300,bios_other_ax=0xbeef));p.run('crt');self.assertEqual(p.get('AX'),0xbeef);self.assertEqual(p.external['old_bios'],1)
        p=self.probe(jump(0x1f6e,0x1fd7));p.run('vector_irq');self.assertEqual(p.external['old_irq'],1);self.assertEqual(p.get('CS'),0x2000)

    def test_indirect_targets_vector_dispatch_and_callback_cld(self):
        p=self.probe(jump(0x1f6e,0x1fd9));p.uc.mem_write(p.code+RAW,struct.pack('<2H',0,0))
        with self.assertRaisesRegex(ValueError,'undeclared external pointer'):p.run('start')
        p=self.probe(jump(0xf02,0xf1a),0xf02,[(0xf1a,b'\xcd\x18')],dict(entry_ax=0x3100));p.uc.mem_write(96,struct.pack('<2H',0,0))
        p.uc.mem_write(p.code+0xf02,b'\xb4\x31'+jump(0xf04,0xf1a))
        with self.assertRaisesRegex(ValueError,'undeclared vector dispatch'):p.run('mode',[0,0])
        p=self.probe(jump(0x1fe2,0x2008),0x1fe2,s=dict(proc=[0x200,0x9000],df=True))
        with self.assertRaisesRegex(ValueError,'callback DS/CLD/live IF'):p.run('irq')

    def test_stale_completion_and_segment_aliases(self):
        p=self.probe(jump(0x1f6e,0x1fd7));p.run('start');p.uc.mem_write(p.code+0x1f6e,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('start',budget=50)
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('start')
        with self.assertRaisesRegex(ValueError,'escaped vsync instruction ownership/segment alias'):self.probe(b'\xea\x7e\x1f\xff\x1f').run('start')


if __name__=='__main__':unittest.main()
