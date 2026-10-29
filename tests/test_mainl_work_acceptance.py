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
        with patch('lib.decoded_mainl_acceptance.runtime', side_effect=AssertionError('ancestor runtime must remain historical')):
            result = verify(ROOT, self.publication)
        self.assertEqual((result["decoded_exact_units"], result["decoded_authored_bytes"]), (182, 16695))
        self.assertEqual(result["decoded_authored_procedures"],100)
        self.assertEqual(result["decoded_authored_code_bytes"],16471)
        self.assertEqual(result["decoded_authored_initialized_data_bytes"],224)
        self.assertFalse(result["product_exact"])
        self.assertEqual(result["mixed_physical_exact_bytes"], 0)
        units = list(csv.DictReader((ROOT / "config/units.csv").read_text().splitlines()))
        self.assertEqual(mainl_product_status(ROOT, units)["decoded_exact_units"], 182)
        self.assertEqual((result['decoded_library_exact_units'], result['decoded_library_bytes']), (87, 12386))
        self.assertEqual((result['decoded_procedures'], result['decoded_source_bytes'], result['decoded_code_bytes']), (243, 29081, 27497))
        self.assertEqual(result['decoded_initialized_data_bytes'], 1584)
        registration = self.publication['audit']['scope']['registration']['layout']
        self.assertEqual((registration['functions'], registration['code_bytes'],
                          len(registration['ordered_native_fields'])), (14, 2720, 188))
        self.assertFalse(registration['context_credited'])

    def test_stale_verifier_hash_fails_before_the_physical_audit(self):
        self.publication["proof_inputs"]["scripts/lib/decoded_mainl_acceptance.py"] = "0" * 64
        with patch("lib.decoded_mainl_acceptance.audit") as physical:
            with self.assertRaisesRegex(ValueError, "verifier input drift"):
                verify(ROOT, self.publication)
            physical.assert_not_called()

    def test_compound_owner_keeps_extent_and_procedure_counts_separate(self):
        with patch('lib.decoded_mainl_acceptance.audit', return_value=self.publication['audit']):
            result=verify(ROOT,self.publication)
        owner,=[o for o in self.publication['audit']['scope']['owners'] if o['unit_id']=='th03-mainl-decoded-snow-cluster']
        self.assertEqual((owner['size'],owner['procedure_count'],len(owner['procedures'])),(464,7,7))
        self.assertEqual((result['decoded_exact_units'],result['decoded_authored_procedures']),(182,100))

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
            svg = progress.render_svg(units, [], [], op_status={'decoded_accepted': False},
                                      zun_status={'decoded_accepted': False})
        self.assertIn("Decoded acceptance: exact 182/211", svg)
        self.assertIn("182 extents / 243 procedures / 29,081 B", svg)
        self.assertIn("CODE 27,497 / DATA 1,584", svg)
        self.assertIn("938 raw outputs", svg)
        self.assertNotIn("MAINL product + decoded accepted", svg)
        self.assertNotIn("exact 150/150", svg)
