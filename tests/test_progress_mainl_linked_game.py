import csv
from pathlib import Path
import unittest
import progress
ROOT=Path(__file__).resolve().parents[1]
class LinkedGameProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def historical_sources(self, units):
        # The current ending owner migrated to the natural staffdat.cpp TU.
        # This older diagnostic cohort remains bound to its original sources.
        projected=[dict(u) for u in units]
        for unit in projected:
            expected=progress.MAINL_LINKED_GAME_SOURCE_UNITS.get(unit['id'])
            if expected:
                unit['source']=expected['source']
        return projected
    def test_earned_linked_game_counts_and_caption(self):
        units,evidence=self.data()
        self.assertFalse(progress.mainl_linked_game_source_proven(units,evidence))
        historical=self.historical_sources(units)
        self.assertTrue(progress.mainl_linked_game_source_proven(historical,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"],139)
        self.assertGreaterEqual(c["source_bytes"],27753)
        self.assertEqual((c["exact"],c["total"]),(0,211))
        self.assertIn("target-equal",progress.render_svg(units,[],evidence, op_status={'decoded_accepted':False}, zun_status={'decoded_accepted':False}))
        self.assertEqual(sum(int(v["size"]) for v in progress.MAINL_LINKED_GAME_SOURCE_UNITS.values()),1765)
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        units=self.historical_sources(units)
        self.assertTrue(progress.mainl_linked_game_source_proven(units,evidence))
        eid=next(iter(progress.MAINL_LINKED_GAME_SOURCE_UNITS.values()))["evidence"][-1]
        self.assertFalse(progress.mainl_linked_game_source_proven(units,[e for e in evidence if e["id"]!=eid]))
