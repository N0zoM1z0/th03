"""Current mixed-link comparisons reject raw and literal relocation regressions."""

from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest
import sys
import tomllib

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
        for u in self.cfg["units"]:
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
            (87, 66843),
        )
        self.assertTrue(all(s["raw_equal"] for s in result["new_scopes"]))
        self.assertFalse(result["new_scopes"][2]["ordered_relocations_equal"])
        self.assertFalse(result["exact_acceptance"])
        self.assertFalse(result["cold_build"])

    def test_all_context_objects_have_maintained_source_producers(self):
        producers = work.context_producers()
        self.assertEqual(len(producers), 80)
        self.assertEqual(len({p["output"] for p in producers}), 80)
        for producer in producers:
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
