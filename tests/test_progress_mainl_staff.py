import copy
import csv
from pathlib import Path
import unittest
import progress
ROOT = Path(__file__).resolve().parents[1]
class StaffProgressTests(unittest.TestCase):
    def data(self):
        result = []
        for p in ("config/units.csv", "config/evidence.csv"):
            with (ROOT / p).open() as stream:
                result.append(list(csv.DictReader(stream)))
        return result
    def test_earned_existing_partition_counts(self):
        units, evidence = self.data()
        self.assertTrue(progress.mainl_staff_source_proven(units, evidence))
        c = progress.mainl_unit_progress(units)
        self.assertEqual((c["source"], c["source_bytes"], c["exact"], c["total"]), (49, 13184, 0, 145))
        self.assertIn("composed 9,483 B target-equal", progress.render_svg(units, [], evidence))
    def test_missing_repeat_evidence_or_source_rejects_caption(self):
        units, evidence = self.data()
        first = next(iter(progress.MAINL_STAFF_SOURCE_UNITS))
        missing = progress.MAINL_STAFF_SOURCE_UNITS[first]["evidence"][-1]
        self.assertFalse(progress.mainl_staff_source_proven(units, [e for e in evidence if e["id"] != missing]))
        for u in units:
            if u["id"] == first: u["source"] = ""
        self.assertFalse(progress.mainl_staff_source_proven(units, evidence))
