"""Native segment gaps and real group/relative relocation semantics."""

from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.zun_driver_layout import review, resolve_native, CONTRIBUTIONS
from lib.zun_driver_alignment import variants
from lib.zun_work_source import compose
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"


@unittest.skipUnless((WORK / "product/zun.target.com").is_file(), "private current native ZUN absent")
class NativeDriverAlignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = (WORK / "driver/driver.obj").read_bytes()
        cls.map = (WORK / "driver/driver.map").read_bytes()
        cls.candidate = (WORK / "driver/driver.com").read_bytes()

    def test_eight_paragraph_gaps_are_linked_not_initialized_object_bytes(self):
        layout = review(self.obj, self.map)
        image, fixups, blocks = resolve_native(self.obj)
        self.assertEqual(image, self.candidate)
        self.assertEqual(layout["layout_profile"], "native-paragraph-contributions")
        self.assertEqual((len(layout["alignment_gaps"]), layout["linker_zero_bytes"], layout["explicit_gap_fillers"]), (8, 71, 0))
        self.assertEqual(sum(size for _, size in blocks), 4224 - 71)
        initialized = {at for start, size in blocks for at in range(start, start + size)}
        for start, end in layout["alignment_gaps"]:
            self.assertFalse(initialized & set(range(start, end)))
            self.assertEqual(end, (start + 15) & ~15)
            self.assertEqual(image[start - 256:end - 256], bytes(end - start))

    def test_real_group_offsets_and_self_relative_near_calls_are_resolved(self):
        image, fixups, _ = resolve_native(self.obj)
        self.assertEqual(image, self.candidate)
        self.assertEqual(len(fixups), 206)
        self.assertEqual(sum(f["self_relative"] for f in fixups), 54)
        self.assertEqual(sum(f["width"] == 4 for f in fixups), 1)
        call, = [f for f in fixups if f["address"] == 0xAD1]
        self.assertEqual((call["target_address"], call["resolved"]), (0x69D, 0xFBCA))
        state, = [f for f in fixups if f["address"] == 0x343]
        self.assertEqual((state["target_address"], state["resolved"]), (0x1064, 0x1064))

    def test_native_alignment_attribute_cannot_be_changed_without_layout_review(self):
        changed = mutate_record(self.obj, lambda r: r.name == "SEGDEF" and r.data[0] == 0x68,
                                lambda d: b"\x48" + d[1:])
        with self.assertRaisesRegex(ValueError, "paragraph CODE contribution layout"): resolve_native(changed)

    def test_map_alignment_and_all_contribution_addresses_are_required(self):
        changed = self.map.replace(b"ACBP=68", b"ACBP=48", 1)
        with self.assertRaisesRegex(ValueError, "owner/alignment"): review(self.obj, changed)
        self.assertEqual(len(CONTRIBUTIONS), 9)

    def test_source_control_changes_only_root_alignment_directives(self):
        files, _, _ = compose(ROOT)
        baseline = {n.removeprefix("driver/"): raw for n, raw in files.items() if n.startswith("driver/")}
        controls = dict(variants(files))
        self.assertEqual(set(controls), {"word", "no-even"})
        for changed in controls.values():
            self.assertEqual({n for n in baseline if baseline[n] != changed[n]}, {"driver.asm"})
        self.assertNotIn(b"segment para", controls["word"]["driver.asm"])
        self.assertNotIn(b"\r\neven\r\n", controls["no-even"]["driver.asm"])

    def test_actual_native_control_outputs_reject_equality_for_both_reasons(self):
        report = json.loads((ROOT / ".analysis/work/zun-build.json").read_bytes())
        word, even = report["driver_alignment_controls"]["controls"]
        self.assertTrue(word["byte_exact_rejected"] and even["byte_exact_rejected"])
        self.assertEqual(word["candidate_bytes"], 4156)
        self.assertEqual((even["candidate_bytes"], even["differing_bytes"]), (4224, 33))
        self.assertTrue(all(c["all_procedure_includes_unchanged"] for c in (word, even)))
