"""Source-only staging contracts; no target, private reference, or native tool needed."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("mainl_heap_stage", ROOT / "scripts/stage_th03_mainl_heap.py")
stage = module_from_spec(SPEC)
SPEC.loader.exec_module(stage)
SOURCE = (ROOT / stage.SOURCE_PATH).read_bytes()


def fixture(newline=b"\n"):
    # Deliberately non-UTF-8 outside bytes ensure no text decoding or normalization.
    return (b"; outside \x81\xff" + newline
            + b"include libs/master.lib/palette_white_out.asm" + newline
            + b"".join(b"include " + name.encode("ascii") + newline
                       for name in stage.PROVIDERS)
            + b"include libs/master.lib/super_free.asm" + newline
            + b"; untouched suffix \x82" + newline)


class MainlHeapStagingTests(unittest.TestCase):
    def test_source_identity_and_complete_public_contract(self):
        self.assertEqual(stage.sha256(SOURCE),
                         "3960b8f2ff1821475f86d947b82380957a35ce4c7169a518689e857560774432")
        self.assertEqual(stage.SOURCE_SHA256, stage.sha256(SOURCE))
        # Inspect the saved production pin independently of the synthetic fixture.
        self.assertEqual(self.production_root_sha,
                         "d0c9d5b9576c9e1300d48a22449fb6acbc35c796e1071e21a2f5cf330d659713")
        names = [row.split()[1] for row in SOURCE.decode().splitlines()
                 if row.startswith("PUBLIC ")]
        self.assertEqual(names, ["HMEM_LALLOCATE", "MEM_ASSIGN_DOS", "MEM_ASSIGN",
                                "MEM_ASSIGN_ALL", "HMEM_ALLOCBYTE", "HMEM_ALLOC",
                                "HMEM_FREE", "MEM_UNASSIGN"])
        self.assertEqual(SOURCE.count(b" PROC FAR\n"), 8)
        self.assertEqual(SOURCE.count(b" ENDP\n"), 8)

    def test_exact_slot_and_outside_bytes_for_both_newlines(self):
        for newline in (b"\n", b"\r\n"):
            with self.subTest(newline=newline):
                root = fixture(newline)
                actual = stage.replace_slot(root)
                old = b"".join(b"include " + n.encode() + newline
                               for n in stage.PROVIDERS)
                new = b"include " + stage.SOURCE_PATH.encode() + newline
                self.assertEqual(actual, root.replace(old, new, 1))
                self.assertEqual(actual.replace(new, old, 1), root)

    def test_full_root_pin_rejects_outside_mutation(self):
        root = fixture()
        self.assertEqual(stage.stage_root(root, SOURCE), stage.replace_slot(root))
        with self.assertRaisesRegex(ValueError, "root SHA-256"):
            stage.stage_root(root + b"; drift\n", SOURCE)

    def test_source_pin_rejects_each_semantic_and_comment_mutation(self):
        root = fixture()
        mutations = [
            (b"MAINL_HEAP_ARG0 EQU 6", b"MAINL_HEAP_ARG0 EQU 4"),
            (b"jmp\tshort hmem_allocb", b"jmp\tshort RETURN"),
            (b"jb\tshort NO_THANKYOU", b"jb\tshort FREE_RETURN"),
            (b"retf\t4", b"retf\t2"),
            (b"@@FAILURE:\nxor\tAX,AX\nstc\nretf", b"@@FAILURE:\nretf"),
            (b"nextseg\tdw\t?", b"nextseg\tdd\t?"),
            (b"; MAINL heap manager", b"; Changed heap manager"),
        ]
        for old, new in mutations:
            with self.subTest(old=old):
                self.assertIn(old, SOURCE)
                with self.assertRaisesRegex(ValueError, "source SHA-256"):
                    stage.stage_root(root, SOURCE.replace(old, new, 1))
        for extra in (b"include libs/master.lib/func.inc\n", b"mem_TopSeg dw 0\n"):
            with self.assertRaisesRegex(ValueError, "source SHA-256"):
                stage.stage_root(root, SOURCE + extra)

    def test_missing_duplicate_reordered_or_interrupted_slot_rejected(self):
        root = fixture()
        first = b"include " + stage.PROVIDERS[0].encode() + b"\n"
        second = b"include " + stage.PROVIDERS[1].encode() + b"\n"
        cases = [root.replace(first, b""), root + first,
                 root.replace(first + second, second + first),
                 root.replace(first + second, first + b"; gap\n" + second),
                 root.replace(b"palette_white_out.asm", b"palette_white_in.asm"),
                 root.replace(b"super_free.asm", b"super_entry.asm"),
                 root + b"include " + stage.SOURCE_PATH.encode() + b"\n"]
        for data in cases:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    stage.replace_slot(data)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source_path = self.root / stage.SOURCE_PATH
        source_path.parent.mkdir(parents=True)
        source_path.write_bytes(SOURCE)
        self.frozen = self.root / "frozen.asm"
        self.frozen.write_bytes(fixture())
        self.root_patch = patch.object(stage, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.production_root_sha = stage.ROOT_SHA256
        self.hash_patch = patch.object(stage, "ROOT_SHA256", stage.sha256(fixture()))
        self.hash_patch.start()
        self.addCleanup(self.hash_patch.stop)

    def test_new_stage_emits_only_pair_and_nonacceptance_report(self):
        report = stage.stage_files(self.frozen, ".analysis/new")
        output = self.root / ".analysis/new"
        self.assertEqual(sorted(p.relative_to(output).as_posix()
                                for p in output.rglob("*") if p.is_file()),
                         ["src/mainl/memory/heap.inl", "staging.json", "th03_mainl.asm"])
        self.assertEqual((output / stage.SOURCE_PATH).read_bytes(), SOURCE)
        self.assertEqual((output / "th03_mainl.asm").read_bytes(),
                         stage.replace_slot(fixture()))
        self.assertEqual(report["native_invocations"], 0)
        for key in ("cold", "default_graph_modified", "exact_acceptance"):
            self.assertIs(report[key], False)
        self.assertEqual(self.frozen.read_bytes(), fixture())

    def test_existing_output_never_overwritten(self):
        stage.stage_files(self.frozen, ".analysis/new")
        output = self.root / ".analysis/new/th03_mainl.asm"
        output.write_bytes(b"preserve failed or historical output")
        with self.assertRaises(FileExistsError):
            stage.stage_files(self.frozen, ".analysis/new")
        self.assertEqual(output.read_bytes(), b"preserve failed or historical output")

    def test_unsafe_output_paths_rejected_before_writes(self):
        for path in ("/tmp/stage", "../stage", ".analysis/../stage",
                     ".analysis/a/b", ".analysis", ".analysis/.",
                     ".analysis//new", ".analysis/new/", ".analysis/new name"):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, "fresh .analysis/NAME"):
                    stage.stage_files(self.frozen, path)
        self.assertFalse((self.root / ".analysis").exists())

    def test_analysis_symlink_rejected(self):
        real = self.root / "elsewhere"
        real.mkdir()
        (self.root / ".analysis").symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "real directory"):
            stage.stage_files(self.frozen, ".analysis/new")
        self.assertEqual(list(real.iterdir()), [])

    def test_input_file_and_parent_symlinks_rejected(self):
        alias = self.root / "alias.asm"
        alias.symlink_to(self.frozen)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            stage.stage_files(alias, ".analysis/new")
        directory_alias = self.root / "alias"
        directory_alias.symlink_to(self.root / "src", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            stage.read_regular(directory_alias / "mainl/memory/heap.inl")
        self.assertFalse((self.root / ".analysis").exists())

    def test_source_symlink_rejected_and_failed_identity_writes_nothing(self):
        source_path = self.root / stage.SOURCE_PATH
        source_path.unlink()
        source_path.symlink_to(self.frozen)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            stage.stage_files(self.frozen, ".analysis/new")
        source_path.unlink()
        source_path.write_bytes(SOURCE + b"; drift\n")
        with self.assertRaisesRegex(ValueError, "source SHA-256"):
            stage.stage_files(self.frozen, ".analysis/new")
        self.assertFalse((self.root / ".analysis").exists())

    def test_existing_output_symlink_never_followed(self):
        analysis = self.root / ".analysis"
        analysis.mkdir()
        (analysis / "new").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(FileExistsError):
            stage.stage_files(self.frozen, ".analysis/new")
        self.assertFalse((self.root / "th03_mainl.asm").exists())


if __name__ == "__main__":
    unittest.main()
