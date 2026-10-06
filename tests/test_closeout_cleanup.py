from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import closeout_cleanup as m


class CloseoutCleanupControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.put('README.md', 'snapshot\n')
        subprocess.run(['git', 'add', 'README.md'], cwd=self.root, check=True)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        for module, name, value in [(m, 'ROOT', self.root), (m.cleanup, 'ROOT', self.root),
                (m.cleanup, 'ANALYSIS', self.root/'.analysis'), (m.cleanup, 'EVIDENCE', self.root/'config/evidence.csv'),
                (m.cleanup, 'PRESERVED_ANALYSIS_ROOTS', {self.root/'.analysis/targets'}),
                (m.cleanup, 'PRESERVED_ANALYSIS_FILES', {self.root/'.analysis/target-import.json'}),
                (m.cleanup, 'CACHE_ROOTS', [])]:
            self.stack.enter_context(patch.object(module, name, value))
    def put(self, name, value):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)
        return path
    def proof(self, name, **extra):
        return self.put(name, json.dumps(dict(kind='test-diagnostic', inputs={}, source_acceptance=False, exact_acceptance=False, **extra)))
    def test_documented_log_and_stale_guard_survive(self):
        self.put('README.md', 'Evidence: .analysis/documented.log\n')
        kept = self.put('.analysis/documented.log', 'keep')
        guarded = self.put('.analysis/guarded.bin', 'changed historical bytes')
        self.proof('.analysis/proof.json', other=dict(inputs={'.analysis/guarded.bin': '0'*64}))
        removed = self.put('.analysis/unused.log', 'discard')
        plan = m.plan_cleanup();m.apply_plan(plan)
        self.assertTrue(kept.exists());self.assertTrue(guarded.exists());self.assertFalse(removed.exists())
        self.assertEqual(plan['retained_input_states']['.analysis/guarded.bin']['sha256'], m.digest(guarded))
    def test_cold_receipt_retains_unlisted_archive(self):
        self.proof('.analysis/cold/receipt.json')
        archive = self.put('.analysis/cold/reference.tar', 'archive')
        m.apply_plan(m.plan_cleanup());self.assertTrue(archive.exists())
    def test_changed_candidate_stops_before_first_deletion(self):
        first = self.put('.analysis/a.tmp', 'first');second = self.put('.analysis/b.tmp', 'second')
        plan = m.plan_cleanup();second.write_text('changed')
        with self.assertRaisesRegex(ValueError, 'candidate changed'):m.apply_plan(plan)
        self.assertTrue(first.exists())
    def test_changed_tracked_reference_stops_deletion(self):
        output = self.put('.analysis/a.tmp', 'keep until checked');plan = m.plan_cleanup()
        self.put('README.md', 'Changed .analysis/a.tmp\n')
        with self.assertRaisesRegex(ValueError, 'tracked reference changed'):m.apply_plan(plan)
        self.assertTrue(output.exists())
    def test_new_file_in_selected_tree_stops_deletion(self):
        original = self.put('.analysis/discard/old.tmp', 'old');plan = m.plan_cleanup()
        self.put('.analysis/discard/new.tmp', 'new')
        with self.assertRaisesRegex(ValueError, 'selected tree changed'):m.apply_plan(plan)
        self.assertTrue(original.exists())
    def test_replaced_tree_symlink_does_not_touch_external_data(self):
        original = self.put('.analysis/discard/old.tmp', 'old');plan = m.plan_cleanup()
        external = self.put('external/keep', 'keep');original.unlink();original.parent.rmdir()
        original.parent.symlink_to(external.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'selected tree changed'):m.apply_plan(plan)
        self.assertTrue(external.exists())
    def test_unreferenced_superseded_proof_can_retire_with_old_fingerprint_retained(self):
        draft = self.proof('.analysis/draft.json')
        fingerprint = self.put('.analysis/history.json', json.dumps(dict(kind='th03-abandoned-build-output-cleanup',
            inputs={}, reference_corpus={'.analysis/draft.json': m.digest(draft)})))
        plan = m.plan_cleanup(retire=['.analysis/draft.json']);m.apply_plan(plan)
        self.assertFalse(draft.exists());self.assertTrue(fingerprint.exists());self.assertIn('.analysis/draft.json',plan['retired_proofs'])
    def test_new_proof_dependency_after_planning_stops_retirement(self):
        draft = self.proof('.analysis/draft.json');plan = m.plan_cleanup(retire=['.analysis/draft.json'])
        self.put('.analysis/new.json',json.dumps(dict(inputs={'.analysis/draft.json':m.digest(draft)})))
        with self.assertRaisesRegex(ValueError,'proof reference corpus changed'):m.apply_plan(plan)
        self.assertTrue(draft.exists())
    def test_retirement_rejects_real_proof_dependency(self):
        draft = self.proof('.analysis/draft.json')
        self.put('.analysis/current.json', json.dumps(dict(inputs={'.analysis/draft.json':m.digest(draft)})))
        with self.assertRaisesRegex(ValueError, 'retained JSON reference'):m.plan_cleanup(retire=['.analysis/draft.json'])
        self.assertTrue(draft.exists())
    def test_retirement_rejects_escaped_json_dependencies(self):
        draft = self.proof('.analysis/draft.json')
        for escaped in ['.analysis\\/draft.json', '\\u002eanalysis/draft.json']:
            self.put('.analysis/current.json', '{"inputs":{"'+escaped+'":"'+m.digest(draft)+'"}}')
            with self.assertRaisesRegex(ValueError,'retained JSON reference'):m.plan_cleanup(retire=['.analysis/draft.json'])
            self.assertTrue(draft.exists())
    def test_retirement_rejects_documented_proof(self):
        self.proof('.analysis/draft.json');self.put('README.md', 'Evidence .analysis/draft.json\n')
        with self.assertRaisesRegex(ValueError, 'documented'):m.plan_cleanup(retire=['.analysis/draft.json'])
    def test_retirement_cannot_ignore_fingerprint_field_in_ordinary_proof(self):
        draft = self.proof('.analysis/draft.json')
        self.put('.analysis/current.json', json.dumps(dict(inputs={}, reference_corpus={'.analysis/draft.json':m.digest(draft)})))
        with self.assertRaisesRegex(ValueError, 'retained JSON reference'):m.plan_cleanup(retire=['.analysis/draft.json'])
    def test_retirement_rejects_accepted_claim_and_private_identity(self):
        for name, data in [('.analysis/accepted.json',dict(inputs={},source_acceptance=False,exact_acceptance=True)),
                           ('.analysis/target-import.json',dict(inputs={},source_acceptance=False,exact_acceptance=False))]:
            path=self.put(name,json.dumps(data))
            with self.assertRaises(ValueError):m.plan_cleanup(retire=[name])
            self.assertTrue(path.exists())
    def test_output_rejects_traversal_symlink_and_existing_receipt(self):
        self.assertEqual(m.output_path('.analysis/closeout/run/receipt.json'),self.root/'.analysis/closeout/run/receipt.json')
        for name in ['.analysis/closeout/../receipt.json','/tmp/receipt.json','.analysis/receipt.json']:
            with self.assertRaises(ValueError):m.output_path(name)
        self.put('.analysis/closeout/existing/receipt.json','{}')
        with self.assertRaises(ValueError):m.output_path('.analysis/closeout/existing/receipt.json')
        (self.root/'.analysis/closeout/link').symlink_to(self.root/'external',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'):m.output_path('.analysis/closeout/link/receipt.json')


if __name__ == '__main__':
    unittest.main()
