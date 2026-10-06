"""Synthetic boundary and callback controls; no game bytes are embedded."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_ongchk import decode, runtime_case, RANGES


def fixture():
    data = bytearray(926)
    for _, start, size, terminal in RANGES:
        offset = start - 0x100
        data[offset:offset + size] = b"\x90" * size
        if terminal == "ret":
            data[offset + size - 1] = 0xc3
        elif terminal == "jmp":
            position = start + size - 3
            data[position - 0x100:position - 0x100 + 3] = b"\xe9" + struct.pack("<h", 0x2c2 - position - 3)
        else:
            data[offset + size - 2:offset + size] = b"\xcd\x21"
    return data


class OngchkReviewTests(unittest.TestCase):
    def test_complete_regions_and_data_exclusion(self):
        data = fixture()
        data[892:] = b"\xff" * 34  # initialized data is never decoded as instructions
        rows = decode(data)
        self.assertEqual(sum(row["size"] for row in rows), 892)
        self.assertEqual(len(rows), 12)

    def test_size_and_terminal_controls(self):
        with self.assertRaisesRegex(ValueError, "size"):
            decode(fixture()[:-1])
        data = fixture()
        data[0x47b - 0x100] = 0x90
        with self.assertRaisesRegex(ValueError, "terminal"):
            decode(data)
        data = fixture()
        data[0x126 - 0x100] = 0x18
        with self.assertRaisesRegex(ValueError, "termination"):
            decode(data)

    def test_branch_into_data_or_operand(self):
        for destination in (0x47c, 0x101):
            data = fixture()
            data[:3] = b"\xe9" + struct.pack("<h", destination - 0x103)
            with self.assertRaisesRegex(ValueError, "data or instruction operand"):
                decode(data)

    def test_call_into_shared_tail_is_rejected(self):
        data = fixture()
        data[:3] = b"\xe8" + struct.pack("<h", 0x2c2 - 0x103)
        with self.assertRaisesRegex(ValueError, "unreviewed entry/shared tail"):
            decode(data)

    def test_indirect_edge_is_rejected(self):
        data = fixture()
        data[:2] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_callback_errors_are_raised_outside_ffi(self):
        __import__("unicorn")
        for code, error in [(b"\xcd\x18", "DOS interrupt"),
                            (b"\xba\x60\xa4\xef", "port width")]:
            data = fixture()
            data[:len(code)] = code
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, error):
                    runtime_case(bytes(data))
            self.assertEqual(stderr.getvalue(), "")

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_budget_stop_is_explicitly_nonterminal(self):
        data = fixture()
        data[:2] = b"\xeb\xfe"
        result = runtime_case(bytes(data), instruction_budget=42)
        self.assertEqual(result["stop"], dict(kind="instruction-budget", ip=0x100))
        self.assertEqual(result["steps"], 42)


if __name__ == "__main__":
    unittest.main()
