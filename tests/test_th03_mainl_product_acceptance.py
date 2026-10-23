"""Actual reviewed replay fixture; mutations are in-memory negative tests only."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / 'config/mainl_product_acceptance/publication.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import copy
import contextlib
import io
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path.cwd()
SOURCE = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, SOURCE / ('scripts/lib/' + name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
v = load('mainl_product_acceptance')
scope = load('mainl_product_scope')
P = json.loads((SOURCE / v.PUBLICATION).read_text())
R = json.loads((SOURCE / P['receipt']['path']).read_text())
class Tests(unittest.TestCase):
    def verify(self, publication=None):
        return v.verify(ROOT, publication or P, SOURCE, allow_review=True)
    def mutated_receipt(self, receipt):
        original = v.checked
        def checked(root, pin, source_root=None):
            if pin == P['receipt']:
                # Isolate structural gates after the separately tested digest gate.
                return json.dumps(receipt).encode()
            return original(root, pin, source_root)
        with patch.object(v, 'checked', checked):
            with self.assertRaises(v.AcceptanceError): self.verify()
    def test_actual_all_scoped_owners_and_product(self):
        status = self.verify()
        self.assertTrue(status['reviewed_proof_ready'])
        self.assertEqual(status['mixed_authored_credit_bytes'], 0)
        self.assertIsNone(status['whole_game_percentage'])
        if P['state'] == 'repository-local-accepted':
            self.assertEqual((status['mixed_physical_exact_bytes'], status['decoded_exact_units'], status['decoded_authored_bytes'], status['decoded_library_bytes']), (37975, 145, 27753, 628))
        self.assertEqual(len(R['decoded_owners']), 145)
        self.assertEqual(len(R['oracle_evidence']), 11)
        self.assertTrue(all(len(r['oracle_evidence']) == 11 for r in R['decoded_owners']))
    def test_review_state_never_credits_exact(self):
        if P['state'] != 'review-ready':
            self.assertTrue(self.verify()['product_exact']); return
        p = copy.deepcopy(P)
        result = self.verify(p)
        self.assertEqual((result['mixed_physical_exact_bytes'], result['decoded_exact_units']), (0, 0))
        with self.assertRaises(v.AcceptanceError): v.verify(ROOT, p, SOURCE)
    def test_publication_cannot_promote_a_review_only_receipt(self):
        p = copy.deepcopy(P)
        p['state'] = 'review-ready' if P['state'] == 'repository-local-accepted' else 'repository-local-accepted'
        with self.assertRaises(v.AcceptanceError): self.verify(p)
    def test_source_pin_drift(self):
        p = copy.deepcopy(P); p['input_bindings'][0]['sha256'] = '0' * 64
        with self.assertRaises(v.AcceptanceError): self.verify(p)
    def test_receipt_digest_drift(self):
        p = copy.deepcopy(P); p['receipt']['sha256'] = '0' * 64
        with self.assertRaises(v.AcceptanceError): self.verify(p)
    def test_missing_validator_binding(self):
        p = copy.deepcopy(P); p['input_bindings'] = [x for x in p['input_bindings'] if x['path'] != 'scripts/lib/mainl_owner_migrations.py']
        with self.assertRaises(v.AcceptanceError): self.verify(p)
    def test_every_product_oracle_is_required(self):
        for key in R['oracle_evidence']:
            p = copy.deepcopy(R); p['oracle_evidence'][key]['result'] = 'fail'
            with self.subTest(key=key): self.mutated_receipt(p)
    def test_owner_oracle_failure(self):
        p = copy.deepcopy(R); next(iter(p['decoded_owners'][0]['oracle_evidence'].values()))['result'] = 'fail'
        self.mutated_receipt(p)
    def test_no_fake_packed_offset(self):
        p = copy.deepcopy(R); p['decoded_owners'][0]['canonical_file_offset'] = 0
        self.mutated_receipt(p)
    def test_no_mixed_authored_credit(self):
        p = copy.deepcopy(R); p['scope']['authored_credit_bytes'] = 37975
        self.mutated_receipt(p)
    def test_owner_gap_or_missing_boundary(self):
        for field, value in [('lineage_gaps', ['unbound producer']), ('reviewed_boundary', False), ('map_covered_bytes', 0)]:
            p = copy.deepcopy(R); p['decoded_owners'][0][field] = value
            with self.subTest(field=field): self.mutated_receipt(p)
    def test_missing_owner(self):
        p = copy.deepcopy(R); p['decoded_owners'].pop()
        self.mutated_receipt(p)
    def test_normal_tracking_rejects_a_malformed_present_publication(self):
        spec = importlib.util.spec_from_file_location('mainl_tracking_test', SOURCE / 'scripts/validate_tracking.py')
        tracking = importlib.util.module_from_spec(spec); spec.loader.exec_module(tracking)
        publication_path = ROOT / v.PUBLICATION
        old_exists, old_read = Path.exists, Path.read_text
        def exists(path): return True if path == publication_path else old_exists(path)
        def read(path, *args, **kwargs): return '{"schema":"invalid"}' if path == publication_path else old_read(path, *args, **kwargs)
        with patch.object(Path, 'exists', exists), patch.object(Path, 'read_text', read), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tracking.main(ROOT), 1)
            self.assertEqual(tracking.main(ROOT, validate_product=False), 0)
    def test_physical_union_counts_once_and_keeps_artifacts_separate(self):
        self.assertEqual(scope.union_bytes([('mainl', 0, 37975), ('mainl', 10, 50), ('main', 0, 50)], {'mainl': 37975, 'main': 100}), 38025)
        with self.assertRaises(scope.Invalid): scope.union_bytes([('decoded-mainl', 0, 50)], {'mainl': 37975})
if __name__ == '__main__': unittest.main()
