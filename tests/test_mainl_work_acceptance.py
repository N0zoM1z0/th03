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
from lib.decoded_mainl_acceptance import PUBLICATION, proof_inputs, verify, covered_inventory
from status import mainl_product_status


class MainlInventoryCoverage(unittest.TestCase):
    def setUp(self):
        self.owners = [dict(unit_id='first', origin='authored', start=0x100, size=2, ordered_relocations=[]),
                       dict(unit_id='second', origin='authored', start=0x102, size=2, ordered_relocations=[])]
        self.unit = dict(id='aggregate', artifact='th03-mainl', state='source-present',
                         boundary_state='reviewed', origin='authored', segment='decoded:0010',
                         offset='0', size='4', compare_size='4')

    def test_complete_aggregate_references_existing_owners_without_mutating_them(self):
        before = deepcopy(self.owners)
        self.assertEqual(covered_inventory([self.unit], self.owners), {'aggregate': ['first', 'second']})
        self.assertEqual(self.owners, before)

    def test_one_unowned_byte_prevents_aggregate_coverage(self):
        self.owners[1]['size'] = 1
        self.assertEqual(covered_inventory([self.unit], self.owners), {})

    def test_range_cannot_cut_a_complete_relocation_word(self):
        self.owners[0].update(size=4, ordered_relocations=[[0x10, 1]])
        self.owners.pop()
        self.unit.update(offset='2', size='2', compare_size='2')
        self.assertEqual(covered_inventory([self.unit], self.owners), {})

    def test_overlapping_source_owners_are_rejected(self):
        self.owners[1]['start'] = 0x101
        with self.assertRaisesRegex(ValueError, 'disjoint accepted byte owners'):
            covered_inventory([self.unit], self.owners)


@unittest.skipUnless((ROOT / PUBLICATION).is_file()
                     and (ROOT / ".analysis/work/mainl-build.json").is_file()
                     and (ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ML/bin/th03/mainl.target.exe").is_file(),
                     "current private MAINL proof absent")
class MainlWorkAcceptance(unittest.TestCase):
    def setUp(self):
        self.publication = json.loads((ROOT / PUBLICATION).read_bytes())
        # In-memory gate fixture only: the physical audit is mocked in those
        # tests. The retained publication on disk is never refreshed.
        self.publication['proof_inputs'] = proof_inputs(ROOT)

    def test_live_publication_binds_current_native_refresh_without_product_credit(self):
        units = list(csv.DictReader((ROOT / 'config/units.csv').read_text().splitlines()))
        result = mainl_product_status(ROOT, units)
        self.assertTrue(result['current_cold_source_scopes'])
        self.assertFalse(result['product_exact'])
        self.assertEqual(set(result['decoded_exact_unit_ids']),
                         {o['unit_id'] for o in self.publication['audit']['scope']['owners']})
        self.assertEqual(result['native_refresh_stage'],
                         self.publication['audit']['scope']['current_native_refresh']['stage'])
        self.assertEqual(result['native_objects_rebuilt_per_round'], 2)

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
        # Native audit has its own live test; this case checks presentation.
        with patch('lib.decoded_mainl_acceptance.audit', return_value=self.publication['audit']):
            result = verify(ROOT, self.publication)
        with patch.object(status, "mainl_product_status", return_value=result):
            svg = progress.render_svg(units, [], [], op_status={'decoded_accepted': False},
                                      zun_status={'decoded_accepted': False})
        self.assertIn("938 raw outputs", svg)
        self.assertNotIn("MAINL product + decoded accepted", svg)
        self.assertNotIn("exact 150/150", svg)
