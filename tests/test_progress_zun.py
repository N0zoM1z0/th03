"""Historical ZUN diagnostics do not confer source or exact unit acceptance."""

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
    def test_standalone_annotation_changes_unit_inventory_not_acceptance(self):
        row = initializer()
        main = {"id": "main-exact", "artifact": "th03-main", "state": "exact", "size": "10"}
        before = progress.render_svg([main], [], [])
        after = progress.render_svg([main, row], [], [])
        added = [line for line in after.splitlines() if "Retained standalone init:" in line]
        self.assertEqual(len(added), 1)
        self.assertIn("2 materializations · 9 procedures / 1,390 B · no exact credit", added[0])
        self.assertEqual(progress.tracked_unit_progress([row], "th03-zun"),
                         {"total": 1, "reviewed": 1, "source": 0, "exact": 0})
        self.assertIn("0 tracked unit extents", before)
        self.assertIn("Unit acceptance: exact 0/1", after)
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

    def test_composition_annotation_changes_unit_inventory_not_acceptance(self):
        main = {"id": "main-exact", "artifact": "th03-main", "state": "exact", "size": "10"}
        before = progress.render_svg([main, initializer()], [], [])
        after = progress.render_svg([main, initializer(), driver()], [], [])
        added = [line for line in after.splitlines() if "Maintained -2/-4 composition:" in line]
        self.assertEqual(len(added), 1)
        self.assertIn("22,812 B · mixed retained inputs · 10 target differences · no exact credit", added[0])
        self.assertIn("three retained other payloads and retained wrapper scaffold", added[0])
        self.assertIn("raw OBJ/COM/MAP equality, no normalization or object reuse", added[0])
        self.assertIn("first was not a predeclared pair", added[0])
        self.assertIn("second source mtimes were declared from observed first inputs", added[0])
        self.assertIn("Fourteen wrapper-only observations and wrong-transfer negative pass", added[0])
        self.assertIn("no payload execution or native composition build", added[0])
        self.assertIn("no exact acceptance or DIET closure", added[0])
        self.assertEqual(progress.tracked_unit_progress([initializer(), driver()], "th03-zun"),
                         {"total": 2, "reviewed": 2, "source": 0, "exact": 0})
        self.assertIn("Unit acceptance: exact 0/1", before)
        self.assertIn("Unit acceptance: exact 0/2", after)
        self.assertIn("Retained standalone init:", after)
        self.assertIn("Inventory pending", after)
        self.assertNotIn("55 tracked functions", after)
        self.assertIn("MAIN verified exact extents: 10 bytes · 1 owners", after)
        self.assertIn("no whole-game completion percentage", after)

    def test_composition_annotation_requires_unique_unchanged_reviewed_scope(self):
        self.assertFalse(progress.zun_driver_hybrid_retained([]))
        self.assertFalse(progress.zun_driver_hybrid_retained([driver()]))
        self.assertFalse(progress.zun_driver_hybrid_retained([initializer(), driver(), driver()]))
        self.assertFalse(progress.zun_driver_hybrid_retained([initializer(), initializer(), driver()]))
        changes = {"id": "other", "artifact": "th03-main", "segment": "decoded:-4",
                   "offset": "0x33a3", "size": "2844", "boundary_state": "provisional",
                   "state": "exact"}
        for field, value in changes.items():
            with self.subTest(field=field):
                row = driver()
                row[field] = value
                self.assertFalse(progress.zun_driver_hybrid_retained([initializer(), row]))
                self.assertNotIn("Maintained -2/-4 composition:", progress.render_svg([initializer(), row], [], []))


if __name__ == "__main__":
    unittest.main()
