"""Stack-allocation private prefix, register/flag ABI and shared heap context."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from test_mainl_heap_review import fixture as heap_fixture
from review_th03_mainl_smem import OWN_RANGES,SmemProbe,analyze


def fixture():
    data=heap_fixture()
    for _,a,z,_ in OWN_RANGES:
        data[a:a+z]=b'\x90'*z;data[a+z-3:a+z]=b'\xca\x02\x00'
    data[0x1eba:0x1ec0]=b'\x0e\xe8\xc8\x02\x72\x2f';data[0x1eb9]=data[0x1ef5]=0x90
    return data


class SmemBoundaryTests(unittest.TestCase):
    def test_complete_shared_context_and_own_cleanup(self):
        with self.assertRaisesRegex(ValueError,'complete include'):analyze(fixture()[:0x1ef4])
        data=fixture();data[0x1ef3]=4
        with self.assertRaisesRegex(ValueError,'complete body/far cleanup'):analyze(data)
        data=fixture();data[0x1eaa]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)
        data=fixture();data[0x21c0]=0x90
        with self.assertRaisesRegex(ValueError,'heap byte shared-tail'):analyze(data)

    def test_private_prefix_and_alignment(self):
        data=fixture();data[0x1ebe:0x1ec0]=b'\x90\x90'
        with self.assertRaisesRegex(ValueError,'private assignment prefix'):analyze(data)
        data=fixture();data[0x1ef5]=0
        with self.assertRaisesRegex(ValueError,'producer alignment'):analyze(data)
        data=fixture();data[0x1eba]=0x90
        with self.assertRaisesRegex(ValueError,'lacks PUSH CS'):analyze(data)

    def test_operand_neighbor_and_native_calls(self):
        for dest in (0x1ec1,0x1ef5):
            data=fixture();data[0x1ec0:0x1ec3]=b'\xe9'+struct.pack('<h',dest-0x1ec3)
            with self.assertRaisesRegex(ValueError,'branch enters operand/neighbor'):analyze(data)
        data=fixture();data[0x1ec0:0x1ec3]=b'\xe8'+struct.pack('<h',0x2186-0x1ec3)
        with self.assertRaisesRegex(ValueError,'unknown native call'):analyze(data)
        for code,msg in ((b'\xff\xd0','unknown indirect'),(b'\x9a\x00\x00\x00\x00','unknown far')):
            data=fixture();data[0x1ec0:0x1ec0+len(code)]=code
            with self.assertRaisesRegex(ValueError,msg):analyze(data)

    def test_own_bodies_have_no_dos_or_ports(self):
        for code in (b'\xcd\x21',b'\xcd\x20',b'\xe6\x60',b'\xe4\x60'):
            data=fixture();data[0x1ec0:0x1ec0+len(code)]=code
            with self.assertRaisesRegex(ValueError,'unexpected port/interrupt'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class SmemRuntimeTests(unittest.TestCase):
    def probe(self,code,at=0x1eaa,patches=(),s=None):
        __import__('unicorn');data=fixture();observed=analyze(data);data[at:at+len(code)]=code
        for a,b in patches:data[a:a+len(b)]=b
        return SmemProbe(SimpleNamespace(program_image=data,relocations=[]),s or {},observed)

    def test_callback_failures_outside_ffi_and_write_spans(self):
        __import__('unicorn')
        for code,msg in ((b'\xcd\x21','unknown DOS request/site'),(b'\xe6\x60','unexpected output'),(b'\xe4\x60','unexpected input'),(b'\xc7\x06\x5f\x14\x01\x00','outside owned state/header')):
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,msg):self.probe(code).run('release',[0x6000])
            self.assertEqual(stderr.getvalue(),'')

    def test_release_preserves_ax_and_all_declared_flags(self):
        code=b'\xb8\x01\x00\xe9'+struct.pack('<h',0x1eb6-0x1eb0)
        with self.assertRaisesRegex(ValueError,'far cleanup/callee-saved'):self.probe(code).run('release',[0x6000])
        code=b'\xf9\xe9'+struct.pack('<h',0x1eb6-0x1eae)
        with self.assertRaisesRegex(ValueError,'release flags'):self.probe(code).run('release',[0x6000])
        p=self.probe(b'\xe9'+struct.pack('<h',0x1eb6-0x1ead),s=dict(initial_cf=1,df=True,initial_flags=0xad6));p.run('release',[0x6000]);self.assertEqual(p.get('AX'),0x1111)

    def test_lazy_assignment_reenters_get_without_duplicate_frame(self):
        code=b'\x83\x3e\x52\x08\x00\x74\xf3\xe9'+struct.pack('<h',0x1ef2-0x1eca)
        init=b'\xc7\x06\x52\x08\x00\x60\xe9'+struct.pack('<h',0x21ac-0x218f)
        p=self.probe(code,0x1ec0,[(0x2186,init)],dict(top=0));p.run('get',[1]);self.assertEqual(dict(p.native),{'get':1,'assign_all':1})
        code=b'\xe9'+struct.pack('<h',0x2186-0x1ec3)
        with self.assertRaisesRegex(ValueError,'native far frame'):self.probe(code,0x1ec0).run('get',[1])

    def test_return_frames_segment_aliases_and_stale_completion(self):
        p=self.probe(b'\xe9'+struct.pack('<h',0x1eb6-0x1ead));p.run('release',[1]);p.uc.mem_write(p.code+0x1eaa,b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/budget'):p.run('release',[1],budget=50)
        code=b'\x83\xc4\x02\xe9'+struct.pack('<h',0x1eb6-0x1eb0)
        with self.assertRaisesRegex(ValueError,'native return frame'):self.probe(code).run('release',[1])
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\xff\x1f').run('release',[1])
        with self.assertRaisesRegex(ValueError,'escaped smem bodies/segment alias'):self.probe(b'\xea\xd0\x1e\xff\x1f').run('release',[1])


if __name__=='__main__':unittest.main()
