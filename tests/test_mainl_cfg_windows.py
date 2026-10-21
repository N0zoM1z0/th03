"""Actual MAINL CFG/window CPU contracts and deliberate behavior/ABI corruption."""
import dataclasses
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from review_th03_mainl_cfg_windows import (
    CS, RANGES, analyze, cfg_case, matrix, text_case, window_case,
)

ORIGINAL = ".analysis/th03-diet/sol-diet-restoration-20261006-b/mainl.exe"
def mutated(mz, offset, value):
    image = bytearray(mz.program_image)
    image[CS * 16 + offset:CS * 16 + offset + len(value)] = value
    return dataclasses.replace(mz, program_image=bytes(image))

NEGATIVES=[
 ('cfg_wrong_return',0x2f,b'\x31\xc0',lambda m:cfg_case(m,0x5678,8,0)),
 ('cfg_wrong_pointer_write',0x27,b'\xed',lambda m:cfg_case(m,0x5678,8,0)),
 ('cfg_far_return',0x33,b'\xcb',lambda m:cfg_case(m,0x5678,8,0)),
 ('winner_palette_bit',0xe2,b'\x00',lambda m:window_case(m,17,0,0,6)),
 ('decisive_message',0x89,b'\x08',lambda m:window_case(m,17,0,0,6)),
 ('missing_nul',0x126,b'\x01',lambda m:window_case(m,17,0,0,6)),
 ('wrong_text_pointer',0x15b,b'\x3d',lambda m:text_case(m,0,0x202)),
 ('wrong_text_geometry',0x154,b'\x11',lambda m:text_case(m,0,0x202)),
 ('win_far_return',0x14d,b'\xcb',lambda m:window_case(m,17,0,0,6))]

class MainlCfgWindowsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The original decoded image is retained ignored evidence, not a fixture
        # redistributed in source. Explicit overrides allow installed candidates.
        path = Path(os.environ.get("TH03_MAINL_CFG_TEST_EXE", str(ROOT / ORIGINAL)))
        if not path.is_file():
            raise unittest.SkipTest("MAINL decoded model input is not present")
        cls.mz = parse_mz(path.read_bytes())
        if not cls.mz.valid:
            raise ValueError("invalid MAINL MZ input")

    def test_complete_scope_and_489_scenarios(self):
        self.assertEqual(RANGES, [(3, 49), (0x34, 282), (0x14e, 56)])
        analysis = analyze(self.mz.program_image)
        self.assertEqual(sum(row["size"] for row in analysis), 387)
        rows = matrix(self.mz)
        self.assertEqual(len(rows), 489)
        self.assertEqual(sum(len(row["events"]) for row in rows), 4723)
        self.assertEqual(
            {kind: sum(row["kind"] == kind for row in rows)
             for kind in ("cfg", "window", "text")},
            {"cfg": 76, "window": 407, "text": 6},
        )

    def test_nine_real_cpu_negative_controls(self):
        self.assertEqual(len(NEGATIVES), 9)
        for name, offset, value, case in NEGATIVES:
            with self.subTest(name=name):
                before = self.mz.program_image[CS * 16 + offset:CS * 16 + offset + len(value)]
                self.assertNotEqual(before, value, "negative control must change bytes")
                with self.assertRaises((AssertionError, ValueError)):
                    case(mutated(self.mz, offset, value))

if __name__ == "__main__":
    unittest.main()
