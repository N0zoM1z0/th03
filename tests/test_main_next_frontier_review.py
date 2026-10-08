"""Negative controls for MAIN target-only candidate intervals."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from review_th03_main_next_frontier import observe_candidate


class NextFrontierTests(unittest.TestCase):
    def test_complete_instruction_and_terminal_are_required(self):
        image=SimpleNamespace(valid=True,program_image=b"\x90\xc3\x90\xcb",relocations=[])
        row=observe_candidate(image,dict(id="test",start=0,end=2,terminal="ret",subsystem="test",caution="none"))
        self.assertEqual(row["size"],2)
        self.assertFalse(row["code_exact"])
        self.assertFalse(row["owner_partition_accepted"])
        with self.assertRaises(ValueError):
            observe_candidate(image,dict(id="test",start=0,end=2,terminal="retf",subsystem="test",caution="none"))

    def test_incomplete_decode_and_crossing_relocation_fail(self):
        image=SimpleNamespace(valid=True,program_image=b"\xe8\xc3",relocations=[])
        with self.assertRaises(ValueError):
            observe_candidate(image,dict(id="test",start=0,end=1,terminal="ret",subsystem="test",caution="none"))
        crossing=SimpleNamespace(valid=True,program_image=b"\x90\xc3",relocations=[SimpleNamespace(linear=1)])
        with self.assertRaises(ValueError):
            observe_candidate(crossing,dict(id="test",start=0,end=2,terminal="ret",subsystem="test",caution="none"))

    def test_missing_image_or_truncated_span_fail(self):
        image=SimpleNamespace(valid=False,program_image=b"\x90\xc3",relocations=[])
        with self.assertRaises(ValueError):
            observe_candidate(image,dict(id="test",start=0,end=2,terminal="ret",subsystem="test",caution="none"))
        image.valid=True
        with self.assertRaises(ValueError):
            observe_candidate(image,dict(id="test",start=0,end=3,terminal="ret",subsystem="test",caution="none"))
