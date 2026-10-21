"""Retained source proof replay is not a new native or full hardware run."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("regist_source_proof", ROOT / "scripts/replay_th03_mainl_regist.py")
proof = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proof)

class RegistSourceProofTests(unittest.TestCase):
    def test_replay_retained_pair_with_honest_scope(self):
        result = proof.replay()
        self.assertTrue(result["checks_pass"])
        self.assertEqual(result["compiled_source_materializations"], 2)
        self.assertEqual(result["retained_other_objects"], 31)
        self.assertEqual(result["native_invocations_this_replay"], 0)
        self.assertFalse(result["cold_whole_program"])
        self.assertFalse(result["whole_runtime_proved"])
        self.assertFalse(result["exact_acceptance"])
        detail = result["linked_diagnostics"]
        self.assertEqual(detail["registration_scoredat_extents"][0]["raw_difference_offsets"], [])
        self.assertEqual(detail["registration_scoredat_extents"][1]["raw_difference_offsets"], [0x19e2,0x19ec,0x22d8,0x22e2,0x230f,0x2319])
        self.assertEqual(detail["all_ordered_relocation_count"], 677)
        self.assertEqual([x["entry_calls"] for x in detail["runtime_runs"]], [152, 152, 152])

    def test_wrong_current_owner_binding_rejected(self):
        manifest = copy.deepcopy(proof.retained_json(proof.FIRST + "/manifest.json"))
        manifest["sources"]["src/mainl/regist.cpp"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "identity differs"):
            proof.source_bindings(manifest)

    def test_uncertain_native_result_rejected(self):
        good = {"exit_code": 0, "timeout": False, "cleanup_uncertain": False,
                "poison": False, "initial_inventory_complete": True,
                "inventory_complete": True, "survivors": [], "errors": []}
        proof.native_finished(good)
        for key, value in {"exit_code": 1, "timeout": True, "cleanup_uncertain": True,
                           "inventory_complete": False, "survivors": [123], "errors": ["failed"]}.items():
            result = dict(good); result[key] = value
            with self.assertRaises(ValueError):
                proof.native_finished(result)

    def test_retained_pin_mutation_rejected(self):
        with self.assertRaisesRegex(ValueError, "identity differs"):
            proof.read_verified(proof.LINKED + "/completion.json", "0" * 64)

if __name__ == "__main__":
    unittest.main()
