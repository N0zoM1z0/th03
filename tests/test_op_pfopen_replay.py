"""No-native PFOPEN replay and fail-closed provenance mutation regressions."""
from pathlib import Path
import copy
from contextlib import contextmanager
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
SOURCE_ROOT = Path(os.environ.get('TH03_OP_PFOPEN_SOURCE_ROOT', Path(__file__).resolve().parents[1])).resolve()
ROOT = Path(os.environ.get('TH03_OP_PFOPEN_REPO_ROOT', Path(__file__).resolve().parents[1])).resolve()
spec = importlib.util.spec_from_file_location('maintained_pfopen_replay', SOURCE_ROOT/'scripts/replay_th03_op_pfopen_source.py')
r = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = r
spec.loader.exec_module(r)


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof = json.loads((SOURCE_ROOT/'config/op_pfopen_source/proof.json').read_bytes())
        cls.manifest = json.loads((ROOT/r.OUT/'manifest.json').read_bytes())
        cls.report = json.loads((ROOT/r.OUT/'linked-verification.json').read_bytes())
        cls.done = json.loads((ROOT/r.OUT/'completion.json').read_bytes())
        cls.start = json.loads((ROOT/r.OUT/'compile_root-started.json').read_bytes())
        cls.finish = json.loads((ROOT/r.OUT/'compile_root-finished.json').read_bytes())
        cls.env = json.loads((ROOT/r.OUT/'environment.json').read_bytes())

    def test_full_actual_native_replay_without_native_or_current_HEAD_gate(self):
        with patch('subprocess.run', side_effect=AssertionError('no process execution')), \
             patch('subprocess.Popen', side_effect=AssertionError('no process execution')):
            result = r.replay(ROOT, self.proof, SOURCE_ROOT)
        self.assertTrue(result['pass_checks'])
        self.assertTrue(result['original_report_reproduced_verbatim'])
        self.assertTrue(result['selection_correction_reproduced'])
        self.assertFalse(result['installed_head_requirement'])
        self.assertEqual(result['native_invocations_now'], 0)
        self.assertEqual((result['total_scoped_bodies'], result['total_scoped_bytes']), (45, 13221))
        self.assertEqual((result['new_owner_bytes'], result['retained_context_objects']), (281, 27))
        self.assertTrue(all(result[n] is False for n in r.FLAGS))

    def test_historical_manifest_is_not_current_full_tree_guard(self):
        p = copy.deepcopy(self.proof); m = copy.deepcopy(self.manifest)
        m['sources']['unrelated/historical-only'] = dict(sha256='0'*64, bytes=1, mode=420)
        r.guard_current(ROOT, p, SOURCE_ROOT, m)

    def test_prior_graph_denominator_is_derived_from_actual_manifest(self):
        p = self.proof; m = self.manifest
        self.assertEqual(p['project_objects'], len(m['project_objects']))
        self.assertEqual(p['retained_context_objects'], len(m['retained_objects']))
        self.assertEqual(len(set(m['new_owner_objects']) | set(m['retained_objects'])), p['project_objects'])
        self.assertNotIn('obj/th03/op.obj', m['repeat_inputs'])

    def test_real_report_and_receipts_pass(self):
        r.validate_proof(self.proof); r.validate_report(self.report); r.validate_completion(self.done)
        r.validate_phase('compile_root', self.start, self.finish, self.manifest, self.env)

    def test_measured_target_relocation_count_is_not_forced_313(self):
        q = copy.deepcopy(self.report); rel = q['whole_ordered_relocations']
        rel['target'] = copy.deepcopy(rel['candidate']); rel['target'][0][0] ^= 1
        rel['target_different_positions'] = 1; rel['target_equal'] = False
        r.validate_report(q)

    def reject_report(self, path, value):
        q = copy.deepcopy(self.report); obj = q
        for part in path[:-1]: obj = obj[part]
        obj[path[-1]] = value
        with self.assertRaises(ValueError): r.validate_report(q)

    def reject_phase(self, group, field, value):
        a, b, e = copy.deepcopy(self.start), copy.deepcopy(self.finish), copy.deepcopy(self.env)
        {'start': a, 'finish': b, 'env': e}[group][field] = value
        with self.assertRaises(ValueError): r.validate_phase('compile_root', a, b, self.manifest, e)

    def reject_guarded_input(self, name, source=False):
        original = r.stable_read
        def altered(root, path):
            data = original(root, path)
            if path == name and Path(root) == (SOURCE_ROOT if source else ROOT):
                return data+b'\x00'
            return data
        with patch.object(r, 'stable_read', side_effect=altered), patch.object(r, 'load_checked_module') as imported:
            with self.assertRaises(ValueError): r.replay(ROOT, self.proof, SOURCE_ROOT)
            imported.assert_not_called()

    def test_inventory_omission_rejected_before_import(self):
        p = copy.deepcopy(self.proof); name = p['inventory']['path']
        inv = json.loads((ROOT/name).read_bytes())
        omitted = self.manifest['source_packet_archive']['path']
        inv['pins'] = [q for q in inv['pins'] if q['path'] != omitted]
        inv['inputs'].pop(omitted)
        raw = (json.dumps(inv, indent=2)+'\n').encode()
        p['inventory'].update(r.values(raw)); original = r.stable_read
        with patch.object(r, 'stable_read', side_effect=lambda root, path: raw if path == name else original(root, path)), patch.object(r, 'load_checked_module') as imported:
            with self.assertRaisesRegex(ValueError, 'exact retained closure membership'):
                r.replay(ROOT, p, SOURCE_ROOT)
            imported.assert_not_called()

    def test_duplicate_inventory_pin_rejected_before_import(self):
        p = copy.deepcopy(self.proof); name = p['inventory']['path']
        inv = json.loads((ROOT/name).read_bytes()); inv['pins'].append(inv['pins'][0])
        raw = json.dumps(inv).encode(); p['inventory'].update(r.values(raw)); original = r.stable_read
        with patch.object(r, 'stable_read', side_effect=lambda root, path: raw if path == name else original(root, path)), patch.object(r, 'load_checked_module') as imported:
            with self.assertRaisesRegex(ValueError, 'duplicate inventory pin'): r.replay(ROOT, p, SOURCE_ROOT)
            imported.assert_not_called()

    def test_unsafe_paths(self):
        for name in ('/tmp/absolute', '../outside', 'scripts/../scripts/lib/omf.py', './scripts/lib/omf.py'):
            with self.subTest(name=name), self.assertRaises(ValueError): r.regular(ROOT, name)

    def test_all_receipts_and_sources_are_retained(self):
        inv = json.loads((ROOT/self.proof['inventory']['path']).read_bytes()); names = set(inv['inputs'])
        self.assertEqual(len(r.receipt_names()), 31)
        self.assertLessEqual({r.OUT+'/'+n for n in r.receipt_names()}, names)
        self.assertLessEqual({q['path'] for q in self.manifest['inputs']}, names)
        self.assertLessEqual({q['path'] for q in self.manifest['retained_objects'].values()}, names)
        self.assertEqual(len(self.proof['context_source_closure']), 79)

    def test_selection_audit_failure_is_not_silently_upgraded(self):
        q = json.loads((ROOT/r.AUDIT/'audit-result.json').read_bytes()); q['original_linked_scope_checks_pass'] = True
        with self.assertRaises(ValueError): r.validate_selection_audit(q, self.manifest, {}, lambda n: b'')


    @contextmanager
    def source_copy(self):
        with tempfile.TemporaryDirectory(prefix='pfopen-replay-binding-') as temp:
            root = Path(temp)
            names = r.SOURCE_CLOSURE | {r.REPLAY_BINDING, 'config/op_pfopen_source/proof.json'}
            names |= {q['snapshot']['path'] for q in r.EXPECTED_BINDING['historical_inputs'].values()}
            names.add(r.EXPECTED_BINDING['predecessor_replay']['snapshot']['path'])
            for name in names:
                dest = root/name; dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(SOURCE_ROOT/name, dest)
            yield root

    def rejected_before_import(self, source_root, pattern):
        with patch.object(r, 'load_checked_module') as imported:
            with self.assertRaisesRegex(ValueError, pattern):
                r.replay(ROOT, self.proof, source_root)
            imported.assert_not_called()

    def reject_binding(self, change, pattern='replay binding'):
        binding = json.loads((SOURCE_ROOT/r.REPLAY_BINDING).read_bytes())
        change(binding)
        raw = json.dumps(binding).encode(); original = r.stable_read
        with patch.object(r, 'stable_read', side_effect=lambda root, path:
                          raw if path == r.REPLAY_BINDING else original(root, path)):
            self.rejected_before_import(SOURCE_ROOT, pattern)

    def test_original_proof_and_predecessor_are_not_rewritten(self):
        binding = r.read_replay_binding(SOURCE_ROOT, self.proof)
        self.assertEqual(r.values((SOURCE_ROOT/'config/op_pfopen_source/proof.json').read_bytes()),
                         {k: binding['original_proof'][k] for k in ('sha256', 'bytes')})
        self.assertEqual(self.proof['maintained_closure'][r.SELF],
                         r.values((SOURCE_ROOT/binding['predecessor_replay']['snapshot']['path']).read_bytes()))
        self.assertNotEqual(self.proof['maintained_closure'][r.SELF],
                            r.values((SOURCE_ROOT/r.SELF).read_bytes()))
        inventory = json.loads((ROOT/self.proof['inventory']['path']).read_bytes())
        self.assertEqual(inventory['metadata'], {k: v for k, v in self.proof.items() if k != 'inventory'})

    def test_current_housekeeping_maintenance_is_not_historical_drift(self):
        original = r.stable_read
        housekeeping = set(r.EXPECTED_BINDING['historical_inputs'])
        def no_live_housekeeping(root, name):
            if name in housekeeping:
                raise AssertionError('must not read evolving housekeeping as historical input')
            return original(root, name)
        with patch.object(r, 'stable_read', side_effect=no_live_housekeeping), \
             patch.object(r, 'load_checked_module', wraps=r.load_checked_module) as imported, \
             patch('subprocess.run', side_effect=AssertionError('no native execution')), \
             patch('subprocess.Popen', side_effect=AssertionError('no native execution')):
            result = r.replay(ROOT, self.proof, SOURCE_ROOT)
        self.assertTrue(result['pass_checks'])
        self.assertEqual(set(result['historical_input_snapshots']), housekeeping)
        snapshots = set(result['historical_input_snapshots'].values())
        snapshots.add(r.EXPECTED_BINDING['predecessor_replay']['snapshot']['path'])
        self.assertTrue(all(not any(str(call.args[1]).endswith(n) for n in snapshots | housekeeping)
                            for call in imported.call_args_list))

    def test_binding_missing_is_rejected_before_import(self):
        with self.source_copy() as root:
            (root/r.REPLAY_BINDING).unlink()
            self.rejected_before_import(root, 'regular input')

    def test_binding_schema_extra_key_is_rejected_before_import(self):
        self.reject_binding(lambda b: b.update(unreviewed=True), 'binding schema')

    def test_binding_duplicate_key_is_rejected_before_import(self):
        raw = (SOURCE_ROOT/r.REPLAY_BINDING).read_bytes()
        raw = b'{"schema":"ignored",' + raw.lstrip()[1:]
        original = r.stable_read
        with patch.object(r, 'stable_read', side_effect=lambda root, name:
                          raw if name == r.REPLAY_BINDING else original(root, name)):
            self.rejected_before_import(SOURCE_ROOT, 'duplicate replay binding key')

    def test_binding_wrong_original_proof_is_rejected_before_import(self):
        self.reject_binding(lambda b: b['original_proof'].update(sha256='0'*64), 'binding provenance')

    def test_binding_wrong_predecessor_is_rejected_before_import(self):
        self.reject_binding(lambda b: b['predecessor_replay']['historical_pin'].update(sha256='0'*64),
                            'binding provenance')

    def test_binding_current_self_wrong_hash_is_rejected_before_import(self):
        self.reject_binding(lambda b: b['current_replay'].update(sha256='0'*64), 'current replay identity')

    def test_binding_current_self_wrong_mode_is_rejected_before_import(self):
        self.reject_binding(lambda b: b['current_replay'].update(mode=0o644), 'current replay pin schema')

    def test_binding_current_self_wrong_path_is_rejected_before_import(self):
        self.reject_binding(lambda b: b['current_replay'].update(path='scripts/clean_generated.py'),
                            'current replay pin schema')

    def test_binding_cannot_add_current_helper_fallback(self):
        self.reject_binding(lambda b: b['historical_inputs'].update({
            'scripts/lib/omf.py': copy.deepcopy(b['historical_inputs']['scripts/clean_generated.py'])}),
            'binding provenance')

    def test_binding_cannot_omit_historical_mapping(self):
        for name in r.EXPECTED_BINDING['historical_inputs']:
            with self.subTest(name=name):
                self.reject_binding(lambda b: b['historical_inputs'].pop(name), 'binding provenance')

    def test_binding_cannot_redirect_snapshot_paths(self):
        for path in ('/tmp/unbound', '../unbound', './config/recovery/copy.py.txt',
                     'config/recovery/../recovery/copy.py.txt', 'config/recovery/same-bytes-copy.py.txt'):
            with self.subTest(path=path):
                self.reject_binding(lambda b: b['historical_inputs']['scripts/clean_generated.py']
                                    ['snapshot'].update(path=path), 'binding provenance')

    def test_wrong_predecessor_pin_in_proof_is_rejected_before_import(self):
        p = copy.deepcopy(self.proof); p['maintained_closure'][r.SELF]['sha256'] = '0'*64
        with patch.object(r, 'load_checked_module') as imported:
            with self.assertRaisesRegex(ValueError, 'original predecessor replay pin'):
                r.replay(ROOT, p, SOURCE_ROOT)
            imported.assert_not_called()

    def test_snapshot_ancestor_symlink_is_rejected_before_import(self):
        with self.source_copy() as root:
            original = root/'config/recovery'
            moved = root/'config/snapshot-bytes'; original.rename(moved)
            original.symlink_to(moved, target_is_directory=True)
            self.rejected_before_import(root, 'regular input')

    def test_historical_logical_mode_cannot_be_rewritten(self):
        for logical in r.EXPECTED_BINDING['historical_inputs']:
            with self.subTest(logical=logical):
                p = copy.deepcopy(self.proof); name = p['inventory']['path']
                inventory = json.loads((ROOT/name).read_bytes())
                next(q for q in inventory['pins'] if q['path'] == logical)['mode'] = 0o644
                raw = json.dumps(inventory).encode(); p['inventory'].update(r.values(raw)); original = r.stable_read
                with patch.object(r, 'stable_read', side_effect=lambda root, path:
                                  raw if path == name else original(root, path)), \
                     patch.object(r, 'load_checked_module') as imported:
                    with self.assertRaisesRegex(ValueError, 'historical housekeeping pin'):
                        r.replay(ROOT, p, SOURCE_ROOT)
                    imported.assert_not_called()

    def test_historical_pin_omission_still_reaches_exact_closure_gate(self):
        for logical in r.EXPECTED_BINDING['historical_inputs']:
            with self.subTest(logical=logical):
                p = copy.deepcopy(self.proof); name = p['inventory']['path']
                inventory = json.loads((ROOT/name).read_bytes())
                inventory['pins'] = [q for q in inventory['pins'] if q['path'] != logical]
                inventory['inputs'].pop(logical)
                raw = json.dumps(inventory).encode(); p['inventory'].update(r.values(raw)); original = r.stable_read
                with patch.object(r, 'stable_read', side_effect=lambda root, path:
                                  raw if path == name else original(root, path)), \
                     patch.object(r, 'load_checked_module') as imported:
                    with self.assertRaisesRegex(ValueError, 'exact retained closure membership'):
                        r.replay(ROOT, p, SOURCE_ROOT)
                    imported.assert_not_called()

    def test_historical_snapshots_cannot_be_loaded_as_code(self):
        binding = r.read_replay_binding(SOURCE_ROOT, self.proof)
        names = set(binding['historical_inputs']) | {
            q['snapshot']['path'] for q in binding['historical_inputs'].values()}
        names.add(binding['predecessor_replay']['snapshot']['path'])
        for name in names:
            with self.subTest(name=name), patch.object(r, 'load_checked_module') as imported:
                with self.assertRaisesRegex(ValueError, 'historical snapshot is data only'):
                    r.load_retained_module('forbidden', ROOT, name, lambda n: b'', binding)
                imported.assert_not_called()

    def test_verifier_adapter_delegates_all_nonhistorical_inputs_unchanged(self):
        original = unittest.mock.Mock(return_value=b'original')
        verifier = types.SimpleNamespace(pin=original); read = unittest.mock.Mock(return_value=b'snapshot')
        binding = r.read_replay_binding(SOURCE_ROOT, self.proof)
        r.bind_verifier_inputs(verifier, read, binding)
        pin = {'path': 'scripts/lib/omf.py', 'sha256': 'unrelated'}; base = Path('/bound/base')
        self.assertEqual(verifier.pin(pin, base), b'original')
        original.assert_called_once_with(pin, base); read.assert_not_called()
        for name, entry in binding['historical_inputs'].items():
            self.assertEqual(verifier.pin(entry['historical_pin']), b'snapshot')
            read.assert_called_with(name)
            for bad in ('hash', 'mode', 'path', 'base'):
                q = copy.deepcopy(entry['historical_pin'])
                if bad == 'hash': q['sha256'] = '0'*64
                elif bad == 'mode': q['mode'] = 0o644
                elif bad == 'path': q['unreviewed'] = True
                with self.subTest(name=name, bad=bad), self.assertRaises(ValueError):
                    verifier.pin(q, base if bad == 'base' else None)
        self.assertEqual(original.call_count, 1)

    def test_current_consumed_maintained_context_still_rejected_before_import(self):
        self.reject_guarded_input(next(iter(self.proof['context_source_closure'])))

    def test_verifier_adapter_never_canonicalizes_path_variants(self):
        binding = r.read_replay_binding(SOURCE_ROOT, self.proof)
        seen = []
        def checked_original(pin, base=None):
            seen.append((pin, base))
            return r.stable_read(ROOT if base is None else base, pin['path'])
        verifier = types.SimpleNamespace(pin=checked_original)
        read = unittest.mock.Mock(side_effect=AssertionError('not an exact historical path'))
        r.bind_verifier_inputs(verifier, read, binding)
        for logical, entry in binding['historical_inputs'].items():
            for name in ('./'+logical, 'scripts/../'+logical, '/'+logical):
                pin = dict(entry['historical_pin'], path=name)
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'unsafe input path'):
                    verifier.pin(pin)
                self.assertIs(seen[-1][0], pin)
        read.assert_not_called()

    def test_current_replay_actual_mode_drift_rejected_before_import(self):
        with self.source_copy() as root:
            (root/r.SELF).chmod(0o644)
            self.rejected_before_import(root, 'current replay mode')

    def test_binding_current_self_wrong_size_rejected_before_import(self):
        self.reject_binding(lambda b: b['current_replay'].update(bytes=1), 'current replay identity')

    def test_current_import_helper_mode_checks_are_unchanged(self):
        original = r.regular
        for helper in r.HELPER_CLOSURE:
            def changed_mode(root, name):
                path = original(root, name)
                if name == helper:
                    wrapper = unittest.mock.Mock(wraps=path)
                    original_stat = path.stat()
                    altered_stat = os.stat_result((original_stat.st_mode ^ 0o100, *original_stat[1:]))
                    wrapper.stat.return_value = altered_stat
                    return wrapper
                return path
            with self.subTest(helper=helper), patch.object(r, 'regular', side_effect=changed_mode):
                self.rejected_before_import(SOURCE_ROOT, 'input mode drift '+helper)

    def test_binding_revision_cannot_change_mid_replay(self):
        binding = r.read_replay_binding(SOURCE_ROOT, self.proof)
        changed = copy.deepcopy(binding); changed['current_replay']['sha256'] = '0'*64
        with patch.object(r, 'read_replay_binding', return_value=changed):
            with self.assertRaisesRegex(ValueError, 'binding changed during replay'):
                r.guard_current(ROOT, self.proof, SOURCE_ROOT, self.manifest, binding)

    def reject_snapshot_mutation(self, name, mutation):
        with self.source_copy() as root:
            path = root/name
            if mutation == 'bytes': path.write_bytes(path.read_bytes()+b'changed')
            elif mutation == 'missing': path.unlink()
            elif mutation == 'mode': path.chmod(0o755)
            elif mutation == 'symlink': path.unlink(); path.symlink_to(SOURCE_ROOT/name)
            self.rejected_before_import(root, 'snapshot|regular input')


for label, entry in list(r.EXPECTED_BINDING['historical_inputs'].items()) + [
        ('predecessor', r.EXPECTED_BINDING['predecessor_replay'])]:
    for mutation in ('bytes', 'missing', 'mode', 'symlink'):
        name = 'test_snapshot_'+Path(label).stem+'_'+mutation+'_rejected_before_import'
        setattr(ReplayTests, name, lambda self, path=entry['snapshot']['path'], mutation=mutation:
                self.reject_snapshot_mutation(path, mutation))

for label, path, source in [('current_replay', r.SELF, True),
                           ('original_proof', 'config/op_pfopen_source/proof.json', True),
                           *[('helper_'+Path(n).stem, n, False) for n in r.HELPER_CLOSURE]]:
    setattr(ReplayTests, 'test_new_binding_preimport_'+label,
            lambda self, path=path, source=source: self.reject_guarded_input(path, source))


REPORT_MUTATIONS = {
    'credit_source': (['source_acceptance'], True),
    'credit_exact': (['exact_acceptance'], True),
    'credit_root': (['whole_root_credit'], True),
    'prior_count': (['prior_owner_count'], 43),
    'prior_bytes': (['prior_owner_bytes'], 12939),
    'all_count': (['candidate_scope_count'], 46),
    'all_bytes': (['candidate_scope_bytes'], 13278),
    'new_count': (['new_candidate_count'], 2),
    'new_bytes': (['new_candidate_bytes'], 338),
    'pfopen_start': (['new_pfopen_body', 'offset'], 0x2EF1),
    'pfopen_extent': (['new_pfopen_body', 'size'], 282),
    'pfopen_byte': (['new_pfopen_body', 'candidate_sha256'], '0'*64),
    'pfopen_reloc': (['new_pfopen_body', 'target_ordered_equal'], False),
    'prior_byte': (['prior_owners', 0, 'baseline_raw_equal'], False),
    'prior_reloc': (['prior_owners', 0, 'baseline_ordered_equal'], False),
    'root_omf': (['root_object', 'complete_structural_equal'], False),
    'root_raw': (['root_object', 'raw_equal'], False),
    'literal_baseline_reloc': (['whole_ordered_relocations', 'baseline', 0, 0], -1),
    'wrong_target_count': (['whole_ordered_relocations', 'target_different_positions'], 0),
    'baseline_image': (['whole_program', 'baseline_different_bytes'], 1),
    'context_dd95': (['excluded_context', 'dd95'], [0xDD95, 0xDD97]),
    'context_alignment': (['excluded_context', 'following_alignment_and_str_ieq'], [0x300C, 0x3044]),
    'public_count': (['map_public_counts', 'candidate', 'Name'], 646),
    'macro_closure': (['source_proof', 'compatibility_headers'], 11),
    'physical_context': (['source_proof', 'physical_context_files'], 141),
    'abi_pop': (['source_proof', 'abi', 'callee_pop_bytes'], 4),
    'abi_far': (['source_proof', 'abi', 'far_return'], False),
    'native_seed': (['native_proof', 'materialized_root_seed_absent'], False),
    'native_count': (['native_proof', 'phase_count'], 1),
    'object_count': (['graph', 'project_object_count'], 27),
    'retained_count': (['graph', 'retained_project_object_count'], 26),
}
for name, (path, value) in REPORT_MUTATIONS.items():
    setattr(ReplayTests, 'test_report_mutation_'+name, lambda self, path=path, value=value: self.reject_report(path, value))

PHASE_MUTATIONS = {
    'boolean_exit': ('finish', 'exit_code', False), 'exit': ('finish', 'exit_code', 1),
    'timeout': ('finish', 'timeout', True), 'poison': ('finish', 'poison', True),
    'uncertain': ('finish', 'cleanup_uncertain', True), 'survivor': ('finish', 'survivors', [1]),
    'incomplete_inventory': ('finish', 'initial_inventory_complete', False),
    'argv': ('start', 'argv', ['model-root']), 'cwd': ('start', 'cwd', '/tmp/fake'),
    'timeout_bound': ('start', 'wait_seconds', 91), 'cleanup_bound': ('start', 'cleanup_seconds', 0),
    'cpu': ('env', 'cpu', [0, 1]), 'nice': ('env', 'nice', 0),
}
for name, args in PHASE_MUTATIONS.items():
    setattr(ReplayTests, 'test_phase_mutation_'+name, lambda self, args=args: self.reject_phase(*args))

for name, value in {'source_acceptance': True, 'exact_acceptance': True, 'whole_root_credit': True,
                    'total_scoped_bytes': 13278, 'fresh_owner_objects': 2,
                    'retained_context_objects': 26, 'manifest_sha256': '0'*64}.items():
    def proof_mutation(self, name=name, value=value):
        p = copy.deepcopy(self.proof); p[name] = value
        with self.assertRaises(ValueError): r.validate_proof(p)
    setattr(ReplayTests, 'test_proof_mutation_'+name, proof_mutation)

for name, path, source in [
    ('maintained', r.SOURCE, True), ('header', 'compat/op_pfopen/libs/master.lib/pf.inc', True),
    ('stage', r.STAGE, True), ('helper', 'scripts/lib/omf.py', False),
    ('receipt', r.OUT+'/compile_root-finished.json', False),
    ('audit', r.AUDIT+'/audit-result.json', False),
    ('consumed_source', '.analysis/toolchain/wineprefix/drive_c/OPPF101/th03/formats/pfopen.asm', False),
    ('consumed_object', '.analysis/toolchain/wineprefix/drive_c/OPPF101/obj/th03/op.obj', False),
    ('archive', '.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar', False),
]:
    setattr(ReplayTests, 'test_preimport_guard_'+name, lambda self, path=path, source=source: self.reject_guarded_input(path, source))

if __name__ == '__main__':
    unittest.main()
