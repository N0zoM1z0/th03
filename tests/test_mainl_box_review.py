"""Negative controls for bounded CPU execution and planar transfer observations."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_box import BoxProbe, expect_copy
from test_mainl_cutscene_review import fixture, CS


@unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
class BoxReviewTests(unittest.TestCase):
    def probe(self, instructions):
        __import__("unicorn")
        data = fixture()
        at = CS * 16 + 0xe4c
        data[at:at + len(instructions)] = instructions
        return BoxProbe(SimpleNamespace(program_image=data, relocations=[]))

    def test_budget_exhaustion_is_not_a_terminal_pass(self):
        with self.assertRaisesRegex(ValueError, "instruction budget"):
            self.probe(b"\xeb\xfe").run(0xe4c, budget=20)

    def test_return_sentinel_is_reset_between_calls(self):
        p = self.probe(b"\xc3")
        p.run(0xe4c)
        p.uc.mem_write(p.code + 0xe4c, b"\xeb\xfe")
        with self.assertRaisesRegex(ValueError, "instruction budget"):
            p.run(0xe4c, budget=20)

    def test_callback_failures_leave_ffi(self):
        for instructions, message in [(b"\xcd\x18", "kernel interrupt"),
                                      (b"\xba\xa6\x00\xef", "port/width"),
                                      (b"\xba\xa6\x00\xec", "input port")]:
            p = self.probe(instructions)
            output = io.StringIO()
            with redirect_stderr(output):
                with self.assertRaisesRegex(ValueError, message):
                    p.run(0xe4c)
            self.assertEqual(output.getvalue(), "")

    def test_interface_segment_alias_is_rejected(self):
        # 2001:219E physically aliases the true allocator entry 2000:21AE.
        with self.assertRaisesRegex(ValueError, "segment alias"):
            self.probe(b"\x9a\x9e\x21\x01\x20").run(0xe4c)

    def test_missing_or_reordered_word_transfers_are_rejected(self):
        for accesses in ([], [["write", 0x60000, 2], ["read", 0xae40a, 2]]):
            with self.assertRaisesRegex(ValueError, "ordered word/plane/offset"):
                expect_copy(SimpleNamespace(accesses=accesses), snapshot=True, segment=0x6000)


if __name__ == "__main__":
    unittest.main()
