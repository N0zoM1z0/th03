"""Exact disposable-trial retirement, retained native proof and docs guard."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cleanup_after597_handoff_storage as cleanup


class AuditedDisposableBossTrials(unittest.TestCase):
    def test_deleted_only_the_three_exploratory_runs(self):
        self.assertEqual(len(cleanup.RETIRED), 3)
        self.assertEqual(sum(cleanup.EXPECTED_FILES), 5331)
        self.assertEqual(sum(cleanup.EXPECTED_ALLOCATED), 78938112)
        self.assertFalse(any((ROOT/path).exists() for path in cleanup.RETIRED))
        self.assertTrue(all("gptweb-561-" not in p for p in cleanup.RETIRED))
        self.assertTrue((ROOT/"docs/RE_HANDOFF_ARCHIVE_AFTER596.md").is_file())
        self.assertTrue((ROOT/"docs/STORAGE_HANDOFF_ARCHIVE_AFTER554.md").is_file())

    def test_full_path_hash_manifest_and_archived_original_logs(self):
        cleanup.verify()
        r=json.loads((cleanup.AUDIT/"report.json").read_text())
        self.assertEqual(r["status"],"applied")
        self.assertEqual(r["candidate_root_files"],5331)
        self.assertEqual(r["candidate_allocated_bytes"],78938112)
        self.assertEqual(len(r["archived"]),3)
        for originals in r["archived"].values():
            self.assertEqual(set(originals),{"receipt.json","compiler.log"})

    def test_source_root_native_receipts_and_active_boss_dirs_are_guarded(self):
        self.assertEqual(cleanup.previous_proofs(),cleanup.PROTECTED_ROOTS)
        self.assertTrue((ROOT/".analysis/work/main-yumemi-cpu-after596-native-build.json").is_file())
        self.assertTrue((ROOT/".analysis/work/mainl-score-input-pi-after587-native-build.json").is_file())

    def test_changed_source_root_sha_fails_closed(self):
        receipt=".analysis/work/main-eight-boss-after561-native-build.json"
        with patch.dict(cleanup.PROTECTED_ROOTS,{receipt:"0"*64}):
            with self.assertRaisesRegex(ValueError,
                                        "protected source-native proof root changed"):
                cleanup.previous_proofs()

    def test_cache_and_git_object_inventory_without_pruning(self):
        report=json.loads((cleanup.AUDIT/"git-maintenance.json").read_text())
        cache=json.loads((cleanup.AUDIT/"python-cache-maintenance.json").read_text())
        before=(cleanup.AUDIT/"git-objects-before.txt").read_bytes()
        after=(cleanup.AUDIT/"git-objects-after.txt").read_bytes()
        self.assertEqual(before,after)
        self.assertEqual(len(before.splitlines()),17926)
        self.assertTrue(report["all_Git_objects_retained"])
        self.assertTrue(report["all_object_type_and_size_tuples_equal"])
        self.assertTrue(report["complete_git_fsck_before_and_after"])
        self.assertEqual(report["allocated_bytes_reclaimed"],4743168)
        self.assertTrue(cache["only_regenerable_python_bytecode_removed"])
        self.assertEqual(cache["allocated_bytes_reclaimed"],11841536)
        self.assertEqual(78938112+4743168+11841536,95522816)



if __name__=="__main__":
    unittest.main()
