"""Scope protections for intentionally conservative handoff artifact cleanup."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import cleanup_mainl_handoff_artifacts as clean


class HandoffCleanupSafety(unittest.TestCase):
    def test_refuse_absolute_and_path_traversal(self):
        for value in ('/etc/passwd','../outside','.analysis/work/../../etc/passwd'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                clean.checked_path(value)

    def test_latest_proof_is_explicitly_protected(self):
        stages=clean.current_layers()
        self.assertEqual((len(stages),stages[-1]),(56,('after317','nec-delay-mbyte')))
        required=clean.active_inputs(stages)
        latest=ROOT/'.analysis/work/mainl-after317-nec-delay-mbyte-build.json'
        self.assertIn(latest,required)
        obsolete,_=clean.candidates(stages,required)
        self.assertFalse(set(obsolete)&required)


if __name__=='__main__':
    unittest.main()
