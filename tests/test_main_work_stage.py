"""Fresh MAIN staging must work without saved build trees or validation archives."""

from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_th03_main_work as build
from lib.main_work_stage import native_carrier, stage_carriers, generate_sprites


class NativeCarveBoundaries(unittest.TestCase):
    def test_unreviewed_procedure_cannot_disappear_inside_a_carve(self):
        source = (
            "public _main\n_main\t\tproc far\n_main\t\tendp\n"
            "sub_DA43\tproc near\nsub_DA43\tendp\n"
            "unreviewed\tproc near\nunreviewed\tendp\n"
            "player_bomb\tproc near\nplayer_bomb\tendp\n"
        )
        with self.assertRaisesRegex(
            ValueError, "complete native procedure interval differs"
        ):
            native_carrier(source.encode())


@unittest.skipUnless(
    (ROOT / "_reference/ReC98/th03_main.asm").is_file(),
    "pinned reference source unavailable",
)
class CanonicalMainStaging(unittest.TestCase):
    def test_character_setup_cannot_absorb_an_unreviewed_procedure(self):
        for distance in (b"near", b"far"):
            def changed(raw):
                anchor = b"sub_A4A1\tproc near"
                self.assertEqual(raw.count(anchor), 1)
                raw = raw.replace(anchor, anchor + b"\n\t@unreviewed$qv\tproc " + distance + b"\n\t@unreviewed$qv\tendp")
                return native_carrier(raw)

            with self.subTest(distance=distance), TemporaryDirectory() as folder:
                with patch("lib.main_work_stage.native_carrier", side_effect=changed):
                    with self.assertRaisesRegex(ValueError, "complete character setup procedure interval differs"):
                        stage_carriers(Path(folder))
    def test_palette_cannot_absorb_an_unreviewed_procedure(self):
        for distance in (b"near", b"far"):
            def changed(raw):
                anchor = b"sub_A38E\tproc far"
                self.assertEqual(raw.count(anchor), 1)
                raw = raw.replace(anchor, anchor + b"\n\t@unreviewed$qv\tproc " + distance + b"\n\t@unreviewed$qv\tendp")
                return native_carrier(raw)

            with self.subTest(distance=distance), TemporaryDirectory() as folder:
                with patch("lib.main_work_stage.native_carrier", side_effect=changed):
                    with self.assertRaisesRegex(ValueError, "complete palette procedure interval differs"):
                        stage_carriers(Path(folder))

    def test_round_loop_cannot_absorb_an_unreviewed_procedure(self):
        def changed(raw):
            anchor = b"sub_9778\tproc near"
            self.assertEqual(raw.count(anchor), 1)
            raw = raw.replace(anchor, anchor + b"\nunreviewed\tproc near\nunreviewed\tendp")
            return native_carrier(raw)

        with TemporaryDirectory() as folder:
            with patch("lib.main_work_stage.native_carrier", side_effect=changed):
                with self.assertRaisesRegex(ValueError, "round-loop procedure interval differs"):
                    stage_carriers(Path(folder))

    def test_score_alias_keeps_the_real_far_pascal_entry(self):
        with TemporaryDirectory() as folder:
            prepared = stage_carriers(Path(folder))
        text = prepared["src/main/hud/score.asm"].decode()
        alias = "@ROUND_RESULT_HIGH_DIGITS_PUT$QIIUIUC"
        self.assertEqual(text.count("public " + alias), 1)
        self.assertIn(alias + " label far\nscore_bonus_digits_put proc far", text)
        body = text.split("score_bonus_digits_put proc far", 1)[1].split(
            "score_bonus_digits_put endp", 1
        )[0]
        self.assertIn("retf 8", body)

    @unittest.skipUnless(
        shutil.which("cc"), "host bitmap converter compiler unavailable"
    )
    def test_two_empty_directories_materialize_the_same_complete_sources(self):
        results = []
        for _ in range(2):
            with TemporaryDirectory() as folder:
                work = Path(folder)
                prepared = stage_carriers(work)
                generated, metadata = generate_sprites(work)
                prepared.update(generated)
                producers = build.context_producers(
                    build.linked_objects(work / "obj/th03/main.@l")
                )
                hashes = build.stage_sources(producers, prepared, work=work)
                self.assertEqual(len(producers), 86)
                self.assertFalse(list(work.rglob("*.obj")))
                self.assertFalse(list(work.rglob("*.exe")))
                self.assertTrue(
                    {
                        "th03_main.asm",
                        "th03/mst_pref.asm",
                        "th03/mst_body.asm",
                        "src/main/hud/score.asm",
                        "obj/th03/main.@l",
                        "th03/sprites/score.bmp",
                        "th03/sprites/score.asp",
                        "th03/sprites/pellet.bmp",
                        "th03/sprites/pellet.asp",
                    }
                    <= hashes.keys()
                )
                for producer in producers:
                    if producer["staged"].endswith(".cpp"):
                        text = (work / producer["staged"]).read_text(encoding="latin1")
                        self.assertNotRegex(text, r'#include\s+"[^"\n]+\.cpp"')
                self.assertEqual(len(metadata["conversions"]), 2)
                results.append(hashes)
        self.assertEqual(*results)


if __name__ == "__main__":
    unittest.main()
