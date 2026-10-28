"""Complete comment/copy bodies and their real animation/delay dependencies."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.op_music_comment import Machine, Prediction, ContractError, RANGES, layout, negative_controls
from lib.op_music_comment import CMT, BG, address
from review_th03_op_cfg_work import images
import review_th03_op_music_comment_work as review


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpMusicCommentCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)

    def test_complete_native_layout(self):
        row = layout(ROOT, self.work, self.target, self.candidate)
        self.assertEqual((row['procedures'], row['code_bytes'], row['instruction_count'],
                          len(row['native_fields']), len(row['ordered_relocations'])), (7, 907, 315, 63, 14))

    def test_equal_corrupted_images_cannot_inherit_native_proof(self):
        raw = bytearray(self.target.program_image)
        raw[RANGES[0][0] + 1] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'complete native/target/candidate bytes'):
            layout(ROOT, self.work, bad, bad)

    def test_all65_native_controls_reject(self):
        row = negative_controls(self.target)
        self.assertEqual((row['actual_instruction_mutations'], len(set(row['rejected']))), (65, 65))

    def test_verifier_defects_never_count_as_guest_rejections(self):
        with patch.object(Machine, '__init__', side_effect=RuntimeError('constructor defect')):
            with self.assertRaisesRegex(RuntimeError, 'constructor defect'):
                negative_controls(self.target)
        with patch.object(Prediction, 'put', side_effect=ContractError('scalar defect')):
            with self.assertRaisesRegex(ContractError, 'scalar defect'):
                negative_controls(self.target)
        for exception in (IndexError, AssertionError, TypeError, ValueError):
            with self.subTest(exception=exception):
                with patch.object(Machine, 'event', side_effect=exception('hook defect')):
                    with self.assertRaisesRegex(exception, 'hook defect'):
                        negative_controls(self.target)

    def test_signed_seek_and_partial_read_keep_last_byte_of_each_record(self):
        m = Machine(self.target, 0x3000)
        try:
            for track, offset in ((39, 32760), (40, -31936), (0x8000, 0), (0xFFFF, -840)):
                row = m.run('load', track=track, read_bytes=0)
                self.assertEqual(row['signed_seek_offset'], offset)
                for line in range(20):
                    at = address(m.ds, CMT + 42 * line)
                    self.assertEqual(bytes(m.uc.mem_read(at + 40, 2)), b'\0' + m.initial[at + 41:at + 42])
        finally:
            m.close()

    def test_actual_dependency_chain_keeps_semicolons_and_reloads_free_pointer(self):
        m = Machine(self.target, 0x1000)
        try:
            m.run('bg_snap', allocated=(0, 0x5400, 0x5800, 0x5C00), source_offset=65535, flags=0xED7)
            row = m.run('comment', reenter=True, read_bytes=0, flags=0xED7)
            self.assertEqual((row['text_calls'], row['maximum_stack_depth']), (20, 24))
            for line in range(20):
                self.assertEqual(bytes(m.uc.mem_read(address(m.ds, CMT + 42 * line), 1)), b';')
            row = m.run('flip', reenter=True, ticks=(0, 0, 65535), flags=0xED7)
            self.assertEqual(row['maximum_stack_depth'], 44)
            row = m.run('bg_free', reenter=True, free_reload=True)
            self.assertEqual((row['free_calls'], row['maximum_stack_depth']), (4, 8))
            self.assertEqual(bytes(m.uc.mem_read(address(m.ds, BG + 6), 2)), b'\xEF\xBE')
        finally:
            m.close()

    def test_complete_current_report_and_dependency_smoke(self):
        row = review.check()
        self.assertEqual((row['images'], row['cases_per_image']), (2, 8))

    def test_partial_or_widened_witness_rejects(self):
        report = json.loads(review.REPORT.read_bytes())
        review.witness(report)
        for path, value in ((('source_ownership_promoted',), True), (('runtime', 'images'), 1),
                            (('runtime', 'ignored_stack_bytes'), 24), (('layout', 'code_bytes'), 906),
                            (('negative_controls', 'actual_instruction_mutations'), 64)):
            bad = deepcopy(report)
            at = bad
            for key in path[:-1]:
                at = at[key]
            at[path[-1]] = value
            with self.assertRaises(ValueError):
                review.witness(bad)


if __name__ == '__main__':
    unittest.main()
