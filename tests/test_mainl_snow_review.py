"""Synthetic fail-closed controls for snow ownership, assets and CPU scope."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_th03_mainl_snow import CS, DS, RANGES, SnowProbe, analysis, sine_words, sprite_from_bmp


def fixture():
    data = bytearray(DS * 16 + 0x3800)
    for _, segment, start, size, kind, cleanup in RANGES:
        at = segment * 16 + start
        data[at:at + size] = b'\x90' * size
        opcode = b'\xca' if kind == 'retf' else b'\xc2'
        terminal = opcode + struct.pack('<H', int(cleanup, 0)) if cleanup else (b'\xcb' if kind == 'retf' else b'\xc3')
        data[at + size - len(terminal):at + size] = terminal
    data[DS * 16 + 0x5ba:DS * 16 + 0x83a] = struct.pack('<320h', *sine_words())
    return data


class SnowBoundaryTests(unittest.TestCase):
    def test_wrong_cleanup_and_truncated_body_are_rejected(self):
        data = fixture()
        data[0xc7e * 16 + 0x153] = 10
        with self.assertRaisesRegex(ValueError, 'return cleanup'):
            analysis(data)
        with self.assertRaisesRegex(ValueError, 'complete body'):
            analysis(fixture()[:CS * 16 + 0x2730])

    def test_branch_cannot_enter_operand_or_another_body(self):
        for destination in (0x2577, 0x2590):
            data = fixture()
            at = CS * 16 + 0x2576
            data[at:at + 3] = b'\xe9' + struct.pack('<h', destination - 0x2579)
            with self.assertRaisesRegex(ValueError, 'branch leaves body or enters operand'):
                analysis(data)

    def test_unknown_or_indirect_call_is_rejected(self):
        for instructions, message in [(b'\x9a\xff\xff\x00\x00', 'unreviewed/interior'),
                                      (b'\xff\xd0', 'indirect')]:
            data = fixture()
            at = CS * 16 + 0x2576
            data[at:at + len(instructions)] = instructions
            with self.assertRaisesRegex(ValueError, message):
                analysis(data)

    def test_table_and_bitmap_layout_mutations_are_rejected(self):
        data = fixture()
        data[DS * 16 + 0x5bb] ^= 1
        with self.assertRaisesRegex(ValueError, 'scalar table'):
            analysis(data)
        with self.assertRaisesRegex(ValueError, 'one-bit layout/palette'):
            sprite_from_bmp(b'BM' + bytes(188))


@unittest.skipUnless(find_spec('unicorn'), 'optional private Unicorn runtime unavailable')
class SnowRuntimeTests(unittest.TestCase):
    def probe(self, instructions):
        __import__('unicorn')
        data = fixture()
        at = CS * 16 + 0x2576
        data[at:at + len(instructions)] = instructions
        return SnowProbe(SimpleNamespace(program_image=data, relocations=[]))

    def test_callback_errors_leave_ffi(self):
        __import__('unicorn')
        for instructions, message in [(b'\xcd\x18', 'interrupt/interface'),
                                      (b'\xb4\x04\xcd\x60', 'interrupt/interface'),
                                      (b'\xba\xa4\x00\xef', 'port/width'),
                                      (b'\xba\x6a\x00\xec', 'input port')]:
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(instructions).run(0x2576)
            self.assertEqual(stderr.getvalue(), '')

    def test_stale_terminal_and_wrong_near_cleanup_are_rejected(self):
        p = self.probe(b'\xc3')
        p.run(0x2576)
        p.uc.mem_write(p.code + 0x2576, b'\xeb\xfe')
        with self.assertRaisesRegex(ValueError, 'terminal/budget'):
            p.run(0x2576, budget=20)
        p.run(0x2576, budget=20, terminal=False)
        with self.assertRaisesRegex(ValueError, 'cleanup/callee-saved'):
            self.probe(b'\xc2\x02\x00').run(0x2576)

    def test_real_far_returns_with_write_hook_and_cleanup(self):
        p = self.probe(b'\xc3')
        p.run(0x1a3e, segment=0)
        p.run(0x110, (1, 80, 0x3402, 0x2e3f, 0x3400, 0x2e3f), segment=0xc7e)
        self.assertEqual([frame['words'] for frame in p.far_frames], [[0xff00, 0x295f]] * 2)
        p.uc.mem_write(0x2c7e0 + 0x153, b'\x0a')
        with self.assertRaisesRegex(ValueError, 'cleanup/callee-saved'):
            p.run(0x110, (1, 80, 0x3402, 0x2e3f, 0x3400, 0x2e3f), segment=0xc7e)


if __name__ == '__main__':
    unittest.main()
