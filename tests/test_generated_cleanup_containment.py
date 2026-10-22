"""Lexical cleanup containment controls; no real repository cleanup."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import clean_generated as c


class CleanupContainmentControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.analysis = self.root / ".analysis"
        self.analysis.mkdir(parents=True)
        self.settings = dict(
            ROOT=self.root, ANALYSIS=self.analysis,
            EVIDENCE=self.root / "evidence.csv",
            PRESERVED_ANALYSIS_FILES={self.analysis / "target-import.json"},
            PRESERVED_ANALYSIS_ROOTS={
                self.analysis / name
                for name in ("targets", "toolchain", "runtime", "ghidra")
            },
            CACHE_ROOTS=[],
        )
        self.patching = patch.multiple(c, **self.settings)
        self.patching.start()
        self.addCleanup(self.patching.stop)
        self.docs = patch.object(c, "documented_analysis_paths", return_value=set())
        self.docs.start()
        self.addCleanup(self.docs.stop)

    def put(self, name, text="payload"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def plan(self, extra=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            size = c.clean_analysis(True, extra)
        return size, output.getvalue().splitlines()

    def assert_candidates(self, expected, extra=None):
        size, lines = self.plan(extra)
        self.assertEqual(lines, expected)
        # The standalone differential runner injects a frozen original module.
        baseline = getattr(self, "baseline", None)
        if baseline is not None:
            with patch.multiple(baseline, **self.settings), \
                    patch.object(baseline, "documented_analysis_paths", return_value=set()), \
                    contextlib.redirect_stdout(io.StringIO()) as old_output:
                old_size = baseline.clean_analysis(True, extra)
            self.assertEqual((size, lines), (old_size, old_output.getvalue().splitlines()))
        return size

    def test_shared_ancestor_and_prefix_collision(self):
        kept = self.put(".analysis/run/keep/input.obj")
        self.put(".analysis/run/keep/junk.obj")
        self.put(".analysis/run/keeper/junk.obj")
        self.put(".analysis/report.json", json.dumps({"inputs": {
            ".analysis/run/keep/input.obj": "sha",
        }}))
        self.assert_candidates([
            "would remove file .analysis/run/keep/junk.obj",
            "would remove tree .analysis/run/keeper",
        ])
        self.assertTrue(kept.is_file())

    def test_nested_receipt_roots_and_explicit_active_tree(self):
        for name in ("cold/receipt.json", "cold/nested/receipt.json"):
            self.put(".analysis/" + name, "{}")
        archive = self.put(".analysis/cold/unlisted/archive.tar")
        self.put(".analysis/active/deep/unlisted.obj")
        self.put(".analysis/active/nested/receipt.json", "{}")
        self.put(".analysis/unused/junk.obj")
        self.assert_candidates(
            ["would remove tree .analysis/unused"],
            {self.analysis / "active"},
        )
        self.assertTrue(archive.is_file())

    def test_missing_guard_under_regular_file_retains_that_file(self):
        blocker = self.put(".analysis/block")
        self.put(".analysis/blocker/junk")
        self.put(".analysis/proof.json", json.dumps({"source_inputs": {
            ".analysis/block/not-created/input.obj": "sha",
        }}))
        self.assert_candidates(["would remove tree .analysis/blocker"])
        self.assertTrue(blocker.is_file())
        self.assertFalse((blocker / "not-created").exists())

    def test_missing_explicit_pin_does_not_keep_sibling(self):
        self.put(".analysis/deep/junk")
        missing = self.analysis / "deep" / "not-created" / "input.obj"
        self.assert_candidates(
            ["would remove file .analysis/deep/junk"], {missing}
        )
        self.assertFalse(missing.exists())

    def test_local_external_and_broken_guarded_symlinks(self):
        target = self.put(".analysis/real/guard.obj")
        alias = self.analysis / "alias.obj"
        alias.symlink_to(target)
        outside = Path(self.temp.name) / "outside.obj"
        outside.write_text("external")
        external_alias = self.analysis / "external.obj"
        external_alias.symlink_to(outside)
        broken = self.analysis / "broken.obj"
        broken.symlink_to(self.root / "missing-target.obj")
        self.put(".analysis/real/junk.obj")
        self.put(".analysis/proof.json", json.dumps({"inputs": {
            ".analysis/alias.obj": "sha",
            ".analysis/external.obj": "sha",
            ".analysis/broken.obj": "sha",
        }}))
        self.assert_candidates(["would remove file .analysis/real/junk.obj"])
        for path in (alias, external_alias, broken):
            self.assertTrue(path.is_symlink())
        self.assertEqual(outside.read_text(), "external")

    def test_private_tree_symlink_and_empty_directory_survive(self):
        external = Path(self.temp.name) / "external-state"
        external.mkdir()
        (external / "state").write_text("private")
        toolchain = self.analysis / "toolchain"
        toolchain.symlink_to(external, target_is_directory=True)
        (self.analysis / "runtime" / "empty").mkdir(parents=True)
        self.put(".analysis/unreferenced")
        self.assert_candidates(["would remove file .analysis/unreferenced"])
        self.assertTrue(toolchain.is_symlink())
        self.assertTrue((self.analysis / "runtime" / "empty").is_dir())

    def test_invalid_guards_do_not_become_implicit_keeps(self):
        self.put(".analysis/junk")
        self.put(".analysis/proof.json", json.dumps({"inputs": {
            "../escape": "sha",
            str(self.analysis / "junk"): "sha",
            "": "sha",
            ".analysis/missing.obj": "sha",
        }}))
        self.assert_candidates(["would remove file .analysis/junk"])
        self.assertFalse((self.analysis / "missing.obj").exists())

    def test_malformed_receipt_fails_before_candidate_reporting(self):
        self.put(".analysis/a-junk")
        self.put(".analysis/z/receipt.json", "{broken")
        modules = [c]
        if getattr(self, "baseline", None) is not None:
            modules.append(self.baseline)
        for module in modules:
            with patch.multiple(module, **self.settings), \
                    patch.object(module, "documented_analysis_paths", return_value=set()), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                with self.assertRaisesRegex(ValueError, "cannot inspect retained proof"):
                    module.clean_analysis(True)
            self.assertEqual(output.getvalue(), "")
        self.assertTrue((self.analysis / "a-junk").is_file())


if __name__ == "__main__":
    unittest.main()
