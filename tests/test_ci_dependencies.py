import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ci


class DependencyControls(unittest.TestCase):
    def test_missing_dependency_fails_before_tests_or_private_tools(self):
        for missing in ('unicorn', 'capstone'):
            with self.subTest(missing=missing), \
                    patch.object(ci, 'find_spec', side_effect=lambda name: None if name == missing else object()), \
                    patch.object(ci, 'run') as run:
                output = io.StringIO()
                with contextlib.redirect_stderr(output):
                    self.assertEqual(ci.main(), 1)
                run.assert_not_called()
                self.assertIn(missing, output.getvalue())
                self.assertIn('requirements-ci.txt', output.getvalue())
                self.assertIn(sys.executable, output.getvalue())


if __name__ == '__main__':
    unittest.main()
