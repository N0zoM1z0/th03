"""Read-only checks for the separately attested 2026-10-22 recovery.

A source-only checkout may omit private evidence. Once its recovery attestation
is present, all bound artifacts must be present and retain their exact bytes.
These checks neither execute native tools nor confer source/exact acceptance.
"""

import hashlib
import json
import stat
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ".analysis/dependency-recovery-20261022-v01/effects-recovery.json"
RECOVERY_SHA = "ff724cabb7555395654572cfb2995f87a39f0b8428ec0388abfaef14002e3655"
EFFECTS = (
    ".analysis/gpt-dots-effects-established-linkage-probe-v01/"
    "compile-first-v01/source/obj/th03/effects.obj"
)
EFFECTS_SHA = "d37d84309d2cc4d66ef62e67c2685839ac05c74bc1ea90be60d408cb4272d13a"
OUTPUT = ".analysis/effects-fresh-reproduction-output-20261022-v02/"
FAILED_COMPLETION = ".analysis/effects-fresh-reproduction-output-20261022-v01/completion.json"
FAILED_SHA = "c1e103f31cc71a6a7f070c1d6f6ce39a69723b6c60b9842fb7e804c7d10a0e3b"


ARCHIVE_RECEIPTS = (
    ("001", "557c4d02b6630681b922dbb6fd689c3bd94484067281a10f333c7d3a5e21a3f3", 1),
    ("002", "533c1d20cbfd4df8f44e7a37fad226d6e281a530b6aa358d043d3a644254fbdd", 3),
    ("003", "19949f097bfaa155856d52ba6964aa8cd8caf4d1deb592a970de2f355cc383f5", 24),
    ("004", "caa35760c42b22d44ddb096a783af5c9e40b5099fc62110a0ad79df4bebb2439", 4),
)


class RetainedDependencyRecoveryTests(unittest.TestCase):
    def pinned_bytes(self, name, expected_sha):
        path = ROOT / name
        self.assertFalse(path.is_symlink(), name)
        self.assertTrue(path.is_file(), name)
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), expected_sha, name)
        return raw

    def recovery(self):
        path = ROOT / RECOVERY
        if not path.exists() and not path.is_symlink():
            self.skipTest("private recovery attestation is not installed")
        return json.loads(self.pinned_bytes(RECOVERY, RECOVERY_SHA))

    def bound_json(self, recovery, name):
        self.assertIn(name, recovery["inputs"])
        return json.loads(self.pinned_bytes(name, recovery["inputs"][name]))

    def test_exact_recovered_object_is_data_not_rewritten_history(self):
        recovery = self.recovery()
        self.assertEqual(recovery["destination"], {
            "path": EFFECTS, "bytes": 2216, "sha256": EFFECTS_SHA,
        })
        self.assertEqual(len(self.pinned_bytes(EFFECTS, EFFECTS_SHA)), 2216)
        self.assertIs(recovery["new_native_reproduction"], True)
        self.assertEqual(recovery["native_invocations"], 1)
        self.assertEqual(recovery["fresh_carrier"], "EFRC222")
        for key in (
            "original_producer_receipts_recreated",
            "original_proof_pins_changed",
            "original_filesystem_mtime_claimed",
            "binary_bytes_patched",
        ):
            self.assertIs(recovery[key], False, key)

    def test_all_fresh_recovery_inputs_still_match_attested_hashes(self):
        recovery = self.recovery()
        self.assertEqual(len(recovery["inputs"]), 10)
        for name, expected_sha in recovery["inputs"].items():
            with self.subTest(path=name):
                self.pinned_bytes(name, expected_sha)

    def test_fresh_completion_retains_bounded_nonacceptance_scope(self):
        recovery = self.recovery()
        completion = self.bound_json(recovery, OUTPUT + "completion.json")
        self.assertIs(completion["complete"], True)
        self.assertEqual(completion["errors"], [])
        self.assertEqual(completion["native_invocations"], 1)
        self.assertEqual(completion["phases"], ["compile_effects"])
        self.assertIs(completion["owned_lock_released"], True)
        for key in ("source_acceptance", "exact_acceptance", "full_historical_replay", "runtime_run"):
            self.assertIs(completion[key], False, key)
        verification = self.bound_json(recovery, OUTPUT + "object-verification.json")
        self.assertEqual(verification["bytes"], 2216)
        self.assertEqual(verification["sha256"], EFFECTS_SHA)
        self.assertEqual(verification["record_count"], 48)
        self.assertIs(verification["whole_omf_sha_equal"], True)
        self.assertIs(verification["historical_receipts_reconstructed"], False)
        self.assertIs(verification["normalized_bytes"], False)

    def test_fresh_phase_cleanup_and_registry_records_remain_clean(self):
        recovery = self.recovery()
        phase = self.bound_json(recovery, OUTPUT + "compile_effects-finished.json")
        self.assertIs(phase["ok"], True)
        self.assertEqual(phase["exit_code"], 0)
        self.assertEqual(phase["survivors"], [])
        self.assertEqual(phase["errors"], [])
        for key in ("timeout", "cleanup_uncertain", "poison"):
            self.assertIs(phase[key], False, key)
        registry = self.bound_json(recovery, OUTPUT + "compile_effects-registry-transition.json")
        self.assertIs(registry["ok"], True)
        self.assertEqual(registry["errors"], [])

    def test_confirmed_archive_receipt_set_is_restored_exactly(self):
        # Only these four receipts are claimed, never the entire proof closure.
        receipt_paths = [
            ".analysis/dependency-recovery-20261022-v01/archive-restoration-" + number + ".json"
            for number, _, _ in ARCHIVE_RECEIPTS
        ]
        if not any((ROOT / name).exists() or (ROOT / name).is_symlink() for name in receipt_paths):
            self.skipTest("private archive restoration receipts are not installed")
        rows = []
        for name, (_, digest, count) in zip(receipt_paths, ARCHIVE_RECEIPTS):
            receipt = json.loads(self.pinned_bytes(name, digest))
            members = receipt.get("members", [receipt.get("member")])
            self.assertEqual(len(members), count)
            rows.extend(members)
        self.assertEqual(len({row["path"] for row in rows}), 32)
        self.assertEqual(sum(row["bytes"] for row in rows), 9370166)
        for row in rows:
            with self.subTest(path=row["path"]):
                self.assertEqual(len(self.pinned_bytes(row["path"], row["sha256"])), row["bytes"])
                restored = (ROOT / row["path"]).stat()
                self.assertEqual(stat.S_IMODE(restored.st_mode), row["mode"])
                self.assertEqual(restored.st_mtime_ns, row["mtime_ns"])

    def test_failed_predecessor_remains_a_zero_native_failure(self):
        self.recovery()
        failed = json.loads(self.pinned_bytes(FAILED_COMPLETION, FAILED_SHA))
        self.assertIs(failed["complete"], False)
        self.assertEqual(failed["native_invocations"], 0)
        self.assertTrue(failed["errors"])
        self.assertIs(failed["owned_lock_released"], True)
        for key in ("source_acceptance", "exact_acceptance", "full_historical_replay"):
            self.assertIs(failed[key], False, key)


if __name__ == "__main__":
    unittest.main()
