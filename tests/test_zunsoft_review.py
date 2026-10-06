"""Synthetic controls for logo root and substituted interface boundaries."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_zunsoft import decode, Probe, RANGES


def fixture():
    data = bytearray(10096)
    for name, start, size in RANGES:
        offset = start - 0x100
        data[offset:offset + size] = b"\x90" * size
        if name == "zunsoft_vector2":
            data[offset + size - 3:offset + size] = b"\xc2\x08\0"
        else:
            data[offset + size - 1] = 0xc3
    return data


class LogoReviewTests(unittest.TestCase):
    def test_complete_synthetic_root(self):
        self.assertEqual(sum(r["size"] for r in decode(fixture())), 1299)

    def test_size_return_and_cleanup_controls(self):
        with self.assertRaisesRegex(ValueError, "size"):
            decode(fixture()[:-1])
        data = fixture()
        data[0x383 - 0x100] = 0xcb
        with self.assertRaisesRegex(ValueError, "return"):
            decode(data)
        data = fixture()
        data[0x437 - 0x100] = 6
        with self.assertRaisesRegex(ValueError, "cleanup"):
            decode(data)

    def test_branch_into_data(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe9" + struct.pack("<h", 0x21ce - 0x36a)
        with self.assertRaisesRegex(ValueError, "data or instruction operand"):
            decode(data)

    def test_call_into_interior(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe8" + struct.pack("<h", 0x385 - 0x36a)
        with self.assertRaisesRegex(ValueError, "bounded entry"):
            decode(data)

    def test_explicit_import_is_a_distinct_edge(self):
        data = fixture()
        data[0x367 - 0x100:0x36a - 0x100] = b"\xe8" + struct.pack("<h", 0x928 - 0x36a)
        self.assertEqual(decode(data)[0]["edges"][0]["target"], 0x928)
        data[0x367 - 0x100:0x369 - 0x100] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_unmodeled_interrupt_is_caught_outside_ffi(self):
        __import__("unicorn")
        data = fixture()
        data[0x367 - 0x100:0x369 - 0x100] = b"\xcd\x21"
        errors = io.StringIO()
        with redirect_stderr(errors):
            with self.assertRaisesRegex(ValueError, "unmodeled logo interrupt"):
                Probe(bytes(data)).call(0x367)
        self.assertEqual(errors.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
