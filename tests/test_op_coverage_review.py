"""Cold carrier crossing is diagnostic, not inferred original/source ownership."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_op_coverage as d


def unit(name='u',start=11,size=4,artifact='th03-op',state='boundary-reviewed'):
    return dict(id=name,artifact=artifact,segment='decoded:0000',offset=str(start),size=str(size),boundary_state='reviewed',state=state)


class CoverageTests(unittest.TestCase):
    def test_shifted_original_body_crosses_cold_carriers_without_claiming_equality(self):
        rows=d.coverage([unit()], [dict(start=10,size=4,module='init'),dict(start=14,size=3,module='next')],30)
        self.assertEqual([r['independent_unit_bytes'] for r in rows],[3,1])
        self.assertEqual(rows[0]['independent_unit_gaps'],[dict(start=10,size=1)])
        self.assertEqual(rows[1]['unit_intersections'],[dict(unit='u',start=14,size=1)])

    def test_other_artifacts_states_and_uncredited_context_do_not_count(self):
        carrier=[dict(start=10,size=5)]
        rows=d.coverage([unit(artifact='th03-mainl'),unit(state='unreviewed')],carrier,30)
        self.assertEqual(rows[0]['independent_unit_bytes'],0)
        self.assertEqual(rows[0]['independent_unit_gaps'],[dict(start=10,size=5)])
        rows=d.coverage([unit(),unit(name='v')],carrier,30)
        self.assertEqual(rows[0]['overlapping_unit_bytes'],4)
        self.assertEqual(rows[0]['independent_unit_bytes'],4)

    def test_unit_and_carrier_bounds_are_rejected(self):
        for u in (unit(start=-1),unit(start=65536),unit(size=-1),unit(start=28,size=4)):
            with self.assertRaisesRegex(ValueError,'unit exceeds'):d.coverage([u],[],30)
        for c in (dict(start=-1,size=3),dict(start=29,size=2),dict(start=5,size=-1)):
            with self.assertRaisesRegex(ValueError,'carrier exceeds'):d.coverage([], [c],30)


if __name__=='__main__':unittest.main()
