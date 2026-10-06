"""Synthetic controls for the complete STAFF boundary and foreign-call model."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_staff import CS, DS, RANGES, decode, Probe


def fixture():
    image = bytearray(DS * 16 + 0xb62)
    for _, start, size, cleanup in RANGES:
        position = CS * 16 + start
        image[position:position + size] = b"\x90" * size
        terminal = b"\xc2\x06\x00" if cleanup else b"\xc3"
        image[position + size - len(terminal):position + size] = terminal
    return image


class StaffReviewTests(unittest.TestCase):
    def test_complete_synthetic_partition(self):
        self.assertEqual(sum(row["size"] for row in decode(fixture())), 424)

    def test_incomplete_or_wrong_return(self):
        data = fixture()
        with self.assertRaisesRegex(ValueError, "body/near-return"):
            decode(data[:CS * 16 + 0x24e5])
        data[CS * 16 + 0x24e3:CS * 16 + 0x24e6] = b"\x90\x90\xc3"
        with self.assertRaisesRegex(ValueError, "cleanup"):
            decode(data)

    def test_branch_into_operand_or_other_body(self):
        for destination in (0x233f, 0x2382, 0x24e6):
            data = fixture()
            data[CS * 16 + 0x233e:CS * 16 + 0x2341] = b"\xe9" + struct.pack("<h", destination - 0x2341)
            with self.assertRaisesRegex(ValueError, "data or instruction operand"):
                decode(data)

    def test_unknown_call_is_rejected(self):
        data = fixture()
        data[CS * 16 + 0x233e:CS * 16 + 0x2341] = b"\xe8\x00\x00"
        with self.assertRaisesRegex(ValueError, "explicit reviewed interface"):
            decode(data)

    def test_import_near_far_mismatch_is_rejected(self):
        data = fixture()
        at = CS * 16 + 0x233e
        data[at:at + 5] = b"\x9a" + struct.pack("<HH", 0xb3e, CS)
        with self.assertRaisesRegex(ValueError, "near/far ABI"):
            decode(data)

    def test_indirect_edge_is_rejected(self):
        data = fixture()
        at = CS * 16 + 0x233e
        data[at:at + 2] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_callback_failure_is_raised_outside_ffi(self):
        __import__("unicorn")
        for code, error in [(b"\xcd\x18", "kernel interrupt"),
                            (b"\xba\xa4\x00\xef", "port/width")]:
            data = fixture()
            at = CS * 16 + 0x233e
            data[at:at + len(code)] = code
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, error):
                    Probe(SimpleNamespace(program_image=data, relocations=[])).run(0x233e)
            self.assertEqual(stderr.getvalue(), "")

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_wrong_runtime_pascal_cleanup_is_rejected(self):
        data = fixture()
        data[CS * 16 + 0x24e3:CS * 16 + 0x24e6] = b"\x90\x90\xc3"
        with self.assertRaisesRegex(ValueError, "stack/callee-saved"):
            Probe(SimpleNamespace(program_image=data, relocations=[])).run(0x249a, (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
