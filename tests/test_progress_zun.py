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


def driver():
    return {"id": "th03-zun-decoded-sprite16-driver", "artifact": "th03-zun",
            "segment": "decoded-COM", "offset": "0x33a2", "size": "4224",
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

    def test_standalone_driver_annotation_changes_no_acceptance_or_inventory(self):
        main = {"id": "main-exact", "artifact": "th03-main", "state": "exact", "size": "10"}
        before = progress.render_svg([main, initializer()], [], [])
        after = progress.render_svg([main, initializer(), driver()], [], [])
        added = [line for line in after.splitlines() if "Maintained standalone driver:" in line]
        self.assertEqual(len(added), 1)
        self.assertIn("4,224 B · candidate-only · 10 target differences · no exact credit", added[0])
        self.assertIn("not two cold rounds or exact acceptance", added[0])
        self.assertIn("Candidate raw equality, not target equality", added[0])
        self.assertIn("Ten maintained sources own the complete driver", added[0])
        self.assertIn("55 procedures / 2,844 bytes plus 1,380 data/layout bytes", added[0])
        self.assertIn("all ten differences are in owned procedure bodies", added[0])
        self.assertEqual(after.replace(added[0] + "\n", ""), before)
        self.assertIn("Retained standalone init:", after)
        self.assertIn("Inventory pending", after)
        self.assertNotIn("55 tracked functions", after)
        self.assertIn("MAIN verified exact extents: 10 bytes · 1 owners", after)
        self.assertIn("no whole-game completion percentage", after)

    def test_standalone_driver_annotation_requires_unique_unchanged_reviewed_scope(self):
        self.assertFalse(progress.zun_driver_hybrid_retained([]))
        self.assertFalse(progress.zun_driver_hybrid_retained([driver(), driver()]))
        changes = {"id": "other", "artifact": "th03-main", "segment": "decoded:-4",
                   "offset": "0x33a3", "size": "2844", "boundary_state": "provisional",
                   "state": "exact"}
        for field, value in changes.items():
            with self.subTest(field=field):
                row = driver()
                row[field] = value
                self.assertFalse(progress.zun_driver_hybrid_retained([row]))
                self.assertNotIn("Maintained standalone driver:", progress.render_svg([row], [], []))


if __name__ == "__main__":
    unittest.main()
