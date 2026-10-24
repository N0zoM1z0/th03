"""The current -3 proof cannot borrow parent offsets, other payloads or stale code."""

from copy import deepcopy
import csv
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.decoded_zun_acceptance import PUBLICATION, verify, runtime_witness
from status import zun_product_status


@unittest.skipUnless((ROOT / PUBLICATION).is_file()
                     and (ROOT / ".analysis/work/zun-build.json").is_file()
                     and (ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN/product/zun.target.com").is_file(),
                     "private current ZUN source proof absent")
class CurrentZunAcceptance(unittest.TestCase):
    def setUp(self):
        self.publication = json.loads((ROOT / PUBLICATION).read_bytes())

    def test_physical_replay_accepts_only_ten_inner_logo_functions(self):
        result = verify(ROOT, self.publication)
        self.assertEqual((result["decoded_exact_units"], result["decoded_authored_bytes"]), (10, 1299))
        self.assertEqual(result["payload_option"], "-3")
        self.assertFalse(result["product_exact"])
        self.assertEqual(result["mixed_physical_exact_bytes"], 0)
        self.assertTrue(result["full_runtime_witness_bound"])

    def test_stale_verifier_is_rejected_before_replay(self):
        self.publication["proof_inputs"]["scripts/lib/decoded_zun_acceptance.py"] = "0" * 64
        with patch("lib.decoded_zun_acceptance.audit") as physical:
            with self.assertRaisesRegex(ValueError, "verifier input drift"): verify(ROOT, self.publication)
            physical.assert_not_called()

    def test_missing_gate_or_wrong_artifact_is_rejected(self):
        before = deepcopy(self.publication)
        for wrong_artifact in (False, True):
            self.publication = deepcopy(before)
            owner = next(iter(self.publication["owner_oracles"].values()))
            if wrong_artifact:
                row, = [r for r in owner.values() if r["oracle"] == "raw-bytes"]
                row["artifact"] = "th03-op"
            else: owner.pop(next(iter(owner)))
            with patch("lib.decoded_zun_acceptance.audit", return_value=self.publication["audit"]):
                with self.assertRaisesRegex(ValueError, "gate witness binding"): verify(ROOT, self.publication)

    def test_child_coordinates_cannot_be_fabricated_as_canonical_offsets(self):
        before = deepcopy(self.publication["audit"])
        self.publication["audit"]["scope"]["owners"][0]["canonical_file_offset"] = 0x367
        with patch("lib.decoded_zun_acceptance.audit", return_value=before):
            with self.assertRaisesRegex(ValueError, "physical audit drift"): verify(ROOT, self.publication)

    def test_complete_runtime_witness_is_required_without_replaying_long_fades(self):
        scope = deepcopy(self.publication["audit"]["scope"])
        scope["runtime"]["cases_per_image"] -= 1
        with self.assertRaisesRegex(ValueError, "runtime dimensions"): runtime_witness(scope)

    def test_partial_caller_inventory_cannot_inherit_live_acceptance(self):
        with (ROOT / "config/units.csv").open() as stream: units = list(csv.DictReader(stream))
        units = [u for u in units if u["id"] != "th03-zun-decoded-logo-main"]
        with patch("lib.decoded_zun_acceptance.verify") as accepted:
            self.assertEqual(zun_product_status(ROOT, units)["decoded_exact_units"], 0)
            accepted.assert_not_called()

    def test_svg_separates_inner_logo_source_from_whole_product(self):
        import progress
        with (ROOT / "config/units.csv").open() as stream: units = list(csv.DictReader(stream))
        result = verify(ROOT, self.publication)
        svg = progress.render_svg(units, [], [], zun_status=result)
        self.assertIn("Decoded extents 10/18", svg)
        self.assertIn("10 functions / 1,299 B", svg)
        self.assertIn("18 guest mutations rejected", svg)
        self.assertNotIn("10 target differences", svg)
        self.assertIn("whole-game totals remain unknown", svg)
