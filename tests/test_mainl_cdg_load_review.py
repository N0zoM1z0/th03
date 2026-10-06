"""Adversarial controls for complete loader ownership and native far frames."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_cdg_load import CS, DS, RANGES, LoadProbe, analyze


def fixture():
    data = bytearray(DS*16+0x3300)
    for _, start, size, cleanup in RANGES:
        at = CS*16+start
        data[at:at+size] = b'\x90'*size
        data[at+size-3:at+size] = b'\xca'+struct.pack('<H', cleanup)
    return data


class LoaderBoundaryTests(unittest.TestCase):
    def test_cleanup_and_truncation_rejected(self):
        data = fixture()
        data[CS*16+0x7c6] = 6
        with self.assertRaisesRegex(ValueError, 'body/far cleanup'):
            analyze(data)
        with self.assertRaisesRegex(ValueError, 'body/far cleanup'):
            analyze(fixture()[:CS*16+0x98e])

    def test_branch_operand_and_neighbor_rejected(self):
        for dest in (0x73f, 0x7c8):
            data = fixture()
            data[CS*16+0x73e:CS*16+0x741] = b'\xe9'+struct.pack('<h', dest-0x741)
            with self.assertRaisesRegex(ValueError, 'branch enters operand/neighbor'):
                analyze(data)

    def test_near_call_requires_push_cs_and_far_entry(self):
        for code in (b'\xe8\x0f\x02', b'\x0e\xe8\x0f\x02'):
            data = fixture()
            data[CS*16+0x73e:CS*16+0x73e+len(code)] = code
            with self.assertRaisesRegex(ValueError, 'near call lacks PUSH CS/far entry'):
                analyze(data)

    def test_unknown_far_and_indirect_calls_rejected(self):
        for code, message in [(b'\x9a\xff\xff\x00\x00', 'unknown'), (b'\xff\xd0', 'indirect')]:
            data = fixture()
            data[CS*16+0x73e:CS*16+0x73e+len(code)] = code
            with self.assertRaisesRegex(ValueError, message):
                analyze(data)


@unittest.skipUnless(find_spec('unicorn'), 'optional Unicorn unavailable')
class LoaderRuntimeTests(unittest.TestCase):
    def probe(self, code):
        __import__('unicorn')
        data = fixture()
        data[CS*16+0x73e:CS*16+0x73e+len(code)] = code
        return LoadProbe(SimpleNamespace(program_image=data, relocations=[]), {'slot': 0})

    def test_guarded_callback_and_outside_write_rejected(self):
        __import__('unicorn')
        for code, message in [(b'\xcd\x18', 'interrupt'),
                              (b'\xb8\x00\x90\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12', 'memory write')]:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(code).run('single', {'slot': 0})
            self.assertEqual(stderr.getvalue(), '')

    def test_interface_and_terminal_segment_aliases_rejected(self):
        # These different segment:offset pairs share the allowed physical address.
        for code, message in [(b'\x9a\x76\x09\xff\x1f', 'interface segment alias'),
                              (b'\xea\x10\xff\x7d\x2c', 'terminal segment alias')]:
            with self.assertRaisesRegex(ValueError, message):
                self.probe(code).run('single', {'slot': 0})

    def test_stale_terminal_and_actual_far_cleanup_rejected(self):
        p = self.probe(b'\xca\x08\x00')
        p.run('single', {'slot': 0})
        p.uc.mem_write(p.code+0x73e, b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError, 'terminal/budget'):
            p.run('single', {'slot': 0}, budget=20)
        p.run('single', {'slot': 0}, budget=20, terminal=False)
        with self.assertRaisesRegex(ValueError, 'far cleanup/callee-saved'):
            self.probe(b'\xcb').run('single', {'slot': 0})


if __name__ == '__main__':
    unittest.main()
