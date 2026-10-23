"""The real demo callbacks retain frame limits, exit writes and near ABI."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_demo_runtime import compare, negative_controls

TARGET = ROOT / ".analysis/targets/th03/main.exe"
CANDIDATE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/bin/th03/main.exe"


@unittest.skipUnless(TARGET.is_file() and CANDIDATE.is_file(), "private MAIN inputs absent")
class DemoCallbacks(unittest.TestCase):
    def test_boundaries_duplicate_writes_and_following_invocation(self):
        result = compare(parse_mz(TARGET.read_bytes()), parse_mz(CANDIDATE.read_bytes()))
        self.assertEqual((result["cases"], result["code_bytes_executed"]), (214, 62))
        self.assertTrue(result["equal"])

    def test_semantic_and_stack_mutations_fail(self):
        controls = negative_controls(parse_mz(TARGET.read_bytes()))
        self.assertEqual(controls["count"], 6)
        self.assertIn("input width", controls["rejected"])
        self.assertIn("no-op stack", controls["rejected"])


if __name__ == "__main__":
    unittest.main()
