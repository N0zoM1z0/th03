"""Current mixed-link comparisons reject raw and literal relocation regressions."""

from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest
import sys
import tomllib
import csv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_th03_main_work as work
from lib.pc98 import parse_mz
from lib.omf import describe_omf
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes


@unittest.skipUnless(
    (work.WORK / "bin/th03/main.exe").is_file(), "current MAIN work tree unavailable"
)
class MainWorkTests(unittest.TestCase):
    def setUp(self):
        self.raw = (work.WORK / "bin/th03/main.exe").read_bytes()
        self.image = parse_mz(self.raw)
        self.cfg = tomllib.loads(
            (ROOT / "config/th03_main_exact_units.toml").read_text()
        )

    def run_image(self, raw):
        with tempfile.TemporaryDirectory(dir=ROOT / ".analysis/work") as folder:
            root = Path(folder)
            p = root / "bin/th03/main.exe"
            p.parent.mkdir(parents=True)
            p.write_bytes(raw)
            with patch.object(work, "WORK", root):
                return work.review()

    def extents(self):
        for u in self.cfg["units"] + self.cfg.get("native_units", []):
            for e in u.get("code_extents", [u]):
                lo = (
                    e.get("segment", u.get("segment", self.cfg["segment"])) * 16
                    + e["start"]
                )
                yield lo, lo + e["size"]

    def test_current_raw_result_does_not_promote_exact(self):
        result = self.run_image(self.raw)
        self.assertEqual(
            (result["checked_owned_extents"], result["checked_owned_bytes"]),
            (93, 70380),
        )
        self.assertTrue(all(s["raw_equal"] for s in result["new_scopes"]))
        self.assertFalse(result["new_scopes"][2]["ordered_relocations_equal"])
        self.assertFalse(result["exact_acceptance"])
        self.assertFalse(result["cold_build"])

    def test_stage_raw_equality_does_not_hide_wrong_relocation_order(self):
        candidate = self.run_image(self.raw)["stage_round_candidate"]
        self.assertEqual(candidate["bytes"], 1865)
        self.assertTrue(candidate["raw_equal"])
        self.assertFalse(candidate["exact_acceptance"])
        if not candidate["ordered_relocations_equal"]:
            with (ROOT / "config/units.csv").open() as stream:
                row = next(
                    r
                    for r in csv.DictReader(stream)
                    if r["id"] == "th03-main-stage-round"
                )
            self.assertNotEqual(row["state"], "exact")

    def test_stage_initializer_order_is_checked_without_normalizing(self):
        sites = [i for i, r in enumerate(self.image.relocations) if 0x9AD6 <= r.linear < 0xA21F]
        self.assertEqual(len(sites), 27)
        raw = bytearray(self.raw)
        a, b = [self.image.header.relocation_table_offset + i * 4 for i in (sites[0], sites[-1])]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        self.assertEqual(parse_mz(raw).program_image, self.image.program_image)
        with self.assertRaisesRegex(ValueError, "tracked scope regressed"):
            self.run_image(raw)

    def test_real_demo_callbacks_define_the_native_stage_producer(self):
        raw = (work.WORK / "obj/th03/stg_rnd.obj").read_bytes()
        segments = [s for s in segment_definitions(raw) if s["size"]]
        self.assertEqual([(s["name"], s["size"]) for s in segments], [("PLAYFLD_TEXT", 1865)])
        index = segments[0]["index"]
        self.assertEqual([offset for offset, _ in code_publics(raw, index)], [0, 57, 62, 1001])
        self.assertEqual([p["size"] for p in code_bytes(raw, index)[1]], [1021, 844])

    def test_entry_and_loop_have_one_native_record_and_global_prefix(self):
        raw = (work.WORK / "obj/th03/entry.obj").read_bytes()
        segments = [s for s in segment_definitions(raw) if s["size"]]
        self.assertEqual([(s["name"], s["class"], s["size"]) for s in segments],
                         [("PLAYFLD_TEXT", "CODE", 1008)])
        index = segments[0]["index"]
        self.assertEqual(code_publics(raw, index), [(0, "_main"), (146, "_round_loop")])
        self.assertEqual([p["size"] for p in code_bytes(raw, index)[1]], [1008])
        result = self.run_image(self.raw)
        self.assertTrue(result["entry_loop_producer"]["ordered_relocations_equal"])
        self.assertGreaterEqual(result["matching_relocation_prefix"], 27)

    def test_cross_owner_order_cannot_borrow_two_passing_local_vectors(self):
        sites = [i for i, r in enumerate(self.image.relocations) if 0x96E6 <= r.linear < 0x9AD6]
        self.assertEqual(len(sites), 23)
        early = [i for i in sites if self.image.relocations[i].linear < 0x9778]
        late = [i for i in sites if self.image.relocations[i].linear >= 0x9778]
        raw = bytearray(self.raw)
        table = self.image.header.relocation_table_offset
        for destination, source in zip(sites, early + late):
            raw[table + destination * 4:table + destination * 4 + 4] = self.raw[table + source * 4:table + source * 4 + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.image.program_image)
        for lo, hi in ((0x96E6, 0x9778), (0x9778, 0x9AD6)):
            vector = lambda image: [r for r in image.relocations if lo <= r.linear < hi]
            self.assertEqual(vector(changed), vector(self.image))
        with self.assertRaisesRegex(ValueError, "entry/loop producer"):
            self.run_image(raw)

    def test_library_gap_is_owned_by_the_linker(self):
        raw = (work.WORK / "obj/th03/mst_pref.obj").read_bytes()
        self.assertTrue(describe_omf(raw)["valid"])
        segments = [s for s in segment_definitions(raw) if s["size"]]
        self.assertEqual([(s["name"], s["class"], s["size"]) for s in segments],
                         [("_TEXT", "CODE", 2269)])
        publics = dict((name, offset) for offset, name in code_publics(raw, segments[0]["index"]))
        self.assertEqual(publics["cutline"], 1016)
        self.assertEqual(publics["GRCG_CIRCLE"], 1904)
        # The module ends BEFORE this byte. A source-emitted padding byte would
        # increase its SEGDEF size and fail the ownership check above.
        self.assertEqual(0x272 + segments[0]["size"], 0xB4F)
        self.assertEqual(self.image.program_image[0xB4F], 0)
        self.assertEqual(self.run_image(self.raw)["complete_program_differing_bytes"],
                         [0xEC2D, 0x1DB05])

    def test_all_context_objects_have_maintained_source_producers(self):
        producers = work.context_producers()
        self.assertEqual(len(producers), 81)
        self.assertEqual(len({p["output"] for p in producers}), 81)
        for producer in producers:
            if producer.get("origin") == "reference-library-context":
                self.assertEqual(producer["source"], "th03/mst_pref.asm")
                self.assertTrue((ROOT / producer["recipe"]).is_file())
            else:
                self.assertTrue((ROOT / producer["source"]).is_file())
        outputs = {p["output"] for p in producers}
        outputs.update(work.object_path(s) for s in work.SOURCES)
        outputs.update({"obj/th03/main.obj", "obj/th03/score_hud.obj", "c0l.obj"})
        self.assertEqual(outputs, set(work.linked_objects()))

    def test_unknown_cached_object_cannot_escape_source_rebuild(self):
        names = work.linked_objects() + ["obj/th03/unknown.obj"]
        with patch.object(work, "linked_objects", return_value=names):
            with self.assertRaisesRegex(ValueError, "lack a source producer"):
                work.context_producers()

    @unittest.skipUnless(
        (work.WORK / "obj/th03/intro.obj").is_file(), "native HUD object absent"
    )
    def test_hud_is_one_native_compiler_producer(self):
        raw = (work.WORK / "obj/th03/intro.obj").read_bytes()
        metadata = describe_omf(raw)
        self.assertTrue(metadata["valid"])
        self.assertEqual(metadata["translator_comments"], ["TC86 Borland C++ 4.02"])
        segments = [s for s in segment_definitions(raw) if s["size"]]
        self.assertEqual(
            [(s["name"], s["size"]) for s in segments], [("PLAYER_M_TEXT", 1478)]
        )
        segment = segments[0]["index"]
        self.assertEqual(
            code_publics(raw, segment),
            [
                (0, "_hud_start_anim_update"),
                (688, "HUD_START_SPRITE_STRIP_PUT"),
                (792, "HUD_START_PARTICLE_PIXEL_PUT"),
                (843, "_hud_start_anim_render"),
            ],
        )
        self.assertEqual([p["size"] for p in code_bytes(raw, segment)[1]], [1024, 454])

    @unittest.skipUnless(
        (work.WORK / "obj/th03/ex_ellen.obj").is_file(), "native Ellen object absent"
    )
    def test_character_producers_include_ellen_initializer(self):
        for name, size, starts, records in (
            ("ex_chyu", 978, [0, 112, 630, 928], [978]),
            ("ex_ellen", 1129, [0, 51, 237, 340, 609, 1079], [1024, 105]),
        ):
            with self.subTest(producer=name):
                raw = (work.WORK / "obj/th03" / (name + ".obj")).read_bytes()
                self.assertEqual(
                    describe_omf(raw)["translator_comments"], ["TC86 Borland C++ 4.02"]
                )
                segs = [s for s in segment_definitions(raw) if s["size"]]
                self.assertEqual(
                    [(s["name"], s["size"]) for s in segs], [("P_EXATT_TEXT", size)]
                )
                segment = segs[0]["index"]
                self.assertEqual(
                    [offset for offset, _ in code_publics(raw, segment)], starts
                )
                self.assertEqual(
                    [p["size"] for p in code_bytes(raw, segment)[1]], records
                )
                if name == "ex_ellen":
                    self.assertEqual(
                        code_publics(raw, segment)[0][1], "EXATT_ELLEN_SLOTS_INIT"
                    )

    def test_last_owned_byte_mutation_rejected(self):
        lo, hi = next(self.extents())
        raw = bytearray(self.raw)
        raw[self.image.header.header_paragraphs * 16 + hi - 1] ^= 1
        with self.assertRaisesRegex(ValueError, "tracked scope regressed"):
            self.run_image(raw)

    def test_each_native_owner_last_byte_mutation_is_rejected(self):
        for unit in self.cfg["native_units"]:
            with self.subTest(owner=unit["id"]):
                (extent,) = unit["code_extents"]
                end = extent["segment"] * 16 + extent["start"] + extent["size"]
                raw = bytearray(self.raw)
                raw[self.image.header.header_size + end - 1] ^= 1
                with self.assertRaisesRegex(ValueError, "tracked scope regressed"):
                    self.run_image(raw)

    def test_literal_relocation_reorder_rejected(self):
        for lo, hi in self.extents():
            sites = [
                i for i, r in enumerate(self.image.relocations) if lo <= r.linear < hi
            ]
            if len(sites) >= 2:
                break
        else:
            self.fail("no reviewed multi-relocation extent")
        a, b = (self.image.header.relocation_table_offset + i * 4 for i in sites[:2])
        raw = bytearray(self.raw)
        raw[a : a + 4], raw[b : b + 4] = raw[b : b + 4], raw[a : a + 4]
        self.assertEqual(parse_mz(raw).program_image, self.image.program_image)
        with self.assertRaisesRegex(ValueError, "tracked scope regressed"):
            self.run_image(raw)


if __name__ == "__main__":
    unittest.main()
