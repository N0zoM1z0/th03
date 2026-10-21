import csv
from pathlib import Path
import unittest
import progress
ROOT = Path(__file__).resolve().parents[1]
class PiProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_earned_pi_counts_and_caption(self):
        units,evidence=self.data()
        self.assertTrue(progress.mainl_pi_decoder_source_proven(units,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"],51)
        self.assertGreaterEqual(c["source_bytes"],17196)
        self.assertEqual((c["exact"],c["total"]),(0,145))
        self.assertIn("target-equal",progress.render_svg(units,[],evidence))
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        evidence=[e for e in evidence if e["id"]!=progress.MAINL_PI_DECODER_EVIDENCE[-1]]
        self.assertFalse(progress.mainl_pi_decoder_source_proven(units,evidence))
