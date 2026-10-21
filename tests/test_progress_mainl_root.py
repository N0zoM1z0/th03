import csv
from pathlib import Path
import unittest
import progress
ROOT = Path(__file__).resolve().parents[1]
class RootProgressTests(unittest.TestCase):
    def data(self):
        rows = []
        for p in ("config/units.csv", "config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_root_earned_counts_and_caption(self):
        units, evidence = self.data()
        self.assertTrue(progress.mainl_root_source_proven(units, evidence))
        c = progress.mainl_unit_progress(units)
        self.assertEqual((c["source"],c["source_bytes"],c["exact"],c["total"]),(50,15672,0,145))
        self.assertIn("composed 11,971 B target-equal",progress.render_svg(units,[],evidence))
    def test_missing_root_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        evidence=[e for e in evidence if e["id"] != progress.MAINL_ROOT_SOURCE_EVIDENCE[-1]]
        self.assertFalse(progress.mainl_root_source_proven(units,evidence))
