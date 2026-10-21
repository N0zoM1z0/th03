"""Pending maintained registration does not earn source/exact acceptance."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import unittest
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("regist_progress", ROOT / "scripts/progress.py")
progress = importlib.util.module_from_spec(spec); spec.loader.exec_module(progress)
def units():
    return [{"id": "th03-mainl-decoded-" + name, "artifact": "th03-mainl", "segment": "decoded:095F",
             "offset": offset, "size": size, "boundary_state": "reviewed", "state": "boundary-reviewed", "source": ""}
            for name, offset, size in (("regist", "0x189e", "2720"), ("scoredat", "0x17b9", "229"))]
class PendingTests(unittest.TestCase):
    def test_pending_caption_without_credit(self):
        rows = units()
        self.assertTrue(progress.mainl_regist_source_pending(rows))
        svg = progress.render_svg(rows, [])
        self.assertIn("17 bodies / 2,949 B owned", svg)
        self.assertIn("native proof pending", svg)
        self.assertIn("Source 0/2", svg)
        self.assertIn("exact 0/2", svg)
    def test_mutated_or_incomplete_scopes_rejected(self):
        for key, value in {"state": "source-present", "size": "2721", "source": "src/mainl/regist.cpp"}.items():
            rows = units(); rows[0][key] = value
            self.assertFalse(progress.mainl_regist_source_pending(rows))
        self.assertFalse(progress.mainl_regist_source_pending(units()[:1]))
        self.assertFalse(progress.mainl_regist_source_pending(units() + units()))
    def test_absent_owner_hides_caption(self):
        with patch.object(Path, "is_file", return_value=False):
            self.assertFalse(progress.mainl_regist_source_pending(units()))
