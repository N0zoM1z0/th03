"""A passing summary cannot replace proof of two complete cold output vectors."""

from pathlib import Path
import copy
import hashlib
import json
import sys
import tomllib
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from review_th03_main_native_units import review, verify_maintained_sources, verify_native_coverage, producer_ownership
from lib.pc98 import parse_mz


@unittest.skipUnless((ROOT / ".analysis/targets/th03/main.exe").is_file(), "private target absent")
class NativeCompilerTables(unittest.TestCase):
    def setUp(self):
        config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
        self.unit = next(u for u in config["native_units"] if u["id"] == "th03-main-stage-round")
        self.extent = self.unit["code_extents"][0]
        self.program = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes()).program_image

    def test_compiler_data_has_complete_coverage_and_owned_destinations(self):
        data = verify_native_coverage(self.unit["functions"], self.extent, self.program)
        self.assertEqual(sum(r["size"] for r in data), 48)

    def test_switch_cannot_point_outside_the_owned_function(self):
        program = bytearray(self.program)
        start = self.extent["segment"] * 16 + 0x7B9
        program[start:start + 2] = b"\xff\xff"
        with self.assertRaisesRegex(ValueError, "owned instruction entry"):
            verify_native_coverage(self.unit["functions"], self.extent, bytes(program))

    def test_alignment_byte_must_match_the_native_zero(self):
        program = bytearray(self.program)
        program[self.extent["segment"] * 16 + 0x7B8] = 0x90
        with self.assertRaisesRegex(ValueError, "compiler alignment"):
            verify_native_coverage(self.unit["functions"], self.extent, bytes(program))

    def test_missing_compiler_range_is_not_function_coverage(self):
        extent = copy.deepcopy(self.extent)
        extent["producer_ranges"].pop(0)
        with self.assertRaisesRegex(ValueError, "gap or overlap"):
            verify_native_coverage(self.unit["functions"], extent, self.program)

    def test_palette_instruction_coverage_keeps_even_bytes_separate(self):
        config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
        unit = next(u for u in config["native_units"] if u["id"] == "th03-main-stage-palette")
        extent = unit["code_extents"][0]
        data = verify_native_coverage(unit["functions"], extent, self.program)
        self.assertEqual(sum(f["size"] for f in unit["functions"]), 128)
        self.assertEqual([(d["kind"], d["size"]) for d in data],
                         [("tasm-code-even", 1), ("tasm-code-even", 1)])
        for d in data:
            changed = bytearray(self.program)
            changed[extent["segment"] * 16 + d["offset"]] = 0
            with self.assertRaisesRegex(ValueError, "native CODE alignment"):
                verify_native_coverage(unit["functions"], extent, bytes(changed))


class MaintainedSourceDrift(unittest.TestCase):
    def test_old_staged_header_cannot_replace_a_deleted_maintained_header(self):
        with TemporaryDirectory() as folder:
            with patch("review_th03_main_native_units.ROOT", Path(folder)):
                with self.assertRaisesRegex(ValueError, "maintained source missing"):
                    verify_maintained_sources({"src/main/player/lose.hpp": "0" * 64})

    def test_old_staged_tree_cannot_accept_a_modified_maintained_source(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "src/main/player/lose.cpp"
            source.parent.mkdir(parents=True)
            old = b"void lose() { timer--; }\n"
            source.write_bytes(b"void lose() { timer++; }\n")
            staged = {"src/main/player/lose.cpp": hashlib.sha256(old).hexdigest()}
            with patch("review_th03_main_native_units.ROOT", root):
                with self.assertRaisesRegex(ValueError, "maintained source drift"):
                    verify_maintained_sources(staged)


class SharedNativeProducer(unittest.TestCase):
    def setUp(self):
        self.config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
        self.peers = [u for u in self.config["native_units"] if u["object"] == "entry"]

    def test_four_reviewed_owners_cover_one_complete_producer(self):
        result = producer_ownership(self.peers[0], self.peers, [])
        self.assertEqual((result["extent"]["start"], result["extent"]["size"]), (6, 3050))
        self.assertEqual([f["offset"] for f in result["functions"]],
                         [6, 152, 1014, 1071, 1076, 2015, 2879, 2985])
        self.assertEqual(result["owners"], ["th03-main-core-entry", "th03-main-round-loop",
                                             "th03-main-stage-round", "th03-main-round-finish"])

    def test_missing_or_double_owned_byte_is_rejected(self):
        for delta in (-1, 1):
            peers = copy.deepcopy(self.peers)
            peers[1]["code_extents"][0]["start"] += delta
            with self.assertRaisesRegex(ValueError, "gap or overlap"):
                producer_ownership(peers[0], peers, [])

    def test_shared_object_cannot_hide_a_different_frame(self):
        peers = copy.deepcopy(self.peers)
        peers[1]["code_extents"][0]["map_group"] = "WRONG_FRAME"
        with self.assertRaisesRegex(ValueError, "frames differ"):
            producer_ownership(peers[0], peers, [])


@unittest.skipUnless(
    (ROOT / ".analysis/work/main-build.json").is_file(),
    "current native cold report absent",
)
class NativeUnitReview(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / ".analysis/work/main-build.json").read_text())
        if not self.report.get("cold_reproducibility", {}).get("complete"):
            self.skipTest("two current cold source builds are unavailable")

    def test_mixed_build_cannot_borrow_a_passing_cold_pair(self):
        bad = copy.deepcopy(self.report)
        bad["cold_build"] = False
        with self.assertRaisesRegex(ValueError, "two cold source materializations"):
            review(bad)

    def test_true_summary_cannot_hide_a_missing_output(self):
        bad = copy.deepcopy(self.report)
        bad["cold_reproducibility"]["raw_output_repeat"].pop("obj/th03/ex_ellen.obj")
        self.assertTrue(bad["cold_reproducibility"]["complete"])
        with self.assertRaisesRegex(ValueError, "complete cold output vector"):
            review(bad)


if __name__ == "__main__":
    unittest.main()
