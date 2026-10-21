import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import progress

class GraphicsProgressTests(unittest.TestCase):
    def test_installed_source_and_metadata_enable_annotation(self):
        self.assertTrue(progress.mainl_graphics_producer_pending())
        with patch.object(progress, "mainl_graphics_linked", return_value=False):
            self.assertIn("333 non-fixup B match", progress.render_svg([], [], []))
            self.assertIn("9 fixups / 22 B await link", progress.render_svg([], [], []))

    def test_missing_or_changed_source_disables_annotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertFalse(progress.mainl_graphics_producer_pending(root))
            for name in progress.MAINL_GRAPHICS_PRODUCER_PINS:
                p = root/name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((progress.ROOT/name).read_bytes())
            self.assertTrue(progress.mainl_graphics_producer_pending(root))
            (root/"src/mainl/formats/cdg_effects.cpp").write_text("changed")
            self.assertFalse(progress.mainl_graphics_producer_pending(root))

    def test_annotation_cannot_change_source_or_exact_counts(self):
        counts = progress.mainl_unit_progress([])
        with patch.object(progress, "mainl_graphics_producer_pending", return_value=True):
            enabled = progress.render_svg([], [], [])
        with patch.object(progress, "mainl_graphics_producer_pending", return_value=False):
            disabled = progress.render_svg([], [], [])
        self.assertEqual(counts, progress.mainl_unit_progress([]))
        for svg in (enabled, disabled):
            self.assertIn("Unit acceptance: exact 0/0", svg)
            self.assertIn("Source 0/0", svg)
        self.assertNotIn("333 non-fixup B match", disabled)

    def test_linked_caption_is_not_acceptance(self):
        self.assertTrue(progress.mainl_graphics_linked())
        svg = progress.render_svg([], [], [])
        self.assertIn("Linked graphics: 355 B target-equal", svg)
        self.assertIn("decoded 1 DATA byte remains", svg)
        self.assertIn("Unit acceptance: exact 0/0", svg)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(progress.mainl_graphics_linked(Path(tmp)))
