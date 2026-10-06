"""Archive-hook table/data boundaries, guarded callbacks and native IRET controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_mainl_pfint21 as hook


def fixture():
    data=bytearray(0xe3f0+0x3300)
    for name,a,z,cleanup in hook.NATIVE:
        data[a:a+z]=b'\x90'*z
        if name in ('archive_len','archive_plain','archive_keyed'):ret=b'\xc3'
        elif name=='compare':ret=b'\xc2\x08\0'
        else:ret=b'\xca'+struct.pack('<H',cleanup)
        data[a+z-len(ret):a+z]=ret
    for a,v in {**hook.bf.ALIGNMENT,**hook.pf.ALIGNMENT,0x2c2f:0x90}.items():data[a]=v
    for _,a,z in hook.OWN:data[a:a+z]=b'\x90'*z
    data[hook.ORG:0x2856]=b'\0'*5+b'\x90';data[0x290f:0x2912]=b'\xca\x04\0';data[0x2949]=0xcb;data[0x2aac]=0xcf;data[0x2aad]=0
    data[0x2982:0x29b2]=b''.join(struct.pack('<2H',*x) for x in hook.TABLE);data[0x2a78:0x2a7a]=b'\xcf\x14'
    return data


class HookBoundaryTests(unittest.TestCase):
    def test_complete_returns_and_truncation(self):
        with self.assertRaisesRegex(ValueError,'complete'):hook.analyze(fixture()[:0x2aac])
        data=fixture();data[0x2910]=2
        with self.assertRaisesRegex(ValueError,'far cleanup'):hook.analyze(data)
        data=fixture();data[0x2aac]=0xcb
        with self.assertRaisesRegex(ValueError,'far cleanup|terminal return'):hook.analyze(data)

    def test_complete_tables_and_state_partition(self):
        for at in (0x2984,0x29af,0x2a78):
            data=fixture();data[at]^=1
            with self.assertRaisesRegex(ValueError,'dispatch/IOCTL table'):hook.analyze(data)
        for at in (hook.ORG,0x2855,0x2aad):
            data=fixture();data[at]^=1
            with self.assertRaisesRegex(ValueError,'CS state/alignment'):hook.analyze(data)

    def test_branches_into_tables_operands_and_foreign_code(self):
        for dest in (0x2857,0x2982,0x2a78,0x2aad):
            data=fixture();data[0x2856:0x2859]=b'\xe9'+struct.pack('<h',dest-0x2859)
            with self.assertRaisesRegex(ValueError,'data/operand/neighbor'):hook.analyze(data)

    def test_vector_dispatch_calls_and_unowned_interrupts(self):
        for at,code,message in [(0x2952,b'\x2e\xff\x2e\x51\x28','saved-vector'),(0x297e,b'\x2e\xff\x64\x03','dispatch operand'),
                               (0x2856,b'\xe8\x00\x00','far call/PUSH CS'),(0x2856,b'\xcd\x21','unknown vector interrupt'),(0x2856,b'\xe6\x60','unexpected port')]:
            data=fixture();data[at:at+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):hook.analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class HookRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x2856):
        __import__('unicorn');data=fixture();observed=hook.analyze(data);data[at:at+len(code)]=code
        # Exercise runtime guards independently from the static negative controls.
        return hook.HookProbe(SimpleNamespace(program_image=data,relocations=[]),{},observed)

    def test_guarded_callbacks_raise_outside_ffi(self):
        __import__('unicorn')
        for code,message in [(b'\xcd\x20','unexpected interrupt'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run('start')
            self.assertEqual(stderr.getvalue(),'')

    def test_native_frames_and_whole_span_write_ownership(self):
        with self.assertRaisesRegex(ValueError,'outside owned state'):self.probe(b'\xc7\x06\0\0\x34\x12').run('start')
        code=b'\xe9'+struct.pack('<h',0x21ae-0x2859)
        with self.assertRaisesRegex(ValueError,'modeled far frame'):self.probe(code).run('start')
        code=b'\xe9'+struct.pack('<h',0x19a4-0x2859)
        with self.assertRaisesRegex(ValueError,'native far frame'):self.probe(code).run('start')
        code=b'\xe9'+struct.pack('<h',0x1952-0x2859)
        with self.assertRaisesRegex(ValueError,'native near frame'):self.probe(code).run('start')

    def test_runtime_dispatch_index_and_destination(self):
        for index,message in ((0x2983,'dispatch index'),(0x2982,'dispatch target')):
            code=b'\xbe'+struct.pack('<H',index)+b'\xe9'+struct.pack('<h',0x297e-0x2950)
            p=self.probe(code,0x294a)
            if index==0x2982:p.uc.mem_write(p.code+0x2984,b'\xb3\x29')
            with self.assertRaisesRegex(ValueError,message):p.run('hook')

    def test_native_iret_stale_completion_cleanup_and_aliases(self):
        p=self.probe(b'\xcf',0x294a);p.run('hook',{'AX':0x1234,'EFLAGS':0x603});self.assertEqual(p.get('AX'),0x1234);self.assertEqual(p.get('EFLAGS')&0x601,0x601)
        p.uc.mem_write(p.code+0x294a,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('hook',budget=10000)
        with self.assertRaisesRegex(ValueError,'far/interrupt cleanup'):self.probe(b'\xca\x02\0').run('start')
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('start')
        with self.assertRaisesRegex(ValueError,'old-kernel stack/entry'):self.probe(b'\xea\x00\x01\x00\x90').run('start')


if __name__=='__main__':unittest.main()
