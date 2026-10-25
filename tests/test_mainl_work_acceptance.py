"""Current MAINL proof cannot broaden its decoded source owners or hide drift."""

from copy import deepcopy
import csv
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.decoded_mainl_acceptance import PUBLICATION, verify
from status import mainl_product_status


@unittest.skipUnless((ROOT / PUBLICATION).is_file()
                     and (ROOT / ".analysis/work/mainl-build.json").is_file()
                     and (ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ML/bin/th03/mainl.target.exe").is_file(),
                     "current private MAINL proof absent")
class MainlWorkAcceptance(unittest.TestCase):
    def setUp(self):
        self.publication = json.loads((ROOT / PUBLICATION).read_bytes())

    def test_live_physical_replay_accepts_current_decoded_owners_only(self):
        result = verify(ROOT, self.publication)
        self.assertEqual((result["decoded_exact_units"], result["decoded_authored_bytes"]), (43, 3381))
        self.assertFalse(result["product_exact"])
        self.assertEqual(result["mixed_physical_exact_bytes"], 0)

    def test_stale_verifier_hash_fails_before_the_physical_audit(self):
        self.publication["proof_inputs"]["scripts/lib/decoded_mainl_acceptance.py"] = "0" * 64
        with patch("lib.decoded_mainl_acceptance.audit") as physical:
            with self.assertRaisesRegex(ValueError, "verifier input drift"):
                verify(ROOT, self.publication)
            physical.assert_not_called()

    def test_one_missing_gate_rejects_the_owner(self):
        owner = next(iter(self.publication["owner_oracles"].values()))
        owner.pop(next(iter(owner)))
        with patch("lib.decoded_mainl_acceptance.audit", return_value=self.publication["audit"]):
            with self.assertRaisesRegex(ValueError, "gate witness binding"):
                verify(ROOT, self.publication)

    def test_wrong_artifact_cannot_inherit_a_unit_gate(self):
        owner = next(iter(self.publication["owner_oracles"].values()))
        row, = [r for r in owner.values() if r["oracle"] == "raw-bytes"]
        row["artifact"] = "th03-main"
        with patch("lib.decoded_mainl_acceptance.audit", return_value=self.publication["audit"]):
            with self.assertRaisesRegex(ValueError, "gate witness binding"):
                verify(ROOT, self.publication)

    def test_vendor_header_or_owner_digest_drift_is_rejected(self):
        before = deepcopy(self.publication["audit"])
        name = next(iter(self.publication["audit"]["vendor_header_sha256"]))
        self.publication["audit"]["vendor_header_sha256"][name] = "0" * 64
        with patch("lib.decoded_mainl_acceptance.audit", return_value=before):
            with self.assertRaisesRegex(ValueError, "physical audit drift"):
                verify(ROOT, self.publication)

    def test_partial_caller_inventory_does_not_inherit_live_acceptance(self):
        with (ROOT / "config/units.csv").open() as stream:
            units = list(csv.DictReader(stream))
        units = [u for u in units if u["id"] != "th03-mainl-decoded-lifecycle-init"]
        with patch("lib.decoded_mainl_acceptance.verify") as accepted:
            self.assertEqual(mainl_product_status(ROOT, units)["decoded_exact_units"], 0)
            accepted.assert_not_called()

    def test_current_svg_separates_decoded_owners_from_product_acceptance(self):
        import progress
        import status
        with (ROOT / "config/units.csv").open() as stream:
            units = list(csv.DictReader(stream))
        result = verify(ROOT, self.publication)
        with patch.object(status, "mainl_product_status", return_value=result):
            svg = progress.render_svg(units, [], [])
        self.assertIn("Decoded acceptance: exact 43/149", svg)
        self.assertIn("43 functions / 3,381 B", svg)
        self.assertIn("938 raw outputs", svg)
        self.assertNotIn("MAINL product + decoded accepted", svg)
        self.assertNotIn("exact 149/149", svg)
