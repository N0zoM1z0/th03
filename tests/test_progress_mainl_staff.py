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
    def historical_sources(self, units):
        projected=copy.deepcopy(units)
        for unit in projected:
            expected=progress.MAINL_STAFF_SOURCE_UNITS.get(unit['id'])
            if expected:
                unit['source']=expected['source']
        return projected
    def test_earned_existing_partition_counts(self):
        units, evidence = self.data()
        # Unput now comes from the natural staffdat.cpp producer. The older
        # hybrid diagnostic stays bound to its original source assignment.
        self.assertFalse(progress.mainl_staff_source_proven(units, evidence))
        self.assertTrue(progress.mainl_staff_source_proven(self.historical_sources(units), evidence))
        c = progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"], 49)
        self.assertGreaterEqual(c["source_bytes"], 13184)
        self.assertEqual((c["exact"], c["total"]), (0, 163))
        self.assertIn("target-equal", progress.render_svg(units, [], evidence))
    def test_missing_repeat_evidence_or_source_rejects_caption(self):
        units, evidence = self.data()
        units=self.historical_sources(units)
        self.assertTrue(progress.mainl_staff_source_proven(units, evidence))
        first = next(iter(progress.MAINL_STAFF_SOURCE_UNITS))
        missing = progress.MAINL_STAFF_SOURCE_UNITS[first]["evidence"][-1]
        self.assertFalse(progress.mainl_staff_source_proven(units, [e for e in evidence if e["id"] != missing]))
        for u in units:
            if u["id"] == first: u["source"] = ""
        self.assertFalse(progress.mainl_staff_source_proven(units, evidence))
