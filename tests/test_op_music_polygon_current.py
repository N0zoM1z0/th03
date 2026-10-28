"""Actual polygon instructions, full frames, adversarial guests and bindings."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.op_music_polygon import Machine, Prediction, ContractError, START, SIZE, layout, negative_controls
from review_th03_op_cfg_work import images
import review_th03_op_music_polygon_work as review


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpMusicPolygonCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)

    def test_complete_native_layout_and_order(self):
        result = layout(ROOT, self.work, self.target, self.candidate)
        self.assertEqual((result['procedures'], result['code_bytes'], result['instruction_count'],
                          len(result['native_fields']), len(result['ordered_relocations'])), (2, 645, 219, 54, 14))

    def test_identical_corrupted_images_cannot_inherit_native_proof(self):
        raw = bytearray(self.target.program_image)
        raw[START + 1] ^= 2
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate'):
            layout(ROOT, self.work, bad, bad)

    def test_all46_actual_instruction_mutations_reject(self):
        result = negative_controls(self.target)
        self.assertEqual(result['actual_instruction_mutations'], 46)
        self.assertEqual(len(set(result['rejected'])), 46)

    def test_verifier_defects_are_never_counted_as_guest_rejections(self):
        with patch.object(Machine, '__init__', side_effect=RuntimeError('constructor defect')):
            with self.assertRaisesRegex(RuntimeError, 'constructor defect'):
                negative_controls(self.target)
        with patch.object(Prediction, 'build', side_effect=ContractError('scalar defect')):
            with self.assertRaisesRegex(ContractError, 'scalar defect'):
                negative_controls(self.target)
        for exception in (IndexError, AssertionError, TypeError, ValueError):
            with self.subTest(exception=exception):
                with patch.object(Machine, 'event', side_effect=exception('hook defect')):
                    with self.assertRaisesRegex(exception, 'hook defect'):
                        negative_controls(self.target)

    def test_actual_two_loads_signed_division_and_reentry(self):
        for load in (0x1000, 0x3000):
            m = Machine(self.target, load)
            try:
                row = m.run('build', count=256, angle=0xFFFF, radius=-32768, center_y=0x7FFF, flags=0xED7, stack=0x100)
                self.assertEqual(row['maximum_stack_depth'], 22)
                first = m.run('update', initialized=0, seed=1, flags=0xED7, stack=0xFFF0)
                second = m.run('update', reenter=True, seed=1, flags=0xED7, stack=0xFFF0)
                self.assertEqual((first['render_calls'], second['render_calls']), (16, 16))
                self.assertNotEqual(first['trace_sha256'], second['trace_sha256'])
                self.assertEqual((first['maximum_stack_depth'], second['maximum_stack_depth']), (40, 40))
                # A separate boundary frame reaches reset and both reset zero
                # replacements; freshly initialized polygons start above it.
                m.run('update', initialized=1, seed=10)
                self.assertEqual(len(m.covered), SIZE)
            finally:
                m.close()

    def test_complete_current_report_and_smoke(self):
        result = review.check()
        self.assertEqual((result['images'], result['cases_per_image']), (2, 6))

    def test_partial_or_wider_witness_is_rejected(self):
        report = json.loads(review.REPORT.read_bytes())
        review.witness(report)
        for path, value in ((('source_ownership_promoted',), True), (('runtime', 'images'), 1),
                            (('runtime', 'ignored_stack_bytes'), 40), (('layout', 'code_bytes'), 644),
                            (('negative_controls', 'actual_instruction_mutations'), 45)):
            bad = deepcopy(report)
            at = bad
            for key in path[:-1]:
                at = at[key]
            at[path[-1]] = value
            with self.assertRaises(ValueError):
                review.witness(bad)


if __name__ == '__main__':
    unittest.main()
