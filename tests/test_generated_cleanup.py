"""Cache cleanup leaves product output and external directories alone."""
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib
import io
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import clean_generated as cleanup


class CacheCleanup(unittest.TestCase):
    def test_preview_then_apply_only_removes_caches(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            caches = ['scripts/pkg/__pycache__/code.pyc', '.pytest_cache/result']
            preserved = ['.analysis/work/current.obj', 'build/current.exe', 'src/current.cpp']
            for name in caches + preserved:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'content')
            with patch.object(cleanup, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                self.assertGreater(cleanup.clean_caches(True), 0)
                self.assertTrue(all((root / p).exists() for p in caches + preserved))
                cleanup.clean_caches(False)
            self.assertTrue(all(not (root / p).exists() for p in caches))
            self.assertTrue(all((root / p).exists() for p in preserved))

    def test_symlinked_caches_and_source_directories_are_skipped(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as external:
            root = Path(folder)
            target = Path(external)
            (target / '__pycache__').mkdir()
            (target / '__pycache__/keep.pyc').write_bytes(b'keep')
            (root / '.pytest_cache').symlink_to(target, target_is_directory=True)
            (root / 'scripts').symlink_to(target, target_is_directory=True)
            with patch.object(cleanup, 'ROOT', root), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cleanup.clean_caches(False), 0)
            self.assertTrue((target / '__pycache__/keep.pyc').exists())
            self.assertTrue((root / '.pytest_cache').is_symlink())


if __name__ == '__main__':
    unittest.main()
