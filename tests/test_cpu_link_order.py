"""Portable checks for the read-only, historical CPU ordering diagnostic."""
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib
import hashlib
import io
import struct
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_th03_cpu_link_order as review


class CPULinkOrderTests(unittest.TestCase):
    def test_input_pin_count_and_optional_locations(self):
        roots = {'baseline': Path('/fixture/base'), 'combined': Path('/fixture/new')}
        target = Path('/fixture/original.exe')
        with mock.patch.object(review, 'check_digest') as check:
            review.guard_inputs(roots, target)
        self.assertEqual(check.call_count, 13)
        self.assertEqual(check.call_args_list[0].args[0], roots['baseline'] / 'obj/th03/main.obj')
        self.assertEqual(check.call_args_list[-1].args[0], target)
        self.assertEqual(len({call.args[1] for call in check.call_args_list}), 13)

    def test_last_pin_failure_still_precedes_all_parsing(self):
        roots = {'baseline': Path('/fixture/base'), 'combined': Path('/fixture/new')}
        with mock.patch.object(review, 'check_digest',
                               side_effect=[None] * 12 + [ValueError('last pin')]) as guard:
            with mock.patch.object(review, 'rows') as parse:
                with self.assertRaisesRegex(ValueError, 'last pin'):
                    review.analyze(roots, Path('/fixture/target'))
                self.assertEqual(guard.call_count, 13)
                parse.assert_not_called()

    def test_default_paths_are_script_relative(self):
        with mock.patch.object(review, 'analyze', return_value={}) as analyze:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(review.main([]), 0)
        roots, target = analyze.call_args.args
        self.assertEqual(roots['baseline'], review.REPOSITORY / review.DEFAULT_ROOTS['baseline'])
        self.assertEqual(roots['combined'], review.REPOSITORY / review.DEFAULT_ROOTS['combined'])
        self.assertEqual(target, review.REPOSITORY / review.DEFAULT_TARGET)
        self.assertEqual(review.REPOSITORY, Path(review.__file__).resolve().parents[1])

    def test_matching_hash(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input'
            path.write_bytes(b'fixture')
            review.check_digest(path, hashlib.sha256(b'fixture').hexdigest())

    def test_hash_mismatch_rejected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input'
            path.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                review.check_digest(path, hashlib.sha256(b'fixture').hexdigest())

    def test_missing_private_input_stops_before_parse(self):
        with TemporaryDirectory() as tmp, mock.patch.object(review, 'omf') as parse:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, 'private input is missing'):
                review.analyze({'baseline': root, 'combined': root}, root / 'target')
            parse.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

    def test_missing_cli_is_concise_and_read_only(self):
        with TemporaryDirectory() as tmp:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                result = review.main(['--baseline-root', tmp, '--candidate-root', tmp,
                                      '--target', str(Path(tmp) / 'missing.exe')])
            self.assertEqual(result, 1)
            self.assertEqual(out.getvalue(), '')
            self.assertIn('required private input is missing', err.getvalue())
            self.assertNotIn('Traceback', err.getvalue())
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_module_run_preserves_order(self):
        rows = [dict(index=i, module=name) for i, name in enumerate(['B', 'B', 'A'])]
        self.assertEqual(review.module_runs(rows), [
            dict(module='B', start=0, count=2), dict(module='A', start=2, count=1)])

    def test_interleaved_module_rejected(self):
        rows = [dict(index=i, module=name) for i, name in enumerate(['A', 'B', 'A'])]
        with self.assertRaisesRegex(ValueError, 'multiple literal MZ runs'):
            review.module_runs(rows)

    def test_same_multiset_different_literal_order_rejected(self):
        with self.assertRaisesRegex(ValueError, 'literal order mismatch'):
            review.same_order([2, 1], [1, 2], 'fixture')
        review.same_order([2, 1], [2, 1], 'fixture')

    def test_missing_duplicate_or_overlapping_map_ownership_rejected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'synthetic.exe'
            data = bytearray(36)
            data[:2] = b'MZ'
            struct.pack_into('<H', data, 6, 2)
            struct.pack_into('<H', data, 24, 28)
            struct.pack_into('<HHHH', data, 28, 3, 0, 1, 0)
            path.write_bytes(data)
            row = dict(start=0, size=5, module='fixture', segment='CODE')
            self.assertEqual([x['site'] for x in review.mz(path, [row])], [3, 1])
            for bad in ([], [row, row], [dict(row, size=2)], [dict(row, size=4)]):
                with self.subTest(rows=bad), self.assertRaises(ValueError):
                    review.mz(path, bad)

    def test_single_and_two_byte_omf_indices(self):
        self.assertEqual(review.index(bytes([0x7F]), 0), (127, 1))
        self.assertEqual(review.index(bytes([0x81, 0x23]), 0), (291, 2))
        with self.assertRaises(IndexError):
            review.index(bytes([0x81]), 0)


if __name__ == '__main__':
    unittest.main()
