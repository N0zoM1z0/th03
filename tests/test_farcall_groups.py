"""Check the limited frame classifier and exact native call-window decoder."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import importlib.util
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
with patch.object(sys, 'path', [str(ROOT / 'scripts'), *sys.path]):
    spec = importlib.util.spec_from_file_location('farcall_groups_review', ROOT / 'scripts/review_th03_farcall_groups.py')
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)


def row(start, size, segment, group):
    return dict(start=start, size=size, category='CODE', segment=segment, group=group, module='control')


class FarCallGroupsTests(unittest.TestCase):
    def test_first_segment_uses_actual_layout_not_input_order(self):
        rows = [row(1, 20, 'A', 'G'), row(0, 1, 'B', 'G')]
        self.assertFalse(r.frame_observation(rows, 2, 1)['predicted_relaxed'])
        self.assertTrue(r.frame_observation(rows, 2, 0)['predicted_relaxed'])

    def test_group_membership_reverses_result_without_moving_code(self):
        rows = [row(0, 1, 'B', 'G'), row(1, 20, 'A', '(none)')]
        self.assertTrue(r.frame_observation(rows, 2, 1)['predicted_relaxed'])
        self.assertFalse(r.frame_observation(rows, 2, 0)['predicted_relaxed'])

    def test_missing_or_overlapping_owner_rejected(self):
        for rows in ([row(0, 1, 'B', 'G')], [row(0, 8, 'A', 'G'), row(1, 8, 'B', 'G')]):
            with self.subTest(rows=rows), self.assertRaisesRegex(ValueError, 'unique CODE owner'):
                r.frame_observation(rows, 2, 0)

    def test_far_pointer_and_negative_near_displacement(self):
        far = SimpleNamespace(program_image=bytes.fromhex('9a34127856'))
        self.assertEqual(r.call_window(far, 0)[:2], (False, 0x56780 + 0x1234))
        near = SimpleNamespace(program_image=b'\x00' * 10 + bytes.fromhex('900ee8f1ff'))
        self.assertEqual(r.call_window(near, 10)[:2], (True, 0))

    def test_short_window_and_changed_opcode_rejected(self):
        for raw in (bytes.fromhex('900ee800'), bytes.fromhex('900ee90000')):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                r.call_window(SimpleNamespace(program_image=raw), 0)

    def test_zero_length_contributions_do_not_own_calls(self):
        text = (' 0000:0000 0000 C=CODE S=A G=G M=empty.asm ACBP=28\n'
                ' 0000:0000 0001 C=CODE S=B G=G M=body.asm ACBP=28\n')
        self.assertEqual([q['segment'] for q in r.contributions(text)], ['B'])


if __name__ == '__main__':
    unittest.main()
