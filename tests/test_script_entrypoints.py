"""Current CLI checks must not select old broad/deletion behavior accidentally."""
import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ci
import clean_generated
import closeout_cleanup


class ScriptEntrypoints(unittest.TestCase):
    def test_full_dispatch_uses_the_running_interpreter(self):
        with patch.object(ci.subprocess, 'call', return_value=7) as run:
            self.assertEqual(ci.main(['--full']), 7)
        self.assertEqual(run.call_args.args[0], [sys.executable, str(ci.ROOT / 'scripts/ci-full.py')])

    def test_unknown_full_option_does_not_run_a_suite(self):
        with patch.object(ci.subprocess, 'call') as run, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                ci.main(['--full', '--typo'])
        self.assertEqual(error.exception.code, 2)
        run.assert_not_called()

    def test_scoped_ci_does_not_dispatch_the_broad_suite(self):
        with patch.object(ci.subprocess, 'call') as broad, \
                patch.object(ci.subprocess, 'check_output', return_value=b''), \
                patch.object(ci.subprocess, 'run'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ci.main([]), 0)
        broad.assert_not_called()

    def test_retired_cleanup_options_stop_before_planning_or_deleting(self):
        cases = [(clean_generated, ['--apply']),
                 (clean_generated, ['--prune-unreferenced-receipts']),
                 (closeout_cleanup, ['--output', '.analysis/unused.json', '--apply']),
                 (closeout_cleanup, ['--output', '.analysis/unused.json', '--retire-proof', 'old.json'])]
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
                    patch.object(clean_generated, 'clean_analysis') as analysis, \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(clean_generated.main(), 0)
            analysis.assert_not_called()
            self.assertEqual(caches.call_args.args[0], '--apply' not in args)


if __name__ == '__main__':
    unittest.main()
