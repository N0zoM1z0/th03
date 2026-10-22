"""Retained native manifests and typed guard-closure regression controls."""
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

SHA = "1" * 64


class CleanupGuardClosureControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.analysis = self.root / ".analysis"
        self.analysis.mkdir(parents=True)
        self.patching = patch.multiple(
            c, ROOT=self.root, ANALYSIS=self.analysis,
            EVIDENCE=self.root / "config/evidence.csv",
            PRESERVED_ANALYSIS_FILES={self.analysis / "target-import.json"},
            PRESERVED_ANALYSIS_ROOTS={self.analysis / name for name in
                                      ("targets", "toolchain", "runtime", "ghidra")},
            CACHE_ROOTS=[],
        )
        self.patching.start()
        self.addCleanup(self.patching.stop)
        self.docs = patch.object(c.subprocess, "check_output",
                                 return_value=b"config/replay.json\0")
        self.docs.start()
        self.addCleanup(self.docs.stop)

    def put(self, name, value="payload"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return path

    def plan(self, phase="ordinary", extra=None):
        removed = []
        def record(path, dry_run):
            self.assertTrue(dry_run)
            self.assertIn(self.analysis, path.parents)
            removed.append(path)
            return 0
        with patch.object(c, "remove_path", side_effect=record):
            if phase == "ordinary":
                c.clean_analysis(True, extra)
            else:
                c.prune_unreferenced_receipts(True, extra)
        return removed

    def assert_retained(self, kept, removed):
        for path in kept:
            self.assertFalse(any(path == p or p in path.parents for p in removed),
                             f"{path} selected through {removed}")
            self.assertTrue(path.exists() or path.is_symlink())

    def native_chain(self):
        # The tracked recipe names a proposal directory; its replay implicitly
        # reads manifest.json, which must be found through the inputs list.
        self.put("config/replay.json", {"builds": [{
            "proposal": ".analysis/native-proposal",
            "output": ".analysis/native-output",
            "work": ".analysis/toolchain/work",
        }]})
        manifest = self.put(".analysis/native-proposal/manifest.json", {
            "schema": "native-proposal-v1",
            "inputs": [{"path": ".analysis/native-output/materialized-inputs.json",
                        "sha256": SHA, "bytes": 1, "mode": 420}],
        })
        materialized = self.put(".analysis/native-output/materialized-inputs.json", {
            ".analysis/bridge.json": {"sha256": SHA, "bytes": 1, "mode": 420},
            "work-relative.obj": {"sha256": SHA, "bytes": 1, "mode": 420},
        })
        bridge = self.put(".analysis/bridge.json", {"repeat_inputs": {
            "work-name.obj": {"path": ".analysis/provider/receipt.json", "sha256": SHA},
        }})
        receipt = self.put(".analysis/provider/receipt.json", {
            "source_inputs": [{"path": ".analysis/final/input.obj", "sha256": SHA}],
        })
        archive = self.put(".analysis/provider/unlisted/reference.tar")
        final = self.put(".analysis/final/input.obj")
        self.put(".analysis/obsolete/receipt.json", {})
        return [manifest, materialized, bridge, receipt, archive, final]

    def test_native_list_materialized_map_nested_guard_ordinary(self):
        kept = self.native_chain()
        self.assert_retained(kept, self.plan())
        self.assertNotIn(self.root / "work-relative.obj", c.proof_preserved_paths()[0])

    def test_native_list_materialized_map_nested_guard_receipt_pruning(self):
        kept = self.native_chain()
        removed = self.plan("receipts")
        self.assert_retained(kept, removed)
        self.assertIn(self.analysis / "obsolete", removed)

    def test_list_and_source_list_guards_discover_standalone_proofs(self):
        for key in ("inputs", "source_inputs"):
            obj = self.put(".analysis/" + key + "/obj")
            proof = self.put(".analysis/" + key + ".json", {
                key: [{"path": str(obj.relative_to(self.root)), "sha256": "stale"}],
            })
            self.assert_retained([obj, proof], self.plan())

    def test_empty_input_list_is_still_an_explicit_guard_collection(self):
        proof = self.put(".analysis/native.json", {"inputs": []})
        self.assert_retained([proof], self.plan())

    def test_documented_typed_descriptor_follows_transitive_json(self):
        self.put("config/replay.json", {"proof": ".analysis/review.json"})
        review = self.put(".analysis/review.json", {
            "provider": {"path": ".analysis/flat.json", "sha256": SHA},
        })
        flat = self.put(".analysis/flat.json", {".analysis/leaf.obj": SHA})
        leaf = self.put(".analysis/leaf.obj")
        self.assert_retained([review, flat, leaf], self.plan())

    def test_explicit_keep_follows_typed_descriptor(self):
        proof = self.put(".analysis/review.json", {
            "provider": {"path": ".analysis/leaf.obj", "sha256": SHA},
        })
        leaf = self.put(".analysis/leaf.obj")
        self.assert_retained([proof, leaf], self.plan(extra={proof}))

    def test_standalone_descriptors_and_hash_maps_are_not_proof_roots(self):
        self.put(".analysis/inventory.json", {
            ".analysis/disposable.obj": SHA,
            "member": {"path": ".analysis/disposable.obj", "sha256": SHA},
        })
        self.put(".analysis/disposable.obj")
        removed = self.plan()
        self.assertIn(self.analysis / "inventory.json", removed)
        self.assertIn(self.analysis / "disposable.obj", removed)

    def test_retained_archive_member_inventory_does_not_activate_originals(self):
        for label in ("schema", "status"):
            discriminator = ({"schema": "recoverable-analysis-archive-v1"} if label == "schema"
                             else {"status": "proposed-lossless-archive-not-applied"})
            original = self.put(".analysis/old-" + label + "/receipt.json", {})
            inventory = self.put(".analysis/backups/" + label + ".json", {
                **discriminator,
                "members": [{"path": str(original.relative_to(self.root)), "sha256": SHA}],
            })
        removed = self.plan("receipts", extra={self.analysis / "backups"})
        for label in ("schema", "status"):
            self.assertIn(self.analysis / ("old-" + label), removed)

    def test_archive_metadata_never_disables_explicit_input_guards(self):
        receipt = self.put(".analysis/provider/receipt.json", {})
        inventory = self.put(".analysis/backup.json", {
            "schema": "recoverable-analysis-archive-v1",
            "members": [{"inputs": [{
                "path": ".analysis/provider/receipt.json", "sha256": SHA,
            }]}],
        })
        self.assert_retained([receipt, inventory], self.plan("receipts"))

    def test_malformed_transitive_json_stops_before_candidate_reporting(self):
        self.put(".analysis/proof.json", {"inputs": [{
            "path": ".analysis/broken.json", "sha256": SHA,
        }]})
        self.put(".analysis/broken.json", "{broken")
        junk = self.put(".analysis/a-junk")
        with patch.object(c, "remove_path") as remove:
            with self.assertRaisesRegex(ValueError, "cannot inspect retained proof"):
                c.clean_analysis(True)
        remove.assert_not_called()
        self.assertTrue(junk.exists())

    def test_missing_list_dependency_stays_missing(self):
        proof = self.put(".analysis/proof.json", {"inputs": [{
            "path": ".analysis/missing.json", "sha256": SHA,
        }]})
        self.assert_retained([proof], self.plan())
        self.assertFalse((self.analysis / "missing.json").exists())

    def test_local_symlink_dependency_and_external_alias_are_safe(self):
        leaf = self.put(".analysis/leaf.obj")
        target = self.put(".analysis/target.json", {
            "provider": {"path": ".analysis/leaf.obj", "sha256": SHA},
        })
        alias = self.analysis / "alias.json"
        alias.symlink_to(target)
        outside = Path(self.temp.name) / "outside.json"
        outside.write_text("{not valid JSON outside the repository")
        external = self.analysis / "external.json"
        external.symlink_to(outside)
        proof = self.put(".analysis/proof.json", {"inputs": [
            {"path": ".analysis/alias.json", "sha256": SHA},
            {"path": ".analysis/external.json", "sha256": SHA},
        ]})
        self.assert_retained([leaf, target, alias, external, proof], self.plan())
        self.assertTrue(outside.exists())

    def test_external_parent_symlink_never_reads_queued_json(self):
        outside = Path(self.temp.name) / "external"
        outside.mkdir()
        external_json = outside / "manifest.json"
        external_json.write_text("{malformed external JSON must not be read")
        alias = self.analysis / "aliasdir"
        alias.symlink_to(outside, target_is_directory=True)
        lexical = alias / "manifest.json"
        proof = self.put(".analysis/proof.json", {"inputs": [{
            "path": ".analysis/aliasdir/manifest.json", "sha256": SHA,
        }]})
        read_text = Path.read_text
        def guarded_read(path, *args, **kwargs):
            self.assertNotEqual(path, lexical, "read through external parent symlink")
            self.assertNotEqual(path, external_json, "read external target JSON")
            return read_text(path, *args, **kwargs)
        with patch.object(Path, "read_text", new=guarded_read):
            self.assert_retained([alias, proof], self.plan())
            self.assertIn(lexical, c.proof_preserved_paths()[0])

    def test_external_parent_symlink_never_traverses_queued_directory(self):
        outside = Path(self.temp.name) / "external"
        nested = outside / "nested"
        nested.mkdir(parents=True)
        (nested / "manifest.json").write_text("{must not be inspected")
        alias = self.analysis / "aliasdir"
        alias.symlink_to(outside, target_is_directory=True)
        lexical = alias / "nested"
        proof = self.put(".analysis/proof.json", {"source_inputs": [{
            "path": ".analysis/aliasdir/nested", "sha256": SHA,
        }]})
        rglob = Path.rglob
        def guarded_rglob(path, *args, **kwargs):
            self.assertNotEqual(path, lexical, "traversed external parent symlink")
            self.assertNotEqual(path, nested, "traversed external target directory")
            return rglob(path, *args, **kwargs)
        with patch.object(Path, "rglob", new=guarded_rglob):
            self.assert_retained([alias, proof], self.plan())
            self.assertIn(lexical, c.proof_preserved_paths()[0])

    def test_local_parent_symlink_follows_validated_json_dependency(self):
        leaf = self.put(".analysis/final/leaf.obj")
        manifest = self.put(".analysis/real/nested/manifest.json", {
            "provider": {"path": ".analysis/final/leaf.obj", "sha256": SHA},
        })
        alias = self.analysis / "aliasdir"
        alias.symlink_to(self.analysis / "real", target_is_directory=True)
        lexical = alias / "nested" / "manifest.json"
        proof = self.put(".analysis/proof.json", {"inputs": [{
            "path": ".analysis/aliasdir/nested/manifest.json", "sha256": SHA,
        }]})
        self.assert_retained([leaf, manifest, alias, proof], self.plan())
        preserved, _ = c.proof_preserved_paths()
        self.assertIn(lexical, preserved)
        self.assertIn(manifest, preserved)

    def test_absolute_and_parent_traversal_descriptors_are_rejected(self):
        junk = self.put(".analysis/junk")
        self.put(".analysis/proof.json", {"inputs": [
            {"path": str(junk), "sha256": SHA},
            {"path": ".analysis/../.analysis/junk", "sha256": SHA},
        ]})
        self.assertIn(junk, self.plan())

    def test_transitive_typed_guard_protects_cache_input(self):
        self.put(".analysis/proof.json", {"inputs": [
            {"path": ".analysis/repeat.json", "sha256": SHA},
        ]})
        self.put(".analysis/repeat.json", {"repeat_inputs": {
            "cached": {"path": "scripts/__pycache__/required.pyc", "sha256": SHA},
        }})
        cache = self.put("scripts/__pycache__/required.pyc")
        with patch.object(c, "remove_path") as remove:
            c.clean_caches(True)
        remove.assert_not_called()
        self.assertTrue(cache.exists())

    def test_typed_and_flat_map_cycle_terminates(self):
        first = self.put(".analysis/first.json", {"inputs": [
            {"path": ".analysis/second.json", "sha256": SHA},
        ]})
        second = self.put(".analysis/second.json", {".analysis/first.json": SHA})
        self.assert_retained([first, second], self.plan())

    def test_nested_receipt_report_descriptor_keeps_external_receipt(self):
        receipt = self.put(".analysis/current/receipt.json", {})
        self.put(".analysis/current/nested/report.json", {
            "provider": {"path": ".analysis/provider/receipt.json", "sha256": SHA},
        })
        provider = self.put(".analysis/provider/receipt.json", {})
        output = self.put(".analysis/provider/unlisted.obj")
        self.assert_retained([receipt, provider, output],
                             self.plan("receipts", extra={receipt}))


if __name__ == "__main__":
    unittest.main()
