"""Source-only ZUN logo overlay tests; no compiler, emulator or target reads."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
# Works in the ignored proposal and after parent installs into tests/.
SCRIPT = HERE / 'stage_th03_zunsoft.py'
ROOT = HERE
if not SCRIPT.exists():
    ROOT = HERE.parent
    SCRIPT = ROOT / 'scripts/stage_th03_zunsoft.py'
spec = importlib.util.spec_from_file_location('zunsoft_stage', SCRIPT)
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)

class ZunsoftStageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=HERE)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'
        for name in stage.INPUTS:
            dest = self.source / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)

    def test_repeat_and_scope(self):
        first = stage.stage(self.source, self.base / 'a')
        second = stage.stage(self.source, self.base / 'b')
        self.assertEqual(first, second)
        self.assertEqual(len(first['files']), 7)
        self.assertEqual(first['source_shape']['historical_code_size'], 1299)
        self.assertFalse(first['exact_acceptance'])
        self.assertFalse(first['whole_payload_ownership'])
        self.assertEqual(sum(p['historical_size'] for p in first['source_shape']['procedures']), 1299)
        for name in (*first['files'], 'source_inventory.json'):
            self.assertEqual((self.base/'a'/name).read_bytes(), (self.base/'b'/name).read_bytes())

    def test_existing_output_rejected(self):
        out = self.base/'out'
        out.mkdir()
        with self.assertRaisesRegex(ValueError, 'exclusive fresh'):
            stage.stage(self.source, out)

    def test_root_edit_rejected_before_output(self):
        p = self.source/stage.OWNER
        p.write_bytes(p.read_bytes().replace(b'char wave_phase;', b'unsigned char wave_phase;'))
        with self.assertRaisesRegex(ValueError, 'identity differs'):
            stage.stage(self.source, self.base/'out')
        self.assertFalse((self.base/'out').exists())

    def test_forwarding_edit_rejected_before_output(self):
        (self.source/stage.COMPAT[0]).write_text('#include "unreviewed.hpp"\n')
        with self.assertRaisesRegex(ValueError, 'compat edge differs'):
            stage.stage(self.source, self.base/'out')
        self.assertFalse((self.base/'out').exists())

    def test_symlink_input_rejected(self):
        p = self.source/stage.OWNER
        p.unlink()
        p.symlink_to((ROOT/stage.OWNER).resolve())
        with self.assertRaisesRegex(ValueError, 'symlink'):
            stage.stage(self.source, self.base/'out')

    def test_symlink_output_parent_rejected(self):
        link = self.base/'linked'
        link.symlink_to(self.source.resolve(), target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            stage.stage(self.source, link/'out')

    def test_missing_dependency_rejected(self):
        (self.source/stage.COMPAT[-1]).unlink()
        with self.assertRaises(FileNotFoundError):
            stage.stage(self.source, self.base/'out')
        self.assertFalse((self.base/'out').exists())

if __name__ == '__main__':
    unittest.main()
