"""A source checkpoint caption never advances MAINL acceptance bars."""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cutscene_progress", ROOT / "scripts/progress.py")
progress = importlib.util.module_from_spec(spec)
spec.loader.exec_module(progress)

def unit():
    return {"id": "th03-mainl-decoded-cutscene", "artifact": "th03-mainl",
            "segment": "decoded:095F", "offset": "0xb3e", "size": "3195",
            "boundary_state": "reviewed", "state": "boundary-reviewed", "source": ""}

class CutsceneCaptionTests(unittest.TestCase):
    def test_owner_caption_without_acceptance(self):
        rows = [unit()]
        self.assertTrue(progress.mainl_cutscene_source_pending(rows))
        svg = progress.render_svg(rows, [])
        self.assertIn("Cutscene owner: 13 bodies / 3,195 B", svg)
        self.assertIn("native proof pending", svg)
        self.assertIn("Source 0/1", svg)
        self.assertIn("exact 0/1", svg)
        self.assertEqual(progress.mainl_unit_progress(rows)["source_bytes"], 0)

    def test_changed_scope_or_state_does_not_keep_pending_caption(self):
        for key, value in {"state": "source-present", "size": "3196",
                           "source": "src/mainl/cutscene.cpp", "offset": "0xb3f"}.items():
            row = unit(); row[key] = value
            self.assertFalse(progress.mainl_cutscene_source_pending([row]))
        self.assertFalse(progress.mainl_cutscene_source_pending([unit(), unit()]))

    def test_missing_owner_does_not_show_caption(self):
        with patch.object(Path, "is_file", return_value=False):
            self.assertFalse(progress.mainl_cutscene_source_pending([unit()]))

if __name__ == "__main__":
    unittest.main()
