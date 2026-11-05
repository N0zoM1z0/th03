"""The after439 storage cleanup may never erase a source-bound native proof."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cleanup_mainl_after439_handoff as cleanup
from cleanup_mainl_handoff_artifacts import active_inputs, candidates


class ProtectedAfter439NativeEvidence(unittest.TestCase):
    def test_exact_current_177_stage_graph(self):
        graph = cleanup.layers()
        self.assertEqual(len(graph), 177)
        self.assertEqual(graph[0], ('after62', 'sprintf-calloc-puts-ctime'))
        self.assertEqual(graph[-1],
                         ('after439', 'streambuf-base-default-constructor-boss'))
        self.assertEqual(len(graph), len(set(graph)))

    def test_all_4464_receipt_log_and_raw_output_paths_protected(self):
        graph = cleanup.layers()
        required = active_inputs(graph)
        self.assertEqual(len(required), 4464)
        self.assertTrue(all(p.is_file() and not p.is_symlink() for p in required))
        alternate, _ = candidates(graph, required)
        self.assertFalse(set(alternate) & required)
        self.assertFalse(set(cleanup.scratch_candidates(required)) & required)
        self.assertTrue(all(p.suffix != '.lst' for p in cleanup.scratch_candidates(required)))
        self.assertTrue(any('after439' in p.name and 'round1-newcrt.lib' in p.name
                            for p in required))
        self.assertTrue(any('after439' in p.name and 'round2-linked.exe' in p.name
                            for p in required))

    def test_latest_receipt_sha_guard_fails_closed(self):
        cleanup.guard()
        with patch.object(cleanup, 'RECEIPT_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'receipt changed'):
                cleanup.guard()

    def test_every_active_output_source_driver_and_log_hash(self):
        cleanup.verify_active_hashes(cleanup.layers())

    def test_alt_mode_is_only_audited_completed_archive(self):
        graph = cleanup.layers()
        required = active_inputs(graph)
        old, _ = candidates(graph, required)
        # The two old incomplete h_ldiv groups stay outside the confirmed
        # cleanup set; do not infer safe deletion from archive-mode status.
        safe = [p for p in old if p.name.startswith('after392-cpp-vector-delete-boss-')]
        self.assertIn(len(safe), (0, 15))
        self.assertTrue(all(p not in required and p.is_file() for p in safe))
        if cleanup.MANIFEST.exists():
            paths = [ROOT / p for p in cleanup.MANIFEST.read_text().splitlines()]
            self.assertEqual(len(paths), 15)
            self.assertTrue(all(not p.exists() for p in paths))


if __name__ == '__main__':
    unittest.main()
