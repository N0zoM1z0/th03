import csv
from pathlib import Path
import unittest
from unittest.mock import patch
import progress
ROOT=Path(__file__).resolve().parents[1]
class CrtProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_earned_crt_counts_and_caption(self):
        units,evidence=self.data()
        self.assertTrue(progress.mainl_crt_source_proven(units,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertEqual((c["source"],c["source_bytes"],c["exact"],c["total"]),(195,38160,0,195))
        # The old aggregate requires the old linked-game source assignment.
        # Ending now comes from staffdat.cpp, so current units suppress it even
        # when publication is unavailable. Preserve the historical caption test
        # using its historical source projection, including the old literal table,
        # without reassigning the ledger.
        with patch('status.mainl_product_status', return_value={
                'product_exact': False, 'decoded_exact_units': 0}):
            self.assertNotIn("24,680 B target-equal",progress.render_svg(units,[],evidence, op_status={'decoded_accepted':False}, zun_status={'decoded_accepted':False}))
            historical=[dict(u) for u in units]
            for unit in historical:
                if unit['id']=='th03-mainl-decoded-root-tail-pfgetc-zero':
                    unit['state']='source-present'
                expected=(progress.MAINL_LINKED_GAME_SOURCE_UNITS.get(unit['id'])
                          or progress.MAINL_STAFF_SOURCE_UNITS.get(unit['id'])
                          or progress.MAINL_RESOURCES_SOURCE_UNITS.get(unit['id']))
                if expected:
                    unit['source']=expected['source']
            self.assertIn("24,680 B target-equal",progress.render_svg(historical,[],evidence, op_status={'decoded_accepted':False}, zun_status={'decoded_accepted':False}))
        self.assertEqual(sum(int(v["size"]) for v in progress.MAINL_CRT_SOURCE_UNITS.values()),628)
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        eid=next(iter(progress.MAINL_CRT_SOURCE_UNITS.values()))["evidence"][-1]
        self.assertFalse(progress.mainl_crt_source_proven(units,[e for e in evidence if e["id"]!=eid]))
