"""Owner/layout checks; historical bindings attest their original inputs."""

import copy
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from th03_cpu_default_fixture import historical_default_bytes
from lib import th03_yumemi_charge_candidate as charge
from replay_th03_main_exact_units import (
    normalized_code_extents,
    verify_disjoint_ownership,
)


class ChargeDefault(unittest.TestCase):
    def setUp(self):
        self.old = tomllib.loads(historical_default_bytes().decode())
        self.new = tomllib.loads(
            (ROOT / "config/th03_main_exact_units.toml").read_text()
        )
        self.candidate = tomllib.loads((ROOT / charge.CANDIDATE_PATH).read_text())
        self.historical = copy.deepcopy(self.old)
        self.historical["units"] += copy.deepcopy(self.candidate["units"])
        self.historical["functions"] += copy.deepcopy(self.candidate["functions"])

    def test_current_charge_owner_matches_candidate(self):
        ids = {u["id"] for u in self.candidate["units"]}
        objects = {u["object"] for u in self.candidate["units"]}
        self.assertEqual(
            [u for u in self.new["units"] if u["id"] in ids], self.candidate["units"]
        )
        self.assertEqual(
            [f for f in self.new["functions"] if f["object"] in objects],
            self.candidate["functions"],
        )

    def test_prior_code_geometry_and_abi_preserved(self):
        def coverage(config):
            spans = sorted(
                (
                    e["segment"] * 16 + e["start"],
                    e["segment"] * 16 + e["start"] + e["size"],
                )
                for unit in config["units"]
                for e in normalized_code_extents(unit, config["segment"])
            )
            merged = []
            for lo, hi in spans:
                if merged and lo <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(hi, merged[-1][1]))
                else:
                    merged.append((lo, hi))
            return merged

        current_coverage = coverage(self.new)
        for lo, hi in coverage(self.old):
            self.assertTrue(
                any(start <= lo and hi <= end for start, end in current_coverage)
            )
        fields = ("name", "segment", "offset", "size", "abi")
        geometry = lambda f: tuple(
            f.get(k, self.new["segment"] if k == "segment" else None) for k in fields
        )
        current_functions = {geometry(f) for f in self.new["functions"]}
        self.assertTrue(
            all(geometry(f) in current_functions for f in self.old["functions"])
        )
        verify_disjoint_ownership(
            {
                u["id"]: normalized_code_extents(u, self.new["segment"])
                for u in self.new["units"]
            }
        )

    def test_historical_binding_does_not_attest_new_producer(self):
        before = copy.deepcopy(self.historical)
        bound, _ = charge.bind_default(self.historical)
        self.assertEqual(bound, self.historical)
        self.assertEqual(before, self.historical)
        with self.assertRaisesRegex(ValueError, "configuration drift"):
            charge.bind_default(self.new)

    def test_changed_owner_rejected(self):
        bad = copy.deepcopy(self.historical)
        bad["units"][-1]["code_extents"][0]["size"] += 1
        with self.assertRaises(ValueError):
            charge.bind_default(bad)

    def test_changed_prior_scope_rejected(self):
        bad = copy.deepcopy(self.historical)
        bad["units"][0]["size"] += 1
        with self.assertRaises(ValueError):
            charge.bind_default(bad)

    def test_duplicate_charge_candidate_rejected(self):
        with self.assertRaises(ValueError):
            charge.bind_candidate(self.new, self.candidate, charge.CANDIDATE_PATH)


if __name__ == "__main__":
    unittest.main()
