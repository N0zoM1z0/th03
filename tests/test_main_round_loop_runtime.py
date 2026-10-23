"""Round-loop behavior is checked independently of target/candidate equality."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_round_loop_runtime import compare, negative_controls

TARGET = ROOT / ".analysis/targets/th03/main.exe"
CANDIDATE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/bin/th03/main.exe"


@unittest.skipUnless(TARGET.is_file() and CANDIDATE.is_file(), "private MAIN inputs absent")
class RoundLoopRuntime(unittest.TestCase):
    def test_all_loop_bytes_exits_callbacks_timing_and_counter_boundaries(self):
        result = compare(parse_mz(TARGET.read_bytes()), parse_mz(CANDIDATE.read_bytes()))
        self.assertEqual(result["cases"], 240)
        self.assertEqual(result["code_bytes_executed"], 862)
        self.assertTrue(result["equal"])

    def test_independent_contract_rejects_semantic_and_memory_mutations(self):
        result = negative_controls(parse_mz(TARGET.read_bytes()))
        self.assertEqual(result["count"], 8)
        self.assertIn("counter width", result["rejected"])
        self.assertIn("unrelated store", result["rejected"])


if __name__ == "__main__":
    unittest.main()
