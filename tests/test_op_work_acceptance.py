"""Acceptance refuses stale inputs, missing gates and altered owner metadata."""

from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.op_work_acceptance import PUBLICATION, verify
from lib.op_decoded_progress import decoded_summary, op_decoded_status


@unittest.skipUnless((ROOT / PUBLICATION).is_file()
                     and (ROOT / ".analysis/work/op-build.json").is_file()
                     and (ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe").is_file(),
                     "current private source proof absent")
class OpWorkAcceptance(unittest.TestCase):
    def setUp(self):
        self.publication = json.loads((ROOT / PUBLICATION).read_bytes())

    def test_live_physical_replay_accepts_only_current_decoded_owners(self):
        result = verify(ROOT, self.publication)
        self.assertEqual((result["decoded_exact_units"], result["decoded_authored_bytes"]), (59, 14758))
        self.assertFalse(result["canonical_credit_changed"])
        self.assertFalse(result["product_exact"])
        self.assertIn("59 extents / 92 procedures / 14,758 bytes (13,221 CODE + 1,537 initialized DATA)", decoded_summary(result))

    def test_stale_verifier_hash_fails_before_physical_replay(self):
        self.publication["proof_inputs"]["scripts/lib/op_work_acceptance.py"] = "0" * 64
        with patch("lib.op_work_acceptance.audit") as physical:
            with self.assertRaisesRegex(ValueError, "verifier input drift"):
                verify(ROOT, self.publication)
            physical.assert_not_called()

    def test_missing_one_required_gate_cannot_publish_an_owner(self):
        owner = next(iter(self.publication["owner_oracles"].values()))
        owner.pop(next(iter(owner)))
        with patch("lib.op_work_acceptance.audit", return_value=self.publication["audit"]):
            with self.assertRaisesRegex(ValueError, "gate witness binding"):
                verify(ROOT, self.publication)

    def test_unit_oracle_cannot_be_broadened_to_an_artifact_claim(self):
        owner = next(iter(self.publication["owner_oracles"].values()))
        row, = [r for r in owner.values() if r["oracle"] == "boundary-ownership"]
        row["unit_id"] = ""
        row["extent_size"] = ""
        with patch("lib.op_work_acceptance.audit", return_value=self.publication["audit"]):
            with self.assertRaisesRegex(ValueError, "gate witness binding"):
                verify(ROOT, self.publication)

    def test_replacing_the_decoded_owner_digest_is_rejected(self):
        current = deepcopy(self.publication["audit"])
        self.publication["audit"]["scope"]["owners"][0]["candidate_sha256"] = "0" * 64
        with patch("lib.op_work_acceptance.audit", return_value=current):
            with self.assertRaisesRegex(ValueError, "physical audit drift"):
                verify(ROOT, self.publication)

    def test_current_summary_does_not_relabel_the_historical_cohort(self):
        import csv
        with (ROOT / "config/units.csv").open() as stream:
            units = list(csv.DictReader(stream))
        result = op_decoded_status(ROOT, units)
        self.assertEqual(result["decoded_exact_unit_ids"], sorted(self.publication["owner_oracles"]))
        self.assertEqual(result["decoded_exact_units"], 59)
