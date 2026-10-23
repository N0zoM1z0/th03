"""Entry transfer rejection controls and checks against the optional local target."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stage_th03_main_entry as stage
from lib.pc98 import parse_mz
from lib.main_entry_runtime import execute
from review_th03_main_entry import negative_controls


def fixture():
    text = "public _main\r\n_main\t\tproc far\r\n retf\r\n_main\t\tendp\r\n"
    for old, (_, kind) in stage.ALIASES.items():
        text += old + (
            " proc far\r\n retf 4\r\n" + old + " endp\r\n"
            if kind == "far"
            else " proc near\r\n ret\r\n" + old + " endp\r\n"
            if kind == "near"
            else " db 0\r\n"
            if kind == "byte"
            else " dd ?\r\n"
        )
    return text.encode("latin1")


class EntryStagingTests(unittest.TestCase):
    def test_alias_collision_rejected(self):
        with self.assertRaisesRegex(ValueError, "alias collision"):
            stage.transform_root(fixture() + b"_main_op_name label byte\r\n")

    def test_partial_or_duplicate_entry_rejected(self):
        raw = fixture()
        for bad in (
            raw.replace(b"proc far", b"proc near", 1),
            raw + raw,
            raw.replace(b"_main\t\tendp", b"_main_missing endp"),
        ):
            with self.assertRaises(ValueError):
                stage.transform_root(bad)

    def test_existing_allocation_statements_preserved(self):
        raw = fixture()
        changed = stage.transform_root(raw)
        import re

        def allocation(text):
            return re.findall(rb"^\S+ (?:db|dd) [^\r\n]+", text, re.M)

        self.assertEqual(allocation(raw), allocation(changed))
        self.assertNotIn(b"_main\t\tproc far", changed)
        self.assertIn(b"MAIN_EXEC label far", changed)

    def test_response_requires_one_original_and_fresh_entry(self):
        raw = b"crt.obj obj\\th03\\main.obj end.obj"
        self.assertEqual(
            stage.transform_response(raw),
            b"crt.obj obj\\th03\\entry.obj obj\\th03\\main.obj end.obj",
        )
        for bad in (b"crt.obj", raw + raw, raw + b" obj\\th03\\entry.obj"):
            with self.assertRaises(ValueError):
                stage.transform_response(bad)


@unittest.skipUnless(
    (ROOT / ".analysis/targets/th03/main.exe").exists(),
    "private MAIN target unavailable",
)
class EntryTargetTests(unittest.TestCase):
    def setUp(self):
        self.image = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())

    def test_missing_resident_and_restart_then_ending(self):
        for scenario in (
            dict(resident=False, bgm=0, story=0, outcomes=[]),
            dict(resident=True, bgm=1, story=255, outcomes=[1, 1, 2]),
        ):
            execute(self.image, scenario)

    def test_semantic_mutations_rejected(self):
        self.assertEqual(len(negative_controls(self.image)), 5)


if __name__ == "__main__":
    unittest.main()
