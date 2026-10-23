"""Actual initializer contracts; incomplete relocation order earns no exact credit."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_round_init_runtime import compare, negative_controls

TARGET = ROOT / ".analysis/targets/th03/main.exe"
CANDIDATE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/bin/th03/main.exe"


@unittest.skipUnless(
    TARGET.is_file() and CANDIDATE.is_file(), "private MAIN inputs absent"
)
class RoundInitializer(unittest.TestCase):
    def test_rank_wrap_clamp_and_preserved_storage(self):
        result = compare(
            parse_mz(TARGET.read_bytes()), parse_mz(CANDIDATE.read_bytes())
        )
        self.assertEqual(result["cases"], 240)
        self.assertEqual(result["code_bytes_executed"], 855)
        self.assertTrue(result["equal"])

    def test_six_semantic_mutations_are_rejected(self):
        result = negative_controls(parse_mz(TARGET.read_bytes()))
        self.assertEqual(result["count"], 6)
        self.assertIn("effect stride", result["rejected"])
        self.assertIn("easy divisor", result["rejected"])


if __name__ == "__main__":
    unittest.main()
