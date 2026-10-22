"""No-native PFOPEN replay and fail-closed provenance mutation regressions."""
from pathlib import Path
import copy
import importlib.util
import json
import os
import sys
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
