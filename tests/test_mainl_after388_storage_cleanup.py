"""Fail-closed archive cleanup: never retire original live MAINL native proof."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cleanup_mainl_after388_handoff as cleanup
from cleanup_mainl_handoff_artifacts import active_inputs, candidates


class ProtectedSourceBoundStorage(unittest.TestCase):
    def test_exact_126_stage_511_source_dag(self):
        layers = cleanup.layers()
        self.assertEqual(len(layers), 126)
        self.assertEqual(layers[0], ('after62', 'sprintf-calloc-puts-ctime'))
        self.assertEqual(layers[-1], ('after388', 'string-default-constructor-boss'))
        self.assertEqual(len(layers), len(set(layers)))

    def test_live_original_obj_lib_exe_map_rounds_all_untouchable(self):
        protected = active_inputs(cleanup.layers())
        self.assertGreaterEqual(len(protected), 3308)
        self.assertTrue(all(path.is_file() for path in protected))
        retired, _ = candidates(cleanup.layers(), protected)
        self.assertFalse(set(retired) & protected)
        self.assertFalse(set(cleanup.scratch_candidates(protected)) & protected)
        # Source-generated xxdisp listings have historical RTTI/exception
        # provenance even if a tracked script reads them by dynamic stem.
        self.assertTrue(all(p.suffix != '.lst' for p in cleanup.scratch_candidates(protected)))
        self.assertTrue(all(str(p).startswith(str(cleanup.WORK)) for p in retired))
        for kind in ('round1-newcrt.lib', 'round2-newcrt.lib',
                     'round1-linked.exe', 'round2-linked.map'):
            self.assertTrue(any(kind in p.name and 'after388' in p.name
                                for p in protected))

    def test_current_receipt_must_remain_unchanged(self):
        cleanup.guard()
        with patch.object(cleanup, 'RECEIPT_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'receipt changed'):
                cleanup.guard()

    def test_every_live_source_driver_log_and_raw_vector_hash(self):
        # Native outputs are retained as real files, not replaceable stubs.
        cleanup.verify_active_hashes(cleanup.layers())

    def test_reapply_with_no_candidates_preserves_old_audit_manifest(self):
        # A future after389 checkpoint must re-audit; the after388 same-checkout
        # no-op may never erase the names of previously deleted artifacts.
        manifest = cleanup.MANIFEST
        if not manifest.is_file():
            self.skipTest('pruning has not been applied in this checkout')
        before = manifest.read_bytes()
        import subprocess
        result = subprocess.run([sys.executable,
             str(ROOT / 'scripts/cleanup_mainl_after388_handoff.py'), '--apply'],
             cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertIn('NOOP: all eligible output already retired', result.stdout)
        self.assertEqual(manifest.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
