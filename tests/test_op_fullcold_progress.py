"""Cold-build annotations must not create an acceptance claim."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import progress

class ColdProgress(unittest.TestCase):
    def rows(self):
        return [dict(id=k, artifact="th03-op", oracle="analysis-bundle", result="pass",
                     unit_id="", extent_start="", extent_size="", output_sha256=v)
                for k, v in progress.OP_FULLCOLD_EVIDENCE.items()]

    def test_retained_pair(self):
        self.assertTrue(progress.op_fullcold_retained(self.rows()))

    def test_missing(self):
        self.assertFalse(progress.op_fullcold_retained(self.rows()[:1]))

    def test_duplicate(self):
        rows = self.rows()
        self.assertFalse(progress.op_fullcold_retained(rows + [rows[0]]))

    def test_wrong_digest(self):
        rows = self.rows()
        rows[0]["output_sha256"] = "0" * 64
        self.assertFalse(progress.op_fullcold_retained(rows))

    def test_wrong_scope_or_result(self):
        for key, value in [("artifact", "th03-mainl"), ("oracle", "raw-bytes"),
                           ("result", "fail"), ("extent_start", "0"),
                           ("extent_size", "9530"), ("unit_id", "invented")]:
            with self.subTest(key=key):
                rows = self.rows()
                rows[0][key] = value
                self.assertFalse(progress.op_fullcold_retained(rows))

if __name__ == "__main__":
    unittest.main()
