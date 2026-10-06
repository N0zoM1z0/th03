"""Adversarial controls for MAINL root boundaries and modeled foreign ABI."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_root import CS,DS,RANGES,TABLE,TABLE_WORDS,RootProbe,analyze


def fixture():
    data=bytearray(DS*16+0x3300)
    for _,start,size,kind,cleanup in RANGES:
        at=CS*16+start;data[at:at+size]=b'\x90'*size
        ret=(b'\xcb' if kind=='retf' else b'\xc2'+struct.pack('<H',int(cleanup)) if cleanup else b'\xc3')
        data[at+size-len(ret):at+size]=ret
    struct.pack_into('<9H',data,CS*16+TABLE,*TABLE_WORDS)
    return data


class RootBoundaryTests(unittest.TestCase):
    def test_interior_wrong_return_and_truncation_rejected(self):
        data=fixture();data[CS*16+0x78d]=0xc3
        with self.assertRaisesRegex(ValueError,'interior return'):analyze(data)
        with self.assertRaisesRegex(ValueError,'complete body/return'):analyze(fixture()[:CS*16+0xb3d])

    def test_branch_operand_and_cross_body_rejected(self):
        for dest in (0x187,0x19d):
            data=fixture();data[CS*16+0x186:CS*16+0x189]=b'\xe9'+struct.pack('<h',dest-0x189)
            with self.assertRaisesRegex(ValueError,'branch leaves body/enters operand'):analyze(data)

    def test_unknown_calls_and_indirect_edges_rejected(self):
        for code,message in [(b'\xe8\xfe\xff','near call'),(b'\x9a\xff\xff\x00\x00','far interface'),(b'\xff\xd0','indirect')]:
            data=fixture();data[CS*16+0x186:CS*16+0x186+len(code)]=code
            with self.assertRaisesRegex(ValueError,message):analyze(data)

    def test_switch_table_and_address_expression_rejected(self):
        data=fixture();struct.pack_into('<H',data,CS*16+TABLE,0x5a8)
        with self.assertRaisesRegex(ValueError,'switch catalogue'):analyze(data)
        data=fixture();data[CS*16+0x5a2:CS*16+0x5a7]=b'\x2e\xff\xa7\xb0\x06'
        with self.assertRaisesRegex(ValueError,'switch expression'):analyze(data)


@unittest.skipUnless(find_spec('unicorn'),'optional Unicorn unavailable')
class RootRuntimeTests(unittest.TestCase):
    def probe(self,code,entry=0x186):
        __import__('unicorn')
        data=fixture();data[CS*16+entry:CS*16+entry+len(code)]=code
        return RootProbe(SimpleNamespace(program_image=data,relocations=[]))

    def test_callback_failures_propagate_without_ffi_errors(self):
        for code,message in [(b'\xcd\x18','interrupt'),(b'\xba\xa4\x00\xef','port/width'),(b'\xba\x6a\x00\xec','input port')]:
            stderr=io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError,message):self.probe(code).run(0x186)
            self.assertEqual(stderr.getvalue(),'')

    def test_far_interface_and_terminal_segment_aliases_rejected(self):
        code=b'\x31\xc0'+b'\x50'*5+b'\x9a\xc7\x09\x7d\x2c\xc3'
        with self.assertRaisesRegex(ValueError,'interface segment alias'):self.probe(code).run(0x186)
        # 295E:FF10 aliases the terminal at 295F:FF00.
        with self.assertRaisesRegex(ValueError,'terminal segment alias'):self.probe(b'\xea\x10\xff\x5e\x29').run(0x186)

    def test_stale_terminal_and_incorrect_cleanup_rejected(self):
        p=self.probe(b'\xc3');p.run(0x186);p.uc.mem_write(p.code+0x186,b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError,'terminal/exec/budget'):p.run(0x186,budget=20)
        p.run(0x186,terminal=False,budget=20)
        with self.assertRaisesRegex(ValueError,'return stack/callee-saved'):self.probe(b'\xc2\x02\x00').run(0x186)

    def test_actual_far_return_preserves_caller_arguments(self):
        p=self.probe(b'\xcb',entry=0x78d);p.run(0x78d,(2,0x1234,0x4567,0x5678,0x6789))
        self.assertEqual(p.get('SP'),0xffd4)
        self.assertEqual(bytes(p.uc.mem_read(p.stack+0xffd4,10)),struct.pack('<5H',2,0x1234,0x4567,0x5678,0x6789))


if __name__=='__main__':unittest.main()
