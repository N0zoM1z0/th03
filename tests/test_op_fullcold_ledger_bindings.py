"""Archive metadata remains exact while current ledgers and build sources stay checked."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/op-pfopen-checkpoint-proposal-v01/install-manifest.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

from pathlib import Path
import copy
import importlib.util
import json
import shutil
import tempfile
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'cold_ledger_bindings', ROOT/'scripts/replay_th03_op_fullcold_exact.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class LedgerBindingTests(unittest.TestCase):
    def setUp(self):
        self.binding = a.read_ledger_bindings(ROOT)
        self.source_binding = a.read_source_bindings(ROOT)

    def test_exact_git_blobs_match_original_install_entries(self):
        original = json.loads(a.pin(ROOT, self.binding['dependency']))
        self.assertEqual(set(self.binding['entries']),
                         {'config/evidence.csv', 'config/knowledge.csv'})
        for name, entry in self.binding['entries'].items():
            self.assertIn(entry['historical_install_entry'], original['files'])
            raw = a.read_git_ledger_snapshot(ROOT, entry['git_snapshot'])
            self.assertEqual(a.sha(raw), entry['historical_install_entry']['sha256'])

    def test_immutable_git_provenance_and_modes_required(self):
        snapshot = next(iter(self.binding['entries'].values()))['git_snapshot']
        for key, value in [('commit', 'HEAD'), ('blob', 'f'*40), ('git_mode', 0o100755),
                           ('sha256', '0'*64), ('bytes', 0),
                           ('path', 'src/shared/formats/pfopen.asm')]:
            changed = dict(snapshot, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                a.read_git_ledger_snapshot(ROOT, changed)

    def test_wrong_dependency_or_install_entry_rejected(self):
        for entry in self.binding['entries'].values():
            for key in ('dependency', 'historical'):
                dependency = dict(self.binding['dependency'])
                historical = dict(entry['historical_install_entry'])
                (dependency if key == 'dependency' else historical)['sha256'] = '0'*64
                with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'historical dependency'):
                    a.pin_source_dependency(ROOT, dependency, historical,
                                            self.source_binding, self.binding)

    def test_original_logical_mode_is_separate_from_git_tree_mode(self):
        changed = copy.deepcopy(self.binding)
        name = 'config/evidence.csv'
        entry = changed['entries'][name]
        self.assertEqual(entry['git_snapshot']['git_mode'], 0o100644)
        entry['git_snapshot']['mode'] ^= 0o040
        with self.assertRaisesRegex(ValueError, 'archival install content identity'):
            a.pin_source_dependency(ROOT, changed['dependency'],
                                    entry['historical_install_entry'],
                                    self.source_binding, changed)

    def test_consumed_product_source_cannot_use_archival_ledger_binding(self):
        name = 'src/shared/formats/pfopen.asm'
        entry = dict(path=name, sha256='0'*64)
        with self.assertRaisesRegex(ValueError, 'artifact pin drift'):
            a.pin_source_dependency(ROOT, self.binding['dependency'], entry,
                                    self.source_binding, self.binding)
        changed = copy.deepcopy(self.binding)
        changed['entries'][name] = next(iter(changed['entries'].values()))
        with self.assertRaisesRegex(ValueError, 'archival ledger scope'):
            a.pin_source_dependency(ROOT, changed['dependency'], entry,
                                    self.source_binding, changed)

    def test_ledger_cannot_be_reclassified_as_a_compiled_input(self):
        changed = copy.deepcopy(a.proof(ROOT))
        changed['source_inventory']['config/evidence.csv'] = dict(sha256='0'*64, bytes=1)
        with mock.patch.object(a, 'proof', return_value=changed):
            with self.assertRaisesRegex(ValueError, 'must not be composed source inputs'):
                a.check_current_sources(ROOT)

    def test_historical_binding_never_masks_current_ledger_validation(self):
        self.assertTrue(a.validate_current_ledgers(ROOT, self.binding))
        validator = mock.Mock(return_value=1)
        with mock.patch.object(a, 'load', return_value=types.SimpleNamespace(main=validator)):
            with self.assertRaisesRegex(ValueError, 'current canonical ledger validation'):
                a.validate_current_ledgers(ROOT, self.binding)
        validator.assert_called_once_with(ROOT, validate_product=False)

    def test_current_validator_bytes_modes_and_symlinks_required(self):
        q = self.binding['current_ledger_validator']
        for mutation in ('bytes', 'mode', 'symlink'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                dest = root/q['path']
                dest.parent.mkdir(parents=True)
                shutil.copy2(ROOT/q['path'], dest)
                if mutation == 'bytes':
                    dest.write_bytes(dest.read_bytes()+b'drift')
                elif mutation == 'mode':
                    dest.chmod(q['mode'] ^ 0o100)
                else:
                    dest.unlink()
                    dest.symlink_to(ROOT/q['path'])
                with self.assertRaises(ValueError):
                    a.validate_current_ledgers(root, self.binding)

    def test_binding_file_changes_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            dest = root/a.LEDGER_BINDING_PATH
            dest.parent.mkdir(parents=True)
            changed = copy.deepcopy(self.binding)
            changed['entries']['config/units.csv'] = next(iter(changed['entries'].values()))
            dest.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, 'artifact pin drift'):
                a.read_ledger_bindings(root)

    def test_virtual_proposal_path_keeps_original_ledger_pins(self):
        for entry in self.binding['entries'].values():
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                historical = entry['historical_install_entry']
                raw = a.read_git_ledger_snapshot(ROOT, entry['git_snapshot'])
                path = root/historical['path']
                path.parent.mkdir(parents=True)
                path.write_bytes(raw)
                self.assertEqual(a.pin_source_dependency(
                    root, self.binding['dependency'], historical, None), raw)
                path.write_bytes(raw+b'drift')
                with self.assertRaisesRegex(ValueError, 'artifact pin drift'):
                    a.pin_source_dependency(root, self.binding['dependency'],
                                            historical, None)


if __name__ == '__main__':
    unittest.main()
