"""Current -3/-5 proofs cannot borrow parent offsets or stale ownership/code."""

from copy import deepcopy
import csv
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.decoded_zun_acceptance import PUBLICATION, verify, runtime_witness, resident_witness, init_witness, driver_witness, command_witness
from status import zun_product_status


@unittest.skipUnless((ROOT / PUBLICATION).is_file()
                     and (ROOT / ".analysis/work/zun-build.json").is_file()
                     and (ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN/product/zun.target.com").is_file(),
                     "private current ZUN source proof absent")
class CurrentZunAcceptance(unittest.TestCase):
    def setUp(self):
        self.publication = json.loads((ROOT / PUBLICATION).read_bytes())

    def test_physical_replay_accepts_all_current_bounded_decoded_scopes(self):
        result = verify(ROOT, self.publication)
        self.assertEqual((result["decoded_exact_units"], result["decoded_authored_bytes"]), (72, 1621))
        self.assertEqual(result["decoded_library_bytes"], 4140)
        self.assertEqual(result["decoded_library_data_bytes"], 1294)
        self.assertEqual(result["decoded_original_asm_bytes"], 1390)
        self.assertEqual((result["decoded_procedures"], result["decoded_code_bytes"]), (76, 5074))
        self.assertEqual(result["payload_options"], ["-2", "-3", "-4", "-5"])
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

    def test_resident_runtime_cannot_reuse_logo_witness(self):
        scope = deepcopy(self.publication["audit"]["scope"]["resident"])
        scope["runtime"]["executed_owner_bytes"] = 1299
        with self.assertRaisesRegex(ValueError, "resident runtime dimensions"):
            resident_witness(scope)

    def test_resident_owner_cannot_use_a_logo_coordinate(self):
        before = deepcopy(self.publication["audit"])
        owner, = [o for o in self.publication["audit"]["scope"]["owners"] if o["unit_id"] == "th03-zun-decoded-resident-main"]
        self.assertEqual(owner["payload_option"], "-5")
        owner["payload_option"] = "-3"
        with patch("lib.decoded_zun_acceptance.audit", return_value=before):
            with self.assertRaisesRegex(ValueError, "physical audit drift"): verify(ROOT, self.publication)

    def test_original_asm_cannot_be_reclassified_as_new_authored_credit(self):
        scope = deepcopy(self.publication["audit"]["scope"]["init"])
        scope["layout"]["source_lineage"]["newly_authored_bytes"] = 607
        with self.assertRaisesRegex(ValueError, "source classification"): init_witness(scope)

    def test_full_conversion_domain_is_required_in_cold_witness(self):
        scope = deepcopy(self.publication["audit"]["scope"]["init"])
        scope["runtime"]["observations"][0]["conversions"]["cases"] = 256
        with self.assertRaisesRegex(ValueError, "init load/scalar"): init_witness(scope)

    def test_scalar_source_cannot_promote_enclosing_driver_or_reserved_spans(self):
        for key in ("enclosing_driver_accepted", "reserved_spans_owned"):
            scope = deepcopy(self.publication["audit"]["scope"]["driver"])
            scope["layout"][key] = True
            with self.assertRaisesRegex(ValueError, "bounded library source classification"): driver_witness(scope)

    def test_driver_library_origin_cannot_be_changed_to_authored(self):
        scope = deepcopy(self.publication["audit"]["scope"]["driver"])
        scope["layout"]["owners"][0]["origin"] = "authored"
        with self.assertRaisesRegex(ValueError, "bounded library source classification"): driver_witness(scope)

    def test_command_witness_requires_complete_code_and_bounded_library_origin(self):
        for key,value in (("executed_owner_bytes",360),("cases_per_image",6677)):
            scope=deepcopy(self.publication["audit"]["scope"]["command"])
            scope["runtime"][key]=value
            with self.assertRaisesRegex(ValueError,"command runtime dimensions"): command_witness(scope)
        scope=deepcopy(self.publication["audit"]["scope"]["command"])
        scope["layout"]["reserved_spans_owned"]=True
        with self.assertRaisesRegex(ValueError,"bounded command library"): command_witness(scope)

    def test_svg_separates_inner_logo_source_from_whole_product(self):
        import progress
        with (ROOT / "config/units.csv").open() as stream: units = list(csv.DictReader(stream))
        result = verify(ROOT, self.publication)
        svg = progress.render_svg(units, [], [], zun_status=result)
        self.assertIn("Decoded extents 72/77", svg)
        self.assertIn("5,074 CODE B", svg)
        self.assertIn("ASM/library separate", svg)
        self.assertIn("156 instruction + 6 DATA runtime mutations", svg)
        self.assertNotIn("10 target differences", svg)
        self.assertIn("whole-game totals remain unknown", svg)
