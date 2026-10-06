"""Synthetic controls for remaining staff boundaries and declared CPU models."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_th03_mainl_transitions import CS, DS, RANGES, TransitionProbe, analyze


def fixture():
    data = bytearray(DS * 16 + 0x3300)
    for _, start, size, cleanup in RANGES:
        at = CS * 16 + start
        data[at:at + size] = b'\x90' * size
        terminal = b'\xc2' + struct.pack('<H', int(cleanup)) if cleanup else b'\xc3'
        data[at + size - len(terminal):at + size] = terminal
    return data


class TransitionBoundaryTests(unittest.TestCase):
    def test_wrong_cleanup_and_truncation_are_rejected(self):
        data = fixture()
        data[CS * 16 + 0x2802] = 6
        with self.assertRaisesRegex(ValueError, 'body/near cleanup'):
            analyze(data)
        with self.assertRaisesRegex(ValueError, 'body/near cleanup'):
            analyze(fixture()[:CS * 16 + 0x31f0])

    def test_branch_cannot_enter_operand_or_neighbor(self):
        for destination in (0x24e7, 0x2731):
            data = fixture()
            at = CS * 16 + 0x24e6
            data[at:at + 3] = b'\xe9' + struct.pack('<h', destination - 0x24e9)
            with self.assertRaisesRegex(ValueError, 'branch leaves body/enters operand'):
                analyze(data)

    def test_calls_require_declared_entries(self):
        for instructions, message in [(b'\x9a\xff\xff\x00\x00', 'unknown.*far interface'),
                                      (b'\xe8\x49\x02', 'unknown/interior'),
                                      (b'\xff\xd0', 'indirect')]:
            data = fixture()
            at = CS * 16 + 0x24e6
            data[at:at + len(instructions)] = instructions
            with self.assertRaisesRegex(ValueError, message):
                analyze(data)


@unittest.skipUnless(find_spec('unicorn'), 'optional private Unicorn runtime unavailable')
class TransitionRuntimeTests(unittest.TestCase):
    def probe(self, instructions):
        __import__('unicorn')
        data = fixture()
        at = CS * 16 + 0x24e6
        data[at:at + len(instructions)] = instructions
        return TransitionProbe(SimpleNamespace(program_image=data, relocations=[]))

    def test_callback_errors_leave_ffi(self):
        __import__('unicorn')
        for instructions, message in [(b'\xcd\x18', 'interrupt'),
                                      (b'\xba\xa4\x00\xef', 'port/width'),
                                      (b'\xba\x6a\x00\xec', 'input port')]:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(instructions).run(0x24e6)
            self.assertEqual(stderr.getvalue(), '')

    def test_stale_terminal_and_cleanup_are_rejected(self):
        p = self.probe(b'\xc3')
        p.run(0x24e6)
        p.uc.mem_write(p.code + 0x24e6, b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError, 'terminal/trap/budget'):
            p.run(0x24e6, budget=20)
        p.run(0x24e6, budget=20, terminal=False)
        with self.assertRaisesRegex(ValueError, 'stack/callee-saved'):
            self.probe(b'\xc2\x02\x00').run(0x24e6)

    def test_actual_divide_fault_requires_explicit_observation(self):
        instructions = b'\x31\xc0\x31\xd2\x31\xdb\xf7\xfb\xc3'
        p = self.probe(instructions)
        with self.assertRaisesRegex(ValueError, 'terminal/trap/budget'):
            p.run(0x24e6)
        p = self.probe(instructions)
        p.run(0x24e6, terminal=False, trap=True)
        self.assertEqual(p.trap['number'], 0)
        self.assertEqual(p.trap['address'], p.code + 0x24ec)

    def test_far_interface_segment_alias_is_rejected(self):
        # 2C7D:09C7 aliases the font entry's physical address 2C7E:09B7.
        instructions = b'\x31\xc0' + b'\x50' * 5 + b'\x9a\xc7\x09\x7d\x2c\xc3'
        with self.assertRaisesRegex(ValueError, 'interface segment alias'):
            self.probe(instructions).run(0x24e6)


if __name__ == '__main__':
    unittest.main()
