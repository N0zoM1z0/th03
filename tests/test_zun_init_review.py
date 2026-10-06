"""Synthetic negative controls for initializer byte and model boundaries."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_zun_init import decode, runtime_case, RANGES


def fixture():
    # Synthetic procedures and data; contains no game instructions or strings.
    data = bytearray(1390)
    for _, start, size, terminal in RANGES:
        offset = start - 0x100
        data[offset:offset + size] = b"\x90" * size
        if terminal in ("ret", "iret"):
            data[offset + size - 1] = 0xc3 if terminal == "ret" else 0xcf
        elif terminal == "jmp":
            data[offset:offset + 3] = b"\xe9" + struct.pack("<h", 0x43a - start - 3)
        else:
            data[offset + size - 2:offset + size] = b"\xcd\x21"
    return data


class InitializerReviewTests(unittest.TestCase):
    def test_complete_synthetic_decode(self):
        self.assertEqual(len(decode(fixture())), 9)

    def test_size_and_terminal_mutations(self):
        with self.assertRaisesRegex(ValueError, "size"):
            decode(fixture()[:-1])
        data = fixture()
        data[0x135 - 0x100] = 0xc3
        with self.assertRaisesRegex(ValueError, "terminal"):
            decode(data)
        data = fixture()
        data[0x534 - 0x100] = 0x18
        with self.assertRaisesRegex(ValueError, "termination"):
            decode(data)

    def test_branch_into_data(self):
        data = fixture()
        data[3:6] = b"\xe9" + struct.pack("<h", 0x23d - 0x106)
        with self.assertRaisesRegex(ValueError, "data or instruction operand"):
            decode(data)

    def test_call_into_interior(self):
        data = fixture()
        data[3:6] = b"\xe8" + struct.pack("<h", 0x137 - 0x106)
        with self.assertRaisesRegex(ValueError, "interior"):
            decode(data)

    def test_indirect_edge_is_not_silently_proved(self):
        data = fixture()
        data[3:5] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_unknown_interrupt_is_caught_outside_ffi(self):
        __import__("unicorn")  # library import warnings precede callback capture
        data = fixture()
        data[0x43a - 0x100:0x43c - 0x100] = b"\xcd\x18"
        errors = io.StringIO()
        with redirect_stderr(errors):
            with self.assertRaisesRegex(ValueError, "unexpected kernel interrupt"):
                runtime_case(bytes(data), "", False)
        self.assertEqual(errors.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
