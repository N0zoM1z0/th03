"""Historical ZUN standalone proof stays outside all progress denominators."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("zun_progress", ROOT / "scripts/progress.py")
progress = module_from_spec(SPEC)
SPEC.loader.exec_module(progress)


def initializer():
    return {"id": "th03-zun-decoded-init", "artifact": "th03-zun",
            "segment": "decoded-COM", "offset": "0x6c4", "size": "1390",
            "boundary_state": "reviewed", "state": "boundary-reviewed"}


class ZunProgressTests(unittest.TestCase):
    def test_standalone_annotation_changes_no_acceptance_or_inventory(self):
        row = initializer()
        main = {"id": "main-exact", "artifact": "th03-main", "state": "exact", "size": "10"}
        before = progress.render_svg([main], [], [])
        after = progress.render_svg([main, row], [], [])
        added = [line for line in after.splitlines() if "Retained standalone init:" in line]
        self.assertEqual(len(added), 1)
        self.assertIn("2 materializations · 9 procedures / 1,390 B · no exact credit", added[0])
        self.assertEqual(after.replace(added[0] + "\n", ""), before)
        self.assertIn("Inventory pending", after)
        self.assertNotIn("9 tracked functions", after)
        self.assertIn("MAIN verified exact extents: 10 bytes · 1 owners", after)
        self.assertIn("no whole-game completion percentage", after)

    def test_annotation_requires_unique_unchanged_reviewed_scope(self):
        self.assertFalse(progress.zun_init_standalone_retained([]))
        self.assertFalse(progress.zun_init_standalone_retained([initializer(), initializer()]))
        changes = {"id": "other", "artifact": "th03-main", "segment": "decoded:-2",
                   "offset": "0x6c5", "size": "607", "boundary_state": "provisional",
                   "state": "exact"}
        for field, value in changes.items():
            with self.subTest(field=field):
                row = initializer()
                row[field] = value
                self.assertFalse(progress.zun_init_standalone_retained([row]))
                self.assertNotIn("Retained standalone init:", progress.render_svg([row], [], []))


if __name__ == "__main__":
    unittest.main()
