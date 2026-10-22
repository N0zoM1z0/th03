"""Offline raster receipt replay and fail-closed mutation coverage."""
from pathlib import Path
from copy import deepcopy
import importlib.util
import json
import os
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(os.environ.get('TH03_OP_RASTER_REPO_ROOT', Path.cwd())).resolve()
SOURCE_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('raster_replay_under_test',
        SOURCE_ROOT / 'scripts/replay_th03_op_raster.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
PROOF = json.loads((SOURCE_ROOT / 'config/op_raster/proof.json').read_bytes())
M = json.loads((ROOT / r.PROPOSAL / 'manifest.json').read_bytes())
REPORT = json.loads((ROOT / r.OUT / 'linked-verification.json').read_bytes())
AUDIT_RESULT = json.loads((ROOT / r.AUDIT / 'audit-result.json').read_bytes())


def load_correction():
    raw = (ROOT / r.AUDIT / 'audit.py').read_bytes()
    assert r.sha(raw) == r.AUDIT_CODE_SHA
    spec = importlib.util.spec_from_file_location('raster_correction_under_test',
            ROOT / r.AUDIT / 'audit.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CORRECTION = load_correction()
EXPECTED = {x['id']: dict(target_raw_equal=x['baseline_target_raw_equal'],
    target_ordered_equal=x['baseline_target_ordered_equal'],
    target_sha256=REPORT['prior_owners'][i]['target_sha256'],
    baseline_sha256=REPORT['prior_owners'][i]['baseline_sha256'])
    for i, x in enumerate(AUDIT_RESULT['corrected_diagnostic']['prior_baseline_comparisons'])}


class RasterReplayTests(unittest.TestCase):
    def test_full_pinned_offline_replay(self):
        result = r.replay(ROOT, PROOF, SOURCE_ROOT)
        self.assertTrue(result['pass_checks'])
        self.assertEqual(result['native_invocations_now'], 0)
        self.assertEqual(result['candidate_sha256'], r.EXE_SHA)
        self.assertFalse(result['original_runner_complete'])
        self.assertFalse(result['original_diagnostic_checks_pass'])
        self.assertTrue(result['separate_offline_correction_pass'])
        self.assertEqual(result['total_source_bodies'], 44)
        self.assertEqual(result['total_source_bytes'], 12940)
        self.assertEqual(result['whole_ordered_relocation_differences'], 313)

    def test_original_false_report_valid(self):
        r.validate_report(REPORT)

    def test_original_report_not_mutated(self):
        before = deepcopy(REPORT)
        got = CORRECTION.aggregate(REPORT, EXPECTED)
        self.assertEqual(got, AUDIT_RESULT['corrected_diagnostic'])
        self.assertEqual(REPORT, before)
        self.assertFalse(got['original_diagnostic_checks_pass'])

    def test_selection_negative_preserved(self):
        got = CORRECTION.aggregate(REPORT, EXPECTED)['known_prior_target_negatives']
        self.assertEqual(len(got), 1)
        self.assertEqual(got[0]['id'], 'th03-op-decoded-character-selection')
        self.assertFalse(got[0]['baseline_target_ordered_equal'])
        self.assertFalse(got[0]['candidate_target_ordered_equal'])

    def test_selection_target_order_flip_rejected_by_correction(self):
        x = deepcopy(REPORT)
        next(q for q in x['prior_owners'] if q['id'] ==
             'th03-op-decoded-character-selection')['target_ordered_equal'] = True
        self.assertFalse(CORRECTION.aggregate(x, EXPECTED)['diagnostic_checks_pass'])

    def test_expected_baseline_flip_rejected_by_correction(self):
        expected = deepcopy(EXPECTED)
        expected['th03-op-decoded-character-selection']['target_ordered_equal'] = True
        self.assertFalse(CORRECTION.aggregate(REPORT, expected)['diagnostic_checks_pass'])

    def test_prior_count_mutation_rejected(self):
        x = deepcopy(REPORT)
        x['prior_owners'].pop()
        with self.assertRaises(ValueError):
            CORRECTION.aggregate(x, EXPECTED)

    def test_duplicate_prior_id_rejected(self):
        x = deepcopy(REPORT)
        x['prior_owners'][1]['id'] = x['prior_owners'][0]['id']
        with self.assertRaises(ValueError):
            CORRECTION.aggregate(x, EXPECTED)

    def test_complete_input_closure(self):
        inv = json.loads((ROOT / PROOF['inventory']['path']).read_bytes())
        pins = {x['path'] for x in inv['pins']}
        self.assertTrue(r.required_paths(M) <= pins)
        self.assertIn(r.AUDIT + '/audit-result.json', pins)
        self.assertIn(r.AUDIT + '/replay-pins.json', pins)
        self.assertIn(M['verification_helpers']['path'], pins)
        baseline = Path(M['baseline_exe']['path']).parents[2]
        self.assertIn(str(baseline / 'th03/op_music.cpp'), pins)
        self.assertIn(str(baseline / 'th03/op/m_main.cpp'), pins)
        self.assertEqual(len(pins), len(inv['pins']))
        self.assertEqual(set(PROOF['maintained_closure']), r.SOURCE_CLOSURE)
        self.assertEqual(len(r.SOURCE_CLOSURE), 5)
        self.assertEqual(set(PROOF['helper_closure']), r.HELPER_CLOSURE)
        self.assertEqual(len(r.HELPER_CLOSURE), 7)

    def test_receipts_not_rewritten(self):
        self.assertEqual(r.sha((ROOT / r.OUT / 'completion.json').read_bytes()),
                         AUDIT_RESULT['original_completion_sha256'])
        self.assertEqual(r.sha((ROOT / r.OUT / 'linked-verification.json').read_bytes()),
                         AUDIT_RESULT['original_report_sha256'])

    def test_missing_helper_rejected(self):
        p = deepcopy(PROOF)
        del p['helper_closure']['scripts/lib/__init__.py']
        with self.assertRaises(ValueError):
            r.validate_proof(p)

    def test_missing_maintained_rejected(self):
        p = deepcopy(PROOF)
        p['maintained_closure'].pop(next(iter(p['maintained_closure'])))
        with self.assertRaises(ValueError):
            r.validate_proof(p)

    def test_missing_context_rejected(self):
        p = deepcopy(PROOF)
        p['context_source_closure'].pop(next(iter(p['context_source_closure'])))
        with self.assertRaises(ValueError):
            r.guard_current(ROOT, p, SOURCE_ROOT, M)

    def test_unsafe_paths_rejected(self):
        for name in ('/tmp/example', '../example', 'src/../example', './example'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                r.regular(ROOT, name)

    def test_no_runner_or_audit_main_calls(self):
        import ast
        tree = ast.parse((SOURCE_ROOT / 'scripts/replay_th03_op_raster.py').read_text())
        calls = [ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)]
        self.assertNotIn('correction.main', calls)
        self.assertFalse(any(x.endswith('runner.guard') for x in calls))
        self.assertFalse(any(x.startswith(('subprocess.', 'os.system')) for x in calls))


def proof_mutation(key, value):
    def test(self):
        p = deepcopy(PROOF)
        p[key] = value
        with self.assertRaises(ValueError):
            r.validate_proof(p)
    return test


for name in r.FLAGS:
    setattr(RasterReplayTests, 'test_credit_' + name, proof_mutation(name, True))
for name in ('native_phases', 'fresh_owner_objects', 'new_owner_bytes',
             'retained_context_objects', 'preserved_prior_owners', 'preserved_prior_bytes',
             'excluded_alignment_bytes'):
    setattr(RasterReplayTests, 'test_scope_' + name, proof_mutation(name, PROOF[name] + 1))
for name in ('manifest_sha256', 'verifier_sha256', 'audit_sha256', 'historical_head'):
    setattr(RasterReplayTests, 'test_identity_' + name, proof_mutation(name, '0' * 64))
setattr(RasterReplayTests, 'test_original_failure_cannot_be_upgraded',
        proof_mutation('original_runner_complete', True))
setattr(RasterReplayTests, 'test_correction_cannot_be_erased',
        proof_mutation('separate_offline_correction', False))


def current_guard_mutation(name, base):
    def test(self):
        original = r.stable_read
        def changed(root, path):
            raw = original(root, path)
            return raw + b'\nMUTATION' if Path(root) == base and path == name else raw
        with patch.object(r, 'stable_read', side_effect=changed), self.assertRaises(ValueError):
            r.guard_current(ROOT, PROOF, SOURCE_ROOT, M)
    return test


for category, base, paths in [
        ('helper', ROOT, PROOF['helper_closure']),
        ('maintained', SOURCE_ROOT, PROOF['maintained_closure']),
        ('context', ROOT, PROOF['context_source_closure'])]:
    for i, name in enumerate(sorted(paths)):
        setattr(RasterReplayTests, 'test_preimport_%s_%03d' % (category, i),
                current_guard_mutation(name, base))


def prior_mutation(index, field):
    def test(self):
        x = deepcopy(REPORT)
        x['prior_owners'][index][field] = False
        self.assertFalse(CORRECTION.aggregate(x, EXPECTED)['diagnostic_checks_pass'])
    return test


for i in range(42):
    for key in ('baseline_raw_equal', 'baseline_ordered_equal', 'map_preserved'):
        setattr(RasterReplayTests, 'test_prior_%02d_%s' % (i, key), prior_mutation(i, key))


def report_mutation(path, value):
    def test(self):
        x = deepcopy(REPORT)
        dest = x
        for key in path[:-1]:
            dest = dest[key]
        dest[path[-1]] = value
        with self.assertRaises(ValueError):
            r.validate_report(x)
    return test


mutations = [
    (['diagnostic_checks_pass'], True), (['prior_owners_preserved'], True),
    (['candidate_sha256'], '0' * 64), (['new_raster_bytes'], 125),
    (['prior_owner_count'], 43), (['prior_owner_bytes'], 12817),
    (['native_invocations_now'], 1), (['whole_file_equal_target'], True),
    (['whole_program', 'target_different_bytes'], 0),
    (['whole_program', 'baseline_different_bytes'], 0),
    (['whole_ordered_relocations', 'target_equal'], True),
    (['whole_ordered_relocations', 'target_different_positions'], 0),
    (['excluded_vendor_alignment', 'candidate'], 0x90),
    (['excluded_vendor_alignment', 'authored_credit'], 1),
    (['new_raster_bodies', 0, 'target_raw_equal'], False),
    (['new_raster_bodies', 1, 'target_ordered_equal'], False),
    (['objects', 0, 'maintained_lineage_checked'], False),
    (['objects', 1, 'literal_non_data_omf_preserved'], False),
]
mutations += [([key], True) for key in ('source_acceptance', 'exact_acceptance',
    'source_progress_changed', 'whole_product_ownership', 'cold_build', 'runtime_run')]
for i, (path, value) in enumerate(mutations):
    setattr(RasterReplayTests, 'test_report_mutation_%02d' % i, report_mutation(path, value))


def phase_mutation(field, value):
    def test(self):
        phase = r.PHASES[0]
        start = json.loads((ROOT / r.OUT / (phase + '-started.json')).read_bytes())
        finish = json.loads((ROOT / r.OUT / (phase + '-finished.json')).read_bytes())
        env = json.loads((ROOT / r.OUT / 'environment.json').read_bytes())
        finish[field] = value
        with self.assertRaises(ValueError):
            r.validate_phase(phase, start, finish, M, env)
    return test


for key, value in [('exit_code', True), ('exit_code', 1), ('timeout', True),
    ('cleanup_uncertain', True), ('poison', True), ('initial_inventory_complete', False),
    ('inventory_complete', False), ('survivors', [1]), ('errors', ['test']), ('ok', False)]:
    setattr(RasterReplayTests, 'test_phase_' + key + '_' + str(value).replace(' ', ''),
            phase_mutation(key, value))


if __name__ == '__main__':
    unittest.main()
