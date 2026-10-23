"""Actual target/candidate round transitions and score writes, with semantic mutations."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_round_finish_runtime import compare, negative_controls

TARGET = ROOT / ".analysis/targets/th03/main.exe"
CANDIDATE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/bin/th03/main.exe"


@unittest.skipUnless(
    TARGET.is_file() and CANDIDATE.is_file(), "private MAIN inputs absent"
)
class RoundFinishRuntime(unittest.TestCase):
    def test_complete_bodies_all_score_bytes_and_round_id_wrap(self):
        result = compare(
            parse_mz(TARGET.read_bytes()), parse_mz(CANDIDATE.read_bytes())
        )
        self.assertEqual(result["by_function"], {"next": 256, "score": 512})
        self.assertEqual(result["code_bytes_executed"], 177)
        self.assertTrue(result["equal"])

    def test_semantic_and_stack_cleanup_mutations_are_rejected(self):
        result = negative_controls(parse_mz(TARGET.read_bytes()))
        self.assertEqual(result["count"], 5)
        self.assertIn("missing score digit", result["rejected"])
        self.assertIn("Pascal cleanup", result["rejected"])


if __name__ == "__main__":
    unittest.main()
