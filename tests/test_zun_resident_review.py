"""Synthetic controls for resident diagnostics; no executable assets."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_zun_resident import decode, root_case, RANGES


def fixture():
    data = bytearray(5618)
    for _, start, size in RANGES:
        offset = start - 0x100
        data[offset:offset + size] = b"\x90" * size
        data[offset + size - 1] = 0xc3
    return data


class ResidentReviewTests(unittest.TestCase):
    def test_complete_synthetic_procedures(self):
        self.assertEqual(len(decode(fixture())), 13)

    def test_size_and_return_controls(self):
        with self.assertRaisesRegex(ValueError, "size"):
            decode(fixture()[:-1])
        data = fixture()
        data[0x3c7 - 0x100] = 0xcb
        with self.assertRaisesRegex(ValueError, "return"):
            decode(data)

    def test_branch_into_data(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe9" + struct.pack("<h", 0x131e - 0x36a)
        with self.assertRaisesRegex(ValueError, "data or instruction operand"):
            decode(data)

    def test_branch_into_unreviewed_runtime(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe9" + struct.pack("<h", 0x100 - 0x36a)
        with self.assertRaisesRegex(ValueError, "data or instruction operand"):
            decode(data)

    def test_call_into_interior(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe8" + struct.pack("<h", 0x3c9 - 0x36a)
        with self.assertRaisesRegex(ValueError, "interior"):
            decode(data)

    def test_indirect_call_remains_unproved(self):
        data = fixture()
        data[0x367 - 0x100:0x369 - 0x100] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_unmodeled_interrupt_is_caught_outside_ffi(self):
        __import__("unicorn")
        data = fixture()
        data[0x3c8 - 0x100:0x3ca - 0x100] = b"\xcd\x18"
        errors = io.StringIO()
        with redirect_stderr(errors):
            with self.assertRaisesRegex(ValueError, "unexpected modeled resident interrupt"):
                root_case(bytes(data))
        self.assertEqual(errors.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
