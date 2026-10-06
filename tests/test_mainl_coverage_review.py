"""Physical interval unions preserve decoded segment namespaces and gap boundaries."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from review_th03_mainl_coverage import coverage


def unit(id,start,size,**changes):
    return dict(id=id,artifact='th03-mainl',segment='decoded:0000',offset=str(start),size=str(size),boundary_state='reviewed',state='boundary-reviewed')|changes


class CoverageTests(unittest.TestCase):
    def test_clipped_union_and_half_open_gaps(self):
        rows=coverage([unit('left',8,4),unit('right',17,5)],[dict(start=10,size=10)],100)
        self.assertEqual(rows[0]['independent_unit_bytes'],5)
        self.assertEqual(rows[0]['independent_unit_gaps'],[dict(start=12,size=5)])
        self.assertEqual(rows[0]['unit_intersections'],[dict(unit='left',start=10,size=2),dict(unit='right',start=17,size=3)])

    def test_overlap_is_reported_without_duplicate_byte_credit(self):
        row=coverage([unit('a',10,5),unit('b',13,7)],[dict(start=10,size=10)],100)[0]
        self.assertEqual(row['independent_unit_bytes'],10);self.assertEqual(row['overlapping_unit_bytes'],2);self.assertEqual(row['independent_unit_gaps'],[])

    def test_review_and_artifact_filters_keep_physical_segment_coordinates(self):
        units=[unit('yes',1,3,segment='decoded:0001'),unit('other',17,3,artifact='th03-main'),unit('stored',17,3,segment='0001'),unit('pending',17,3,boundary_state='pending')]
        row=coverage(units,[dict(start=16,size=5)],100)[0]
        self.assertEqual(row['independent_unit_bytes'],3);self.assertEqual([r['unit'] for r in row['unit_intersections']],['yes']);self.assertEqual(row['independent_unit_gaps'],[dict(start=16,size=1),dict(start=20,size=1)])

    def test_out_of_image_and_negative_bounds_fail_closed(self):
        for row in (unit('negative',-1,1),unit('past',99,2),unit('negative-size',0,-1),unit('wide-offset',65536,0),unit('negative-segment',0,1,segment='decoded:-001')):
            with self.assertRaisesRegex(ValueError,'unit exceeds'):coverage([row],[dict(start=0,size=100)],100)
        for carrier in (dict(start=-1,size=1),dict(start=99,size=2)):
            with self.assertRaisesRegex(ValueError,'carrier exceeds'):coverage([], [carrier],100)


if __name__=='__main__':unittest.main()
