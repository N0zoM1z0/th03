"""A passing summary cannot replace proof of two complete cold output vectors."""

from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from review_th03_main_native_units import review


@unittest.skipUnless(
    (ROOT / ".analysis/work/main-build.json").is_file(),
    "current native cold report absent",
)
class NativeUnitReview(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / ".analysis/work/main-build.json").read_text())
        if not self.report.get("cold_reproducibility", {}).get("complete"):
            self.skipTest("two current cold source builds are unavailable")

    def test_mixed_build_cannot_borrow_a_passing_cold_pair(self):
        bad = copy.deepcopy(self.report)
        bad["cold_build"] = False
        with self.assertRaisesRegex(ValueError, "two cold source materializations"):
            review(bad)

    def test_true_summary_cannot_hide_a_missing_output(self):
        bad = copy.deepcopy(self.report)
        bad["cold_reproducibility"]["raw_output_repeat"].pop("obj/th03/ex_ellen.obj")
        self.assertTrue(bad["cold_reproducibility"]["complete"])
        with self.assertRaisesRegex(ValueError, "complete cold output vector"):
            review(bad)


if __name__ == "__main__":
    unittest.main()
