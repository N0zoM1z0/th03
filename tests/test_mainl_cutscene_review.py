"""Synthetic controls for cutscene code/data partitions and bounded CPU hooks."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_cutscene import CS, DS, RANGES, decode, Probe


def fixture():
    data = bytearray(DS * 16 + 0x2800)
    for _, start, size, cleanup in RANGES:
        at = CS * 16 + start
        data[at:at + size] = b"\x90" * size
        terminal = b"\xc2" + struct.pack("<H", int(cleanup)) if cleanup else b"\xc3"
        data[at + size - len(terminal):at + size] = terminal
    at = CS * 16 + 0x108c
    data[at:at + 4] = b"\x2e\xff\x67\x20"
    at = CS * 16 + 0x112a
    data[at:at + 5] = b"\x2e\xff\xa7\x36\x16"
    struct.pack_into("<4H", data, CS * 16 + 0x1636, 0x1130, 0x1131, 0x1132, 0x1133)
    struct.pack_into("<16H", data, CS * 16 + 0x163e, *b"$=@bcefgkmnpstvw")
    struct.pack_into("<16H", data, CS * 16 + 0x165e, *range(0x1090, 0x10a0))
    return data


class CutsceneReviewTests(unittest.TestCase):
    def test_complete_synthetic_partition(self):
        result = decode(fixture())
        self.assertEqual(len(result["functions"]), 13)
        self.assertEqual(sum(row["size"] for row in result["functions"]), 3122)
        self.assertEqual(result["tables"]["data_size"], 72)

    def test_truncated_or_wrong_cleanup(self):
        data = fixture()
        with self.assertRaisesRegex(ValueError, "boundary"):
            decode(data[:CS * 16 + 0x17b8])
        data[CS * 16 + 0xb82] = 2
        with self.assertRaisesRegex(ValueError, "cleanup"):
            decode(data)

    def test_switch_target_into_data_or_operand(self):
        for table, target in [(0x1636, 0x1636), (0x165e, 0x108d)]:
            data = fixture()
            struct.pack_into("<H", data, CS * 16 + table, target)
            with self.assertRaisesRegex(ValueError, "table enters data or instruction operand"):
                decode(data)

    def test_catalog_and_alignment_controls(self):
        data = fixture()
        data[CS * 16 + 0x163e] = ord("A")
        with self.assertRaisesRegex(ValueError, "catalogue"):
            decode(data)
        data = fixture()
        data[CS * 16 + 0x1635] = 0x90
        with self.assertRaisesRegex(ValueError, "alignment"):
            decode(data)

    def test_direct_edge_into_another_body(self):
        data = fixture()
        at = CS * 16 + 0xb3e
        data[at:at + 3] = b"\xe9" + struct.pack("<h", 0xb84 - 0xb41)
        with self.assertRaisesRegex(ValueError, "another body"):
            decode(data)

    def test_near_call_into_interior(self):
        data = fixture()
        at = CS * 16 + 0xb3e
        data[at:at + 3] = b"\xe8" + struct.pack("<h", 0xb85 - 0xb41)
        with self.assertRaisesRegex(ValueError, "body interior"):
            decode(data)

    def test_unknown_far_call(self):
        data = fixture()
        at = CS * 16 + 0xb3e
        data[at:at + 5] = b"\x9a\xff\xff\x00\x00"
        with self.assertRaisesRegex(ValueError, "unreviewed interface"):
            decode(data)

    def test_other_indirect_edge(self):
        data = fixture()
        at = CS * 16 + 0xb3e
        data[at:at + 2] = b"\xff\xd0"
        with self.assertRaisesRegex(ValueError, "indirect"):
            decode(data)

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_callback_failures_are_raised_outside_ffi(self):
        __import__("unicorn")
        for instructions, message in [(b"\xcd\x18", "kernel interrupt"),
                                      (b"\xba\xa6\x00\xef", "port/width"),
                                      (b"\xba\xa6\x00\xec", "input port")]:
            data = fixture()
            at = CS * 16 + 0xb3e
            data[at:at + len(instructions)] = instructions
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    Probe(SimpleNamespace(program_image=data, relocations=[])).run(0xb3e, (0, 0))
            self.assertEqual(stderr.getvalue(), "")

    @unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
    def test_wrong_runtime_cleanup(self):
        data = fixture()
        data[CS * 16 + 0xb82] = 2
        with self.assertRaisesRegex(ValueError, "stack/callee-saved"):
            Probe(SimpleNamespace(program_image=data, relocations=[])).run(0xb3e, (0, 0))


if __name__ == "__main__":
    unittest.main()
