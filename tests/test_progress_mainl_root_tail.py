import csv
from pathlib import Path
import unittest
import progress
ROOT=Path(__file__).resolve().parents[1]
class RootTailProgressTests(unittest.TestCase):
    def data(self):
        rows=[]
        for p in ("config/units.csv","config/evidence.csv"):
            with (ROOT/p).open() as f: rows.append(list(csv.DictReader(f)))
        return rows
    def test_earned_root_tail_counts_and_caption(self):
        units,evidence=self.data()
        self.assertFalse(progress.mainl_root_tail_source_proven(units,evidence))
        historical=[dict(u) for u in units]
        for unit in historical:
            # Restore the historical105-byte joystick aggregate only in this fixture.
            if unit['id']=='th03-mainl-decoded-root-tail-joystick':
                unit.update(offset='0x2aad',size='105',compare_size='105',source='src/mainl/root_tail/joystick_prefix.asm')
            if unit['id']=='th03-mainl-decoded-root-tail-pfgetc-zero':
                unit['state']='source-present'
        self.assertTrue(progress.mainl_root_tail_source_proven(historical,evidence))
        c=progress.mainl_unit_progress(units)
        self.assertGreaterEqual(c["source"],116)
        self.assertGreaterEqual(c["source_bytes"],25988)
        self.assertEqual((c["exact"],c["total"]),(0,234))
        self.assertIn("target-equal",progress.render_svg(units,[],evidence, op_status={'decoded_accepted':False}, zun_status={'decoded_accepted':False}))
        self.assertEqual(sum(int(v["size"]) for v in progress.MAINL_ROOT_TAIL_SOURCE_UNITS.values()),722)
    def test_missing_repeat_evidence_rejects_caption(self):
        units,evidence=self.data()
        for unit in units:
            # Restore the historical105-byte joystick aggregate only in this fixture.
            if unit['id']=='th03-mainl-decoded-root-tail-joystick':
                unit.update(offset='0x2aad',size='105',compare_size='105',source='src/mainl/root_tail/joystick_prefix.asm')
            if unit['id']=='th03-mainl-decoded-root-tail-pfgetc-zero':
                unit['state']='source-present'
        eid=next(iter(progress.MAINL_ROOT_TAIL_SOURCE_UNITS.values()))["evidence"][-1]
        self.assertFalse(progress.mainl_root_tail_source_proven(units,[e for e in evidence if e["id"]!=eid]))
