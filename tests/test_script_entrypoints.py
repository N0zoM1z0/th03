"""Cache CLI requires an explicit apply and stays outside native output."""
import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import clean_generated


class ScriptEntrypoints(unittest.TestCase):
    def test_retired_cleanup_options_stop_before_planning_or_deleting(self):
        cases = [(clean_generated, ['--apply']),
                 (clean_generated, ['--prune-unreferenced-receipts'])]
        for module, args in cases:
            with self.subTest(command=module.__name__, args=args), \
                    patch.object(sys, 'argv', [module.__name__, *args]), \
                    patch.object(module, 'ROOT', Path('/nonexistent/no-cleanup')), \
                    contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    module.main()
                self.assertEqual(error.exception.code, 2)

    def test_cache_preview_and_apply_keep_analysis_out_of_scope(self):
        for args in (['--caches-only'], ['--caches-only', '--apply']):
            with self.subTest(args=args), patch.object(sys, 'argv', ['clean_generated', *args]), \
                    patch.object(clean_generated, 'clean_caches', return_value=0) as caches, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(clean_generated.main(), 0)
            self.assertEqual(caches.call_args.args[0], '--apply' not in args)


if __name__ == '__main__':
    unittest.main()
