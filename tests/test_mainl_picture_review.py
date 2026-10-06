"""Negative controls for direct helper ownership, packed tables and CPU scopes."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_picture import HELPERS, DS, PictureProbe, helper_analysis, far_return_engine_control
from test_mainl_cutscene_review import fixture, CS


def helper_fixture():
    data = fixture()
    for _, start, size, cleanup in HELPERS:
        data[start:start + size] = b"\x90" * size
        terminal = b"\xca\x0a\x00" if cleanup else b"\xcb"
        data[start + size - len(terminal):start + size] = terminal
    for byte in range(256):
        value = sum(((((byte & 15) >> p) & 1) | ((((byte >> 4) >> p) & 1) << 1)) << (p * 8) for p in range(4))
        struct.pack_into("<I", data, 0x1aaa + byte * 4, value)
    struct.pack_into("<H", data, DS * 16 + 0x52e, 0xa800)
    for at in (0x739,0x759,0x785):
        data[at] = 0x90
    return data


class PictureBoundaryTests(unittest.TestCase):
    def test_changed_far_cleanup_is_rejected(self):
        data = helper_fixture()
        data[0x2d30] = 8
        with self.assertRaisesRegex(ValueError, "far cleanup"):
            helper_analysis(data)

    def test_shared_tail_does_not_authorize_neighboring_body(self):
        data = helper_fixture()
        data[0x2c6e:0x2c71] = b"\xe9" + struct.pack("<h", 0x2c64 - 0x2c71)
        with self.assertRaisesRegex(ValueError, "leaves body/shared return tail"):
            helper_analysis(data)

    def test_changed_rotation_table_and_clip_segment_are_rejected(self):
        for at in (0x1aaa + 19, DS * 16 + 0x52e):
            data = helper_fixture()
            data[at] ^= 1
            with self.assertRaisesRegex(ValueError, "rotation table/initial clipping"):
                helper_analysis(data)

    def test_observed_even_byte_cannot_be_silently_reclassified(self):
        data = helper_fixture()
        data[0x759] = 0
        with self.assertRaisesRegex(ValueError, "EVEN bytes"):
            helper_analysis(data)


@unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
class PictureRuntimeTests(unittest.TestCase):
    def probe(self, instructions):
        __import__("unicorn")
        data = helper_fixture()
        at = CS * 16 + 0xba3
        data[at:at + len(instructions)] = instructions
        return PictureProbe(SimpleNamespace(program_image=data, relocations=[]))

    def test_callback_errors_leave_ffi(self):
        for instructions, message in [(b"\xcd\x18", "interrupt"),
                                      (b"\xba\xa4\x00\xef", "port/width"),
                                      (b"\xba\x6a\x00\xec", "input port")]:
            p = self.probe(instructions)
            output = io.StringIO()
            with redirect_stderr(output):
                with self.assertRaisesRegex(ValueError, message):
                    p.run(0xba3)
            self.assertEqual(output.getvalue(), "")

    def test_budget_and_stale_terminal_sentinels_are_rejected(self):
        p = self.probe(b"\xc3")
        p.run(0xba3)
        p.uc.mem_write(p.code + 0xba3, b"\xeb\xfe")
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            p.run(0xba3, budget=20)

    def test_return_transition_model_requires_actual_opcode(self):
        p = self.probe(b"\x9a\x24\x07\x00\x20")
        p.uc.mem_write(0x20738, b"\x90")
        with self.assertRaisesRegex(ValueError, "far-return opcode"):
            p.run(0xba3)

    def test_synthetic_engine_return_control(self):
        result = far_return_engine_control()
        self.assertEqual([o["far_return_frames"] for o in result], [[[5, 0x295f]], [[5, 0x295f]]])
        self.assertEqual([o["returned_correctly"] for o in result], [True, False])


if __name__ == "__main__":
    unittest.main()
