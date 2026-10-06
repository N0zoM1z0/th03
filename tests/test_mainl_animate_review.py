"""Negative controls for interpreter CPU/model terminal observations."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_mainl_animate import AnimateProbe
from test_mainl_cutscene_review import fixture, CS


@unittest.skipUnless(find_spec("unicorn"), "optional private Unicorn runtime is unavailable")
class AnimateReviewTests(unittest.TestCase):
    def probe(self, instructions, **kwargs):
        __import__("unicorn")
        data = fixture()
        at = CS * 16 + 0x167e
        data[at:at + len(instructions)] = instructions
        return AnimateProbe(SimpleNamespace(program_image=data, relocations=[]), **kwargs)

    def test_budget_exhaustion_cannot_pass_as_terminal(self):
        with self.assertRaisesRegex(ValueError, "terminal contract"):
            self.probe(b"\xeb\xfe").execute(b"\\$", budget=20)

    def test_nonterminal_requires_no_return(self):
        with self.assertRaisesRegex(ValueError, "terminal contract"):
            self.probe(b"\xc3").execute(b"AB", expect_terminal=False)

    def test_terminal_sentinel_is_reset_for_reuse(self):
        p = self.probe(b"\xc3")
        p.execute(b"\\$")
        p.uc.mem_write(p.code + 0x167e, b"\xeb\xfe")
        with self.assertRaisesRegex(ValueError, "terminal contract"):
            p.execute(b"\\$", budget=20)

    def test_substituted_delay_stop_is_not_budget_observation(self):
        # Physically relocated direct frame_delay entry with one stack word.
        with self.assertRaisesRegex(ValueError, "substituted delay stopped"):
            self.probe(b"\x6a\x01\x9a\x72\x03\x7e\x2c\xc3", frame_limit=1).execute(b"AB", expect_terminal=False)

    def test_callback_failures_leave_ffi(self):
        for instructions, message in [(b"\xcd\x18", "kernel interrupt"),
                                      (b"\xba\xa6\x00\xef", "port/width"),
                                      (b"\xba\xa6\x00\xec", "input port")]:
            p = self.probe(instructions)
            output = io.StringIO()
            with redirect_stderr(output):
                with self.assertRaisesRegex(ValueError, message):
                    p.execute(b"\\$")
            self.assertEqual(output.getvalue(), "")

    def test_interface_segment_alias_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "segment alias"):
            self.probe(b"\x9a\xb2\x0d\x7f\x2c").execute(b"\\$")

    def test_input_model_rejects_invalid_constructed_words(self):
        for keys in ((), (-1,), (65536,)):
            with self.assertRaisesRegex(ValueError, "input sequence"):
                self.probe(b"\xc3", keys=keys)


if __name__ == "__main__":
    unittest.main()
