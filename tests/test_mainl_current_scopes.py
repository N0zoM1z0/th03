"""MAINL lifecycle ownership, Pascal ABI and real instruction mutations."""

from dataclasses import replace
from pathlib import Path
import re
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_th03_mainl_work as build
from lib.mainl_lifecycle_layout import OWNERS, verify
from lib.mainl_lifecycle_runtime import Machine, negative_controls
from lib.pc98 import parse_mz
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ML"


class ConsumedVendorHeaders(unittest.TestCase):
    def test_consumed_prefix_headers_must_match_the_pinned_installation(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "config").mkdir()
            (root / "config/toolchain.toml").write_text(
                '[paths]\nwine_prefix="prefix"\n[[surfaces]]\nid="tc40j-include"\npath="installed"\n')
            consumed = root / "prefix/drive_c/TC4/INCLUDE"
            installed = root / "installed"
            for directory in (consumed, installed):
                directory.mkdir(parents=True)
                for name in build.VENDOR_HEADERS:
                    (directory / name.upper()).write_text("original:" + name)
            with patch.object(build, "ROOT", root):
                self.assertEqual(set(build.vendor_header_inventory()),
                    {"C:/TC4/INCLUDE/" + n for n in ("stddef.h", "_defs.h", "_null.h", "mem.h")})
                for name in ("STDDEF.H", "MEM.H"):
                    original = (consumed / name).read_bytes()
                    (consumed / name).write_text("different consumed declaration")
                    with self.assertRaisesRegex(ValueError, "consumed vendor header differs"):
                        build.vendor_header_inventory()
                    (consumed / name).write_bytes(original)


@unittest.skipUnless((WORK / "bin/th03/mainl.target.exe").is_file(), "private MAINL cold build absent")
class MainlCurrentScopes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = parse_mz((WORK / "bin/th03/mainl.target.exe").read_bytes())
        cls.candidate = parse_mz((WORK / "bin/th03/mainl.exe").read_bytes())

    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.work = Path(folder.name)
        for name in [o[5] for o in OWNERS] + ["obj/th03/mainl.map"]:
            dest = self.work / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(WORK / name, dest)

    def test_complete_native_scope_and_far_argument_width(self):
        owners = verify(self.work, self.target, self.candidate)
        self.assertEqual(sum(o["size"] for o in owners), 210)
        self.assertEqual(sum(len(o["ordered_relocations"]) for o in owners), 19)
        init, = [o for o in owners if o["argument_bytes"]]
        self.assertEqual((init["argument_bytes"], init["callee_pop_bytes"]), (4, 4))
        self.assertTrue(all(o["canonical_file_offset"] is None for o in owners))

    def test_replacing_a_source_dependency_with_context_is_rejected(self):
        path = self.work / "obj/th03/initmain.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: b"src/mainl/linked_game/init.cpp" in r.data,
                                      lambda d: d.replace(b"src/mainl/linked_game/init.cpp", b"src/mainl/linked_game/old_.cpp")))
        with self.assertRaisesRegex(ValueError, "maintained source dependency"):
            verify(self.work, self.target, self.candidate)

    def test_private_storage_cannot_hide_behind_equal_code(self):
        path = self.work / "obj/th03/exit.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.name == "SEGDEF" and r.data[0] == 0x48,
                                      lambda d: d[:1] + b"\x02\0" + d[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            verify(self.work, self.target, self.candidate)

    def test_external_storage_addresses_are_required_in_both_map_tables(self):
        path = self.work / "obj/th03/mainl.map"
        text, count = re.subn(r"(0E3F:)1C60(\s+_VRAM_PLANE_B\b)", r"\g<1>1C62\2", path.read_text())
        self.assertEqual(count, 2)
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "external plane storage"):
            verify(self.work, self.target, self.candidate)

    def test_last_owned_byte_is_compared(self):
        raw = bytearray(self.candidate.program_image)
        raw[0xCF1D] ^= 1
        with self.assertRaisesRegex(ValueError, "complete raw owner"):
            verify(self.work, self.target, replace(self.candidate, program_image=bytes(raw)))

    def test_relocation_order_is_literal_even_with_identical_loaded_bytes(self):
        raw = bytearray(self.candidate.raw)
        indexes = [i for i, r in enumerate(self.candidate.relocations) if 0xCEE0 <= r.linear < 0xCF1E]
        self.assertEqual(len(indexes), 6)
        a, b = [self.candidate.header.relocation_table_offset + i * 4 for i in indexes[:2]]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        candidate = parse_mz(raw)
        self.assertEqual(candidate.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, "literal ordered"):
            verify(self.work, self.target, candidate)

    def test_negative_assign_result_returns_one_without_side_effects(self):
        events, pointers, ax = Machine(self.target, 0x3000).run("init", assign=0x8000, flags=0x602, sp=0xFFF0)
        self.assertEqual((events, pointers, ax), ((("assign", 18000),), b"\xA5" * 16, 1))

    def test_far_filename_is_passed_unchanged_and_library_status_is_ignored(self):
        events, pointers, ax = Machine(self.target, 0x1000).run("init", filename=(0xFFFE, 0xFFFF), library_return=0xFFFF)
        self.assertEqual(events[-1], ("pfstart", 0xFFFE, 0xFFFF))
        self.assertEqual((len(pointers), ax), (16, 0))

    def test_fifteen_actual_guest_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)["count"], 15)
