import csv
from pathlib import Path
import unittest
import progress
ROOT=Path(__file__).resolve().parents[1]
class ArchiveProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_earned_archive_counts_and_caption(self):
        units,evidence=self.data()
        self.assertTrue(progress.mainl_archive_io_source_proven(units,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"],84)
        self.assertGreaterEqual(c["source_bytes"],23150)
        self.assertEqual((c["exact"],c["total"]),(0,180))
        self.assertIn("target-equal",progress.render_svg(units,[],evidence))
        self.assertEqual(sum(int(v["size"]) for v in progress.MAINL_ARCHIVE_IO_SOURCE_UNITS.values()),2479)
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        eid=next(iter(progress.MAINL_ARCHIVE_IO_SOURCE_UNITS.values()))["evidence"][-1]
        self.assertFalse(progress.mainl_archive_io_source_proven(units,[e for e in evidence if e["id"]!=eid]))
