"""MAINL progress uses unit extents and keeps diagnostic evidence out of acceptance."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("mainl_progress", ROOT / "scripts/progress.py")
progress = module_from_spec(SPEC)
SPEC.loader.exec_module(progress)


def heap():
    return {
        "id": progress.MAINL_HEAP_UNIT, "artifact": "th03-mainl",
        "kind": "module-candidate", "segment": "decoded:0000",
        "offset": "0x210a", "size": "628", "boundary_state": "reviewed",
        "state": "source-present", "source": "src/mainl/memory/heap.inl",
        "evidence_ids": ";".join(progress.MAINL_HEAP_RETAINED),
    }


def other():
    row = heap()
    row.update(id="other-mainl-extent", kind="function", offset="0x2400",
               size="20", state="boundary-reviewed", source="", evidence_ids="")
    return row


def evidence():
    return [
        {"id": name, "oracle": "analysis-bundle", "artifact": "th03-mainl",
         "unit_id": progress.MAINL_HEAP_UNIT, "extent_start": "0x210a",
         "extent_size": "628", "evidence_class": kind, "result": "pass",
         "output_sha256": digest}
        for name, (kind, digest) in progress.MAINL_HEAP_RETAINED.items()
    ]


def artifact_row(svg, artifact):
    label = f">{artifact}</text>"
    lines = svg.splitlines()
    start = next(i for i, line in enumerate(lines) if label in line)
    return lines[start:start + 8]


class MainlProgressTests(unittest.TestCase):
    def test_mixed_function_module_units_do_not_become_function_counts(self):
        rows = [heap(), other()]
        self.assertEqual(progress.mainl_unit_progress(rows),
                         {"total": 2, "reviewed": 2, "source": 1,
                          "source_bytes": 628, "exact": 0})
        fake_functions = [{"artifact": "th03-mainl", "state": "exact",
                           "boundary_state": "reviewed"}] * 17
        svg = progress.render_svg(rows, fake_functions, evidence())
        self.assertIn("2 tracked unit extents", svg)
        self.assertIn("Reviewed 2 · Source 1/2", svg)
        self.assertIn("Unit acceptance: exact 0/2", svg)
        self.assertNotIn("17 tracked", svg)
        self.assertIn('width="125.00" height="5" fill="#e0af68"', svg)

    def test_source_and_retained_passes_never_inflate_exact_acceptance(self):
        rows = [heap(), other()]
        self.assertTrue(progress.mainl_heap_retained(rows, evidence()))
        self.assertEqual(progress.mainl_unit_progress(rows)["exact"], 0)
        svg = progress.render_svg(rows, [], evidence())
        self.assertIn("8 procedures / 628 B retained-only", svg)
        self.assertIn("Unit acceptance: exact 0/2", svg)
        self.assertIn("MAIN verified exact extents: 0 bytes · 0 owners", svg)
        self.assertIn("no whole-game completion percentage", svg)

    def test_source_requires_state_and_path(self):
        rows = [heap(), other()]
        rows[0]["source"] = ""
        rows[1]["source"] = "src/mainl/not_maintained.inl"
        self.assertEqual(progress.mainl_unit_progress(rows)["source"], 0)
        self.assertEqual(progress.mainl_unit_progress(rows)["source_bytes"], 0)

    def test_duplicate_units_rejected_and_exclusions_not_counted(self):
        with self.assertRaisesRegex(ValueError, "inflate"):
            progress.mainl_unit_progress([heap(), heap()])
        excluded = other()
        excluded["state"] = "excluded"
        self.assertEqual(progress.mainl_unit_progress([heap(), excluded])["total"], 1)

    def test_retained_annotation_requires_both_unique_linked_records(self):
        rows = [heap()]
        for records in ([], evidence()[:1], evidence() + [evidence()[0]]):
            with self.subTest(records=records):
                self.assertFalse(progress.mainl_heap_retained(rows, records))
        rows[0]["evidence_ids"] = ""
        self.assertFalse(progress.mainl_heap_retained(rows, evidence()))

    def test_wrong_result_oracle_hash_scope_and_class_reject_annotation(self):
        changes = {"result": "fail", "oracle": "raw-bytes",
                   "artifact": "th03-main", "unit_id": "other",
                   "extent_start": "0x210b", "extent_size": "625",
                   "evidence_class": "upstream", "output_sha256": "0" * 64}
        for field, value in changes.items():
            with self.subTest(field=field):
                records = evidence()
                records[0][field] = value
                self.assertFalse(progress.mainl_heap_retained([heap()], records))

    def test_unit_scope_and_status_changes_cannot_keep_retained_caption(self):
        changes = {"artifact": "th03-main", "segment": "decoded:0001",
                   "offset": "0x210b", "size": "625", "boundary_state": "provisional",
                   "state": "exact", "source": "src/mainl/other.inl"}
        for field, value in changes.items():
            with self.subTest(field=field):
                row = heap()
                row[field] = value
                self.assertFalse(progress.mainl_heap_retained([row], evidence()))
        self.assertFalse(progress.mainl_heap_retained([heap(), heap()], evidence()))

    def test_unrelated_artifacts_and_main_accepted_totals_unchanged(self):
        main = {"id": "main-exact", "artifact": "th03-main", "state": "exact", "size": "10"}
        functions = [{"artifact": "th03-main", "state": "exact", "boundary_state": "reviewed"}]
        before = progress.render_svg([main, other()], functions, [])
        after = progress.render_svg([main, other(), heap()], functions, evidence())
        for name in ("OP.EXE", "MAIN.EXE", "ZUN.COM"):
            with self.subTest(name=name):
                self.assertEqual(artifact_row(before, name), artifact_row(after, name))
        self.assertIn("MAIN verified exact extents: 10 bytes · 1 owners", after)

    def test_empty_mainl_inventory_has_no_percentage_or_retained_credit(self):
        svg = progress.render_svg([], [], [])
        self.assertIn("0 tracked unit extents", svg)
        self.assertIn("Unit acceptance: exact 0/0", svg)
        self.assertNotIn("628 B retained-only", svg)


if __name__ == "__main__":
    unittest.main()
