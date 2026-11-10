"""Basic CI checks real worktrees and committed PR/push changes without private tools."""
import contextlib
import io
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ci


class BasicChecks(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.name', 'CI test')
        self.git('config', 'user.email', 'ci@example.invalid')
        self.git('config', 'core.whitespace', 'blank-at-eol,blank-at-eof')
        self.write('README.md', 'Initial\n')
        self.commit()
        self.patch = patch.object(ci, 'ROOT', self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root).decode().strip()

    def write(self, name, content):
        (self.root / name).write_text(content)

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-qm', 'Test change')
        return self.git('rev-parse', 'HEAD')

    def check(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return ci.main(list(args))

    def test_untracked_machine_syntax_positive_and_negative(self):
        for name, good, bad in [('unit.py', 'x = 1\n', 'def (: \n'),
                                ('data.json', '{"ok": true}\n', '{'),
                                ('config.toml', 'ok = true\n', 'ok = ['),
                                ('probe.sh', 'echo ok\n', 'if then\n')]:
            with self.subTest(name=name):
                self.write(name, good)
                self.assertEqual(self.check(), 0)
                self.write(name, bad)
                self.assertEqual(self.check(), 1)
                (self.root / name).unlink()

    def test_clean_checkout_checks_committed_whitespace(self):
        self.write('README.md', 'Trailing space \n')
        self.commit()
        self.assertEqual(self.check(), 1)

    def test_base_covers_earlier_commits_in_a_push_or_pr(self):
        base = self.git('rev-parse', 'HEAD')
        self.write('unit.py', 'def (: \n')
        self.commit()
        self.write('README.md', 'Later docs change\n')
        self.commit()
        self.assertEqual(self.check('--base', base), 1)

    def test_deleted_file_and_first_push_base(self):
        self.assertEqual(self.check('--base', '0' * 40), 0)
        self.write('unit.py', 'def (: \n')
        self.commit()
        (self.root / 'unit.py').unlink()
        self.assertEqual(self.check(), 0)


if __name__ == '__main__':
    unittest.main()
