import csv
from pathlib import Path
import unittest
import progress
ROOT=Path(__file__).resolve().parents[1]
class ResourcesProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_earned_resource_counts_and_caption(self):
        units,evidence=self.data()
        self.assertTrue(progress.mainl_resources_source_proven(units,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"],65)
        self.assertGreaterEqual(c["source_bytes"],20671)
        self.assertEqual((c["exact"],c["total"]),(0,150))
        self.assertIn("target-equal",progress.render_svg(units,[],evidence))
        self.assertEqual(sum(int(v["size"]) for v in progress.MAINL_RESOURCES_SOURCE_UNITS.values()),3475)
        self.assertNotIn("th03-mainl-heap-manager",progress.MAINL_RESOURCES_SOURCE_UNITS)
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        eid=next(iter(progress.MAINL_RESOURCES_SOURCE_UNITS.values()))["evidence"][-1]
        self.assertFalse(progress.mainl_resources_source_proven(units,[e for e in evidence if e["id"]!=eid]))
