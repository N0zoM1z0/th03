"""Portable source/receipt guards; optional read-only retained-receipt replay."""
from pathlib import Path
import copy
import importlib.util
import inspect
import json
import os
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
REPO = Path(os.environ.get('TH03_REPLAY_REPO_ROOT', ROOT)).resolve()
spec = importlib.util.spec_from_file_location('op_remaining_proof',
        ROOT / 'scripts/replay_th03_op_remaining_helpers.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class ProofTests(unittest.TestCase):
    def setUp(self):
        self.p = json.loads((ROOT / 'config/op_remaining_helpers/proof.json').read_text())

    def test_real_compact_proof(self):
        replay.validate_proof(self.p)

    def test_every_credit_flag_rejected(self):
        for name in replay.FLAGS:
            p = copy.deepcopy(self.p)
            p[name] = True
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'credit inflation'):
                replay.validate_proof(p)

    def test_scope_inflation(self):
        for name in ('native_groups', 'native_phases', 'fresh_owner_objects', 'new_owner_bytes',
                     'retained_context_objects', 'preserved_prior_owners', 'preserved_prior_bytes',
                     'original_producer_context_bytes', 'excluded_alignment_bytes'):
            p = copy.deepcopy(self.p)
            p[name] += 1
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'bounded scope'):
                replay.validate_proof(p)

    def test_false_group_manifest_verifier_and_historical_head(self):
        for name, value in [('manifest_sha256', ['0' * 64, replay.MANIFEST_SHAS[1]]),
                            ('manifest_sha256', [replay.MANIFEST_SHAS[0], '0' * 64]),
                            ('verifier_sha256', '0' * 64), ('historical_head', '0' * 40)]:
            p = copy.deepcopy(self.p)
            p[name] = value
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'recipe identity'):
                replay.validate_proof(p)

    def test_missing_current_source_and_import_helper(self):
        for section, name in [('maintained_closure', 'src/op/core/initop.cpp'),
                              ('helper_closure', 'scripts/inventory_rec98_th03.py')]:
            p = copy.deepcopy(self.p)
            p[section].pop(name)
            with self.subTest(section=section), self.assertRaisesRegex(ValueError, 'current source/helper closure'):
                replay.validate_proof(p)

    def test_unrelated_historical_guard_forbidden(self):
        self.p['helper_closure']['docs/unrelated.md'] = {'sha256': '0' * 64, 'bytes': 0}
        with self.assertRaisesRegex(ValueError, 'current source/helper closure'):
            replay.validate_proof(self.p)

    def fixture(self, root):
        p = {'helper_closure': {}, 'maintained_closure': {}, 'context_source_closure': {}}
        m = {'sources': {}, 'repeat_inputs': {}}
        for section, names in [('helper_closure', replay.HELPER_CLOSURE),
                               ('maintained_closure', replay.SOURCE_CLOSURE),
                               ('context_source_closure', {'src/op/existing.cpp'})]:
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                body = ('safe fixture ' + name).encode()
                path.write_bytes(body)
                q = replay.values(body)
                p[section][name] = q
                if section != 'maintained_closure':
                    m['sources'][name] = dict(q, mode=420)
                if section == 'context_source_closure':
                    m['repeat_inputs'][name] = dict(q, mode=420)
        return p, m

    def test_complete_current_closure_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p, m = self.fixture(root)
            replay.guard_current(root, p, root, m)

    def test_every_maintained_and_import_file_mutation_precedes_import(self):
        for section, names in [('maintained_closure', replay.SOURCE_CLOSURE),
                               ('helper_closure', replay.HELPER_CLOSURE),
                               ('context_source_closure', {'src/op/existing.cpp'})]:
            for name in names:
                with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                    root = Path(d)
                    p, m = self.fixture(root)
                    (root / name).write_bytes(b'raise RuntimeError("must not execute")')
                    with self.assertRaisesRegex(ValueError, 'current '):
                        replay.guard_current(root, p, root, m)

    def test_false_native_helper_binding_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p, m = self.fixture(root)
            m['sources']['scripts/lib/omf.py']['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'current helper before import'):
                replay.guard_current(root, p, root, m)

    def test_retained_current_source_closure_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p, m = self.fixture(root)
            p['context_source_closure'] = {}
            with self.assertRaisesRegex(ValueError, 'current retained source closure'):
                replay.guard_current(root, p, root, m)

    def test_guards_precede_all_dynamic_imports(self):
        source = inspect.getsource(replay.replay)
        guard = source.index('guard_current(root, p, source_root, m)')
        self.assertLess(source.index('for n in pins:'), guard)
        self.assertLess(source.index('guard_pin_closure(pins, manifests, read)'), guard)
        for mark in ('stage = load(', 'policy = load(', 'verifier = load('):
            self.assertLess(guard, source.index(mark))

    def test_no_native_runner_freezer_or_subprocess_execution(self):
        source = inspect.getsource(replay)
        self.assertNotIn('import subprocess', source)
        self.assertNotIn("m['runner']", source)
        self.assertNotIn("m['freezer']", source)
        self.assertNotIn('check_output(', source)
        self.assertNotIn('os.system(', source)

    def test_current_head_is_not_historical_source_guard(self):
        source = inspect.getsource(replay.replay)
        self.assertIn("m['head'] == HISTORICAL_HEAD", source)
        self.assertNotIn('git ', source)
        self.assertNotIn('rev-parse', source)

    def phase(self):
        env = {'environment': {'DISPLAY': '', 'WAYLAND_DISPLAY': '', 'TZ': 'UTC'},
               'cpu': [0], 'nice': 10}
        m = {'work': 'work', 'native_argv': {'compile_initop': ['tcc', 'th03/initop.cpp']}}
        a = {'argv': m['native_argv']['compile_initop'], 'cwd': '/repo/work',
             'environment': env['environment'], 'wait_seconds': 90, 'cleanup_seconds': 15}
        z = {'exit_code': 0, 'timeout': False, 'cleanup_uncertain': False, 'poison': False,
             'initial_inventory_complete': True, 'inventory_complete': True,
             'survivors': [], 'errors': [], 'ok': True,
             'owned_leader': [16, 16, '123456', 'wine', 'R']}
        return a, z, m, env

    def test_positive_bounded_phase(self):
        replay.validate_phase('compile_initop', *self.phase())

    def test_native_phase_mutations(self):
        cases = [('a', 'argv', ['tasm'], 'argv'), ('a', 'cwd', '/other', 'cwd'),
                 ('a', 'wait_seconds', 91, 'phase bounds'),
                 ('a', 'cleanup_seconds', 16, 'phase bounds'),
                 ('e', 'cpu', [0, 1], 'resource bounds'), ('e', 'nice', 0, 'resource bounds'),
                 ('z', 'exit_code', 1, 'phase exit'), ('z', 'exit_code', False, 'phase exit'),
                 ('z', 'timeout', True, 'unsafe cleanup'),
                 ('z', 'cleanup_uncertain', True, 'unsafe cleanup'),
                 ('z', 'poison', True, 'unsafe cleanup'),
                 ('z', 'survivors', [123], 'owned cleanup inventory'),
                 ('z', 'inventory_complete', False, 'owned cleanup inventory'),
                 ('z', 'initial_inventory_complete', False, 'owned cleanup inventory'),
                 ('z', 'ok', False, 'owned cleanup inventory'),
                 ('z', 'owned_leader', [], 'exact owned process identity')]
        for target, key, value, message in cases:
            a, z, m, e = self.phase()
            {'a': a, 'z': z, 'e': e}[target][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, message):
                replay.validate_phase('compile_initop', a, z, m, e)

    def report(self):
        comparisons = dict(target_raw_equal=True, baseline_raw_equal=True,
                           target_ordered_equal=True, baseline_ordered_equal=True)
        return dict(diagnostic_checks_pass=True, source_integrity_checked=True,
            source_acceptance=False, exact_acceptance=False, whole_product_ownership=False,
            cold_build=False, runtime_run=False, native_invocations_now=0,
            new_helper_bytes=247, new_helper_all_raw_ordered_pass=True,
            new_helpers=[dict(name=n, offset=o, size=s, full_producer=dict(comparisons),
                instructions=dict(full_decode=True, return_abi_preserved=True), **comparisons)
                for n, o, s in replay.EXTENTS],
            objects=[dict(maintained_lineage_checked=True, literal_non_comment_omf_equal=True,
                stable_compiler_comments_equal=True) for _ in range(5)],
            retained_project_context=[{} for _ in range(22)], retained_project_context_count=22,
            prior_owner_count=37, prior_owner_bytes=12569, prior_owners_preserved=True,
            prior_owners=[dict(baseline_raw_equal=True, baseline_ordered_equal=True,
                map_preserved=True) for _ in range(37)],
            all_map_publics_preserved=True, all_map_code_contributions_preserved=True,
            baseline_whole_program_and_order_preserved=True, whole_file_equal_baseline=True,
            candidate_sha256=replay.EXE_SHA, baseline_sha256=replay.EXE_SHA,
            whole_program=dict(target_different_bytes=6),
            whole_ordered_relocations=dict(target_different_positions=313, target_equal=False),
            whole_file_equal_target=False, global_target_negatives_unchanged=True,
            original_producer_context_bytes=2, excluded_alignment_bytes=1,
            unowned_context=[dict(offset=o, size=1, raw_hex=h, function_code_credit=False,
                target_baseline_candidate_equal=True) for o, h in
                [(0x67, '90'), (0xa1, '90'), (0x16f, '00')]])

    def test_positive_structural_report(self):
        replay.validate_report(self.report())

    def test_report_mutation_guards(self):
        cases = [
            (('new_helpers', 0, 'size'), 30, 'new owner extents'),
            (('objects', 0, 'maintained_lineage_checked'), False, 'fresh maintained OMF lineage'),
            (('prior_owners', 0, 'baseline_raw_equal'), False, 'prior owner preservation'),
            (('whole_file_equal_target',), True, 'global target negatives'),
            (('whole_program', 'target_different_bytes'), 0, 'global target negatives'),
            (('whole_ordered_relocations', 'target_equal'), True, 'global target negatives'),
            (('unowned_context', 0, 'function_code_credit'), True, 'unowned NOP/alignment context'),
            (('unowned_context', 2, 'offset'), 0x170, 'unowned NOP/alignment context'),
            (('new_helpers', 3, 'instructions', 'return_abi_preserved'), False, 'original return ABI'),
            (('new_helpers', 0, 'target_ordered_equal'), False, 'new owner comparisons'),
            (('retained_project_context_count',), 23, 'fresh/retained object partition'),
            (('candidate_sha256',), '0' * 64, 'baseline identity')]
        for path, value, message in cases:
            report = self.report()
            obj = report
            for key in path[:-1]:
                obj = obj[key]
            obj[path[-1]] = value
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, message):
                replay.validate_report(report)

    def test_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            replay.regular(ROOT, '../outside')

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'body').write_bytes(b'body')
            (root / 'link').symlink_to(root / 'body')
            with self.assertRaisesRegex(ValueError, 'regular input'):
                replay.regular(root, 'link')

    def retained_available(self):
        if not (REPO / self.p['inventory']['path']).is_file():
            self.skipTest('Retained private native receipts are unavailable; portable guards still run.')

    def test_retained_positive_offline_replay(self):
        self.retained_available()
        result = replay.replay(REPO, self.p, ROOT)
        self.assertTrue(result['pass_checks'])
        self.assertEqual(result['native_invocations_now'], 0)
        self.assertEqual(result['native_phases_replayed'], 6)
        self.assertEqual(result['new_owner_bytes'], 247)
        self.assertFalse(result['exact_acceptance'])

    def test_retained_required_pin_omission_rejected(self):
        self.retained_available()
        inventory = json.loads((REPO / self.p['inventory']['path']).read_bytes())
        pins = {row['path']: row for row in inventory['pins']}
        manifests = [json.loads((REPO / out / 'manifest.json').read_bytes()) for out in replay.OUTS]
        targets = [manifests[1]['work'] + '/bin/th03/op.exe',
                   manifests[1]['work'] + '/obj/th03/polar.obj',
                   manifests[1]['verifier']['path'],
                   manifests[1]['registry_policy']['path'],
                   replay.OUTS[1] + '/linked-verification.json',
                   replay.OUTS[0] + '/compile_snd_mode-finished.json',
                   'scripts/lib/pc98.py',
                   '.analysis/op-remaining-helpers-source-proposal-v01/payload/src/op/core/initop.cpp']
        for target in targets:
            remaining = dict(pins)
            remaining.pop(target)
            with self.subTest(target=target), self.assertRaisesRegex(ValueError, 'missing required retained pin'):
                replay.guard_pin_closure(remaining, manifests,
                                         lambda name: replay.regular(REPO, name).read_bytes())

    def test_retained_receipt_drift_rejected_before_any_dynamic_import(self):
        self.retained_available()
        original = replay.regular
        target = replay.OUTS[0] + '/compile_snd_mode-finished.json'
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / 'bad.json'
            bad.write_text('{"exit_code": 999}')
            def altered(root, name):
                return bad if name == target else original(root, name)
            with mock.patch.object(replay, 'regular', side_effect=altered), \
                 mock.patch.object(replay.types, 'ModuleType', side_effect=AssertionError('early import')), \
                 self.assertRaisesRegex(ValueError, 'input drift'):
                replay.replay(REPO, self.p, ROOT)


if __name__ == '__main__':
    unittest.main()

