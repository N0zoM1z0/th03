"""Adversarial decoded PI ownership and native-call contract controls."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_pi import CS, DS, RANGES, HELPERS, PiProbe, analyze, difference_partition


def fixture(original=True):
    data = bytearray(DS*16+0x3300)
    for _, a, b, size, cleanup in RANGES:
        at = CS*16+(a if original else b)
        data[at:at+size] = b'\x90'*size
        data[at+size-3:at+size] = b'\xca'+struct.pack('<H', cleanup)
    for _, start, size, cleanup in HELPERS:
        data[start:start+size] = b'\x90'*size
        ret = b'\xca'+struct.pack('<H', cleanup) if cleanup else b'\xcb'
        data[start+size-len(ret):start+size] = ret
    data[CS*16+(0x529 if original else 0x65d)] = 0x90 if original else 0
    return data


class PiBoundaryTests(unittest.TestCase):
    def test_complete_failure_partition_rejects_extra_unowned_byte(self):
        original = bytearray(DS*16+0x3300)
        candidate = bytearray(original)
        for at, size in [(CS*16+0x529, 300), (0x95f0+0x186, 10),
                         (0x95f0+0xb3e, 3), (0x95f0+0x189e, 6),
                         (0x95f0+0x24e6, 20), (DS*16+0x849, 1)]:
            candidate[at:at+size] = b'\x01'*size
        self.assertEqual(difference_partition(original, candidate)['different_bytes'], 340)
        candidate[42] = 1
        with self.assertRaisesRegex(ValueError, 'unclassified changed bytes'):
            difference_partition(original, candidate)
        with self.assertRaisesRegex(ValueError, 'lengths differ'):
            difference_partition(original, candidate[:-1])

    def test_truncation_cleanup_and_neighbor_rejected(self):
        self.assertEqual(analyze(fixture())['body_bytes'], 555)
        self.assertEqual(analyze(fixture(False), original=False)['helper_bytes'], 112)
        data = fixture()
        data[CS*16+0x54d] = 6
        with self.assertRaisesRegex(ValueError, 'body/far cleanup'):
            analyze(data)
        with self.assertRaisesRegex(ValueError, 'body/far cleanup'):
            analyze(fixture()[:0x4ba0])
        data = fixture()
        data[CS*16+0x529] = 0
        with self.assertRaisesRegex(ValueError, 'neighboring byte'):
            analyze(data)

    def test_branch_operand_and_neighbor_rejected(self):
        for dest in (0x550, 0x5d7):
            data = fixture()
            data[CS*16+0x54f:CS*16+0x552] = b'\xe9'+struct.pack('<h', dest-0x552)
            with self.assertRaisesRegex(ValueError, 'branch enters operand/neighbor'):
                analyze(data)

    def test_free_near_call_requires_push_cs_and_entry(self):
        for code in (b'\xe8'+struct.pack('<h', 0x22b2-0xfef),
                     b'\x0e\xe8'+struct.pack('<h', 0x22b3-0xff0)):
            data = fixture()
            data[0xfec:0xfec+len(code)] = code
            with self.assertRaisesRegex(ValueError, 'near call lacks PUSH CS/far entry'):
                analyze(data)

    def test_unknown_far_and_indirect_edges_rejected(self):
        for code, message in [(b'\x9a\xff\xff\x00\x00', 'unknown'), (b'\xff\xd0', 'indirect')]:
            data = fixture()
            data[CS*16+0x54f:CS*16+0x54f+len(code)] = code
            with self.assertRaisesRegex(ValueError, message):
                analyze(data)


@unittest.skipUnless(find_spec('unicorn'), 'optional Unicorn unavailable')
class PiRuntimeTests(unittest.TestCase):
    scenario = {'slot': 0, 'top': 0, 'left': 0}

    def probe(self, code):
        __import__('unicorn')
        data = fixture()
        data[CS*16+0x54f:CS*16+0x54f+len(code)] = code
        return PiProbe(SimpleNamespace(program_image=data, relocations=[]), self.scenario)

    def test_callbacks_and_outside_data_writes_rejected(self):
        __import__('unicorn')
        for code, message in [(b'\xcd\x18', 'interrupt'),
                              (b'\xb8\x00\x90\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12', 'data write')]:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(code).run('put', self.scenario)
            self.assertEqual(stderr.getvalue(), '')

    def test_interface_and_terminal_segment_aliases_rejected(self):
        for code, message in [(b'\x9a\x42\x16\xff\x1f', 'interface segment alias'),
                              (b'\xea\x10\xff\x7d\x2c', 'terminal segment alias')]:
            with self.assertRaisesRegex(ValueError, message):
                self.probe(code).run('put', self.scenario)

    def test_stale_terminal_and_actual_far_cleanup_rejected(self):
        p = self.probe(b'\xca\x06\x00')
        p.run('put', self.scenario)
        p.uc.mem_write(p.code+0x54f, b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError, 'terminal/budget'):
            p.run('put', self.scenario, budget=20)
        p.run('put', self.scenario, terminal=False, budget=20)
        with self.assertRaisesRegex(ValueError, 'far cleanup/callee-saved'):
            self.probe(b'\xcb').run('put', self.scenario)


if __name__ == '__main__':
    unittest.main()
