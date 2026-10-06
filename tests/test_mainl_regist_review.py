"""Synthetic controls for registration ownership and bounded CPU interfaces."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_regist import CS, DS, RANGES, RegistrationProbe, decode


def fixture():
    data = bytearray(DS * 16 + 0x2800)
    for _, start, size, cleanup in RANGES:
        at = CS * 16 + start
        data[at:at + size] = b"\x90" * size
        terminal = b"\xc2" + struct.pack("<H", int(cleanup)) if cleanup else b"\xc3"
        data[at + size - len(terminal):at + size] = terminal
    return data


class RegistrationBoundaryTests(unittest.TestCase):
    def test_wrong_cleanup_and_truncation_are_rejected(self):
        data = fixture()
        data[CS * 16 + 0x18fe] = 4
        with self.assertRaisesRegex(ValueError, "complete body/near cleanup"):
            decode(data)
        with self.assertRaisesRegex(ValueError, "complete body/near cleanup"):
            decode(fixture()[:CS * 16 + 0x233d])

    def test_branch_cannot_enter_another_body_or_operand(self):
        for target in (0x17f5, 0x17ba):
            data = fixture()
            at = CS * 16 + 0x17b9
            data[at:at + 3] = b"\xe9" + struct.pack("<h", target - 0x17bc)
            with self.assertRaisesRegex(ValueError, "branch enters"):
                decode(data)

    def test_call_cannot_enter_an_interior_or_unknown_interface(self):
        for instructions, message in [(b"\xe8\x3a\x00", "near call enters"),
                                      (b"\x9a\xff\xff\x00\x00", "unknown foreign"),
                                      (b"\xff\xd0", "indirect")]:
            data = fixture()
            at = CS * 16 + 0x17b9
            data[at:at + len(instructions)] = instructions
            with self.assertRaisesRegex(ValueError, message):
                decode(data)


@unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
class RegistrationRuntimeTests(unittest.TestCase):
    def probe(self, instructions):
        __import__("unicorn")
        data = fixture()
        at = CS * 16 + 0x17b9
        data[at:at + len(instructions)] = instructions
        return RegistrationProbe(SimpleNamespace(program_image=data, relocations=[]))

    def test_callback_errors_leave_ffi(self):
        for instructions, message in [(b"\xcd\x18", "interrupt"),
                                      (b"\xba\xa4\x00\xef", "port/width"),
                                      (b"\xba\x6a\x00\xec", "input port")]:
            output = io.StringIO()
            with redirect_stderr(output):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(instructions).run(0x17b9)
            self.assertEqual(output.getvalue(), "")

    def test_stale_terminal_flag_and_budget_are_rejected(self):
        p = self.probe(b"\xc3")
        p.run(0x17b9)
        p.uc.mem_write(p.code + 0x17b9, b"\xeb\xfe")
        with self.assertRaisesRegex(ValueError, "terminal/budget"):
            p.run(0x17b9, budget=20)
        p.run(0x17b9, budget=20, terminal=False)

    def test_actual_near_cleanup_is_checked(self):
        with self.assertRaisesRegex(ValueError, "cleanup/callee-saved"):
            self.probe(b"\xc2\x02\x00").run(0x17b9)

    def test_struct_copy_model_rejects_wrong_count(self):
        # Four zero argument words, CX=7, and a real far call to the modeled helper.
        instructions = b"\x31\xc0\x50\x50\x50\x50\xb9\x07\x00\x9a\x6c\x30\x00\x20\xc3"
        with self.assertRaisesRegex(ValueError, "struct-copy count"):
            self.probe(instructions).run(0x17b9)


if __name__ == "__main__":
    unittest.main()
