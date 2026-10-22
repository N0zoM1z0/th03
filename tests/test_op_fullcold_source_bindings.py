"""Versioned replay maintenance must preserve cold source and historical guards."""
from pathlib import Path
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cold_source_bindings', ROOT/'scripts/replay_th03_op_fullcold_exact.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class SourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.binding = a.read_source_bindings(ROOT)

    def copy_binding_inputs(self, root):
        names = {a.SOURCE_BINDING_PATH, self.binding['dependency']['path'],
                 self.binding['pfopen_replay_binding']['path']}
        for entry in self.binding['replacements'].values():
            names.update((entry['current']['path'], entry['snapshot']['path']))
        for name in names:
            dest = root/name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/name, dest)

    def test_exact_historical_manifest_and_snapshot_bindings(self):
        original = json.loads(a.pin(ROOT, self.binding['dependency']))
        for entry in self.binding['replacements'].values():
            self.assertIn(entry['historical_install_entry'], original['files'])
            self.assertEqual(a.sha(a.pin(ROOT, entry['snapshot'])),
                             entry['historical_install_entry']['sha256'])
            self.assertNotEqual(entry['current']['sha256'], entry['snapshot']['sha256'])

    def test_current_and_historical_files_both_remain_required(self):
        for entry in self.binding['replacements'].values():
            for kind in ('current', 'snapshot'):
                with self.subTest(path=entry[kind]['path']), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    self.copy_binding_inputs(root)
                    path = root/entry[kind]['path']
                    path.write_bytes(path.read_bytes()+b'drift')
                    with self.assertRaisesRegex(ValueError, 'artifact pin drift'):
                        a.read_source_bindings(root)

    def test_snapshot_or_current_mode_drift_rejected(self):
        for entry in self.binding['replacements'].values():
            for kind in ('current', 'snapshot'):
                with self.subTest(path=entry[kind]['path']), tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    self.copy_binding_inputs(root)
                    (root/entry[kind]['path']).chmod(entry[kind]['mode'] ^ 0o100)
                    with self.assertRaisesRegex(ValueError, 'source binding mode'):
                        a.read_source_bindings(root)

    def test_binding_cannot_be_extended_or_rewritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.copy_binding_inputs(root)
            changed = copy.deepcopy(self.binding)
            changed['replacements']['src/shared/formats/pfopen.asm'] = next(iter(changed['replacements'].values()))
            (root/a.SOURCE_BINDING_PATH).write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError, 'artifact pin drift'):
                a.read_source_bindings(root)

    def test_wrong_dependency_or_historical_entry_rejected(self):
        for entry in self.binding['replacements'].values():
            for mutation in ('dependency', 'historical'):
                dependency = dict(self.binding['dependency'])
                historical = dict(entry['historical_install_entry'])
                if mutation == 'dependency':
                    dependency['sha256'] = '0'*64
                else:
                    historical['sha256'] = '0'*64
                with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'historical dependency'):
                    a.pin_source_dependency(ROOT, dependency, historical, self.binding)

    def test_consumed_source_cannot_use_replay_fallback(self):
        path = 'src/shared/formats/pfopen.asm'
        pin = dict(path=path, sha256='0'*64)
        with self.assertRaisesRegex(ValueError, 'artifact pin drift '+path):
            a.pin_source_dependency(ROOT, self.binding['dependency'], pin, self.binding)

    def test_virtual_historical_proposals_keep_original_pins(self):
        for entry in self.binding['replacements'].values():
            with self.subTest(path=entry['current']['path']), self.assertRaisesRegex(ValueError, 'artifact pin drift'):
                a.pin_source_dependency(ROOT, self.binding['dependency'], entry['historical_install_entry'], None)

    def test_snapshot_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.copy_binding_inputs(root)
            entry = next(iter(self.binding['replacements'].values()))
            path = root/entry['snapshot']['path']
            path.unlink()
            path.symlink_to(ROOT/entry['snapshot']['path'])
            with self.assertRaisesRegex(ValueError, 'artifact symlink'):
                a.read_source_bindings(root)


if __name__ == '__main__':
    unittest.main()
