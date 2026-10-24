"""Native owner, ABI and semantic controls for the current decoded OP scopes."""

from dataclasses import replace
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.op_exit_layout import OWNERS, verify
from lib.op_exit_runtime import Machine, negative_controls
from lib.pc98 import parse_mz
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03OP"


@unittest.skipUnless((WORK / "bin/th03/op.target.exe").is_file(), "private OP cold build absent")
class OpCurrentScopes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = parse_mz((WORK / "bin/th03/op.target.exe").read_bytes())
        cls.candidate = parse_mz((WORK / "bin/th03/op.exe").read_bytes())

    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.work = Path(folder.name)
        for name in [o[4] for o in OWNERS] + ["obj/th03/op.map"]:
            dest = self.work / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(WORK / name, dest)

    def test_complete_native_ownership_and_literal_pairs(self):
        owners = verify(self.work, self.target, self.candidate)
        self.assertEqual(sum(o["size"] for o in owners), 133)
        self.assertEqual(sum(len(o["ordered_relocations"]) for o in owners), 11)
        self.assertTrue(all(o["canonical_file_offset"] is None for o in owners))

    def test_reference_producer_without_actual_maintained_dependency_fails(self):
        path = self.work / OWNERS[1][4]
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: b"src/op/hardware/vram_planes_set.cpp" in r.data,
                                      lambda data: data.replace(b"src/op/hardware/vram_planes_set.cpp", b"src/op/hardware/vram_planes_old.cpp")))
        with self.assertRaisesRegex(ValueError, "maintained source dependency"):
            verify(self.work, self.target, self.candidate)

    def test_implicit_private_storage_cannot_hide_behind_equal_code(self):
        path = self.work / OWNERS[2][4]
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.name == "SEGDEF" and r.data[0] == 0x48,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            verify(self.work, self.target, self.candidate)

    def test_last_owned_byte_is_compared(self):
        raw = bytearray(self.candidate.program_image)
        raw[0xC004] ^= 1
        with self.assertRaisesRegex(ValueError, "full raw owner"):
            verify(self.work, self.target, replace(self.candidate, program_image=bytes(raw)))

    def test_literal_pair_order_cannot_be_replaced_by_relocation_membership(self):
        raw = bytearray(self.candidate.raw)
        indexes = [i for i, r in enumerate(self.candidate.relocations) if 0xBEB8 <= r.linear < 0xBED1]
        a, b = [self.candidate.header.relocation_table_offset + 4 * i for i in indexes[:2]]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, "literal ordered"):
            verify(self.work, self.target, changed)

    def test_graphics_page_outs_and_cleanup_order_are_actual_guest_events(self):
        machine = Machine(self.target, 0x3000)
        events, _ = machine.run("exit_dos", seed=0xFFFF, sp=0xFFF0, flags=0x602)
        self.assertEqual([e for e in events if e[0] == "out"],
                         [("out", 0xA6, 1), ("out", 0xA6, 0), ("out", 0xA6, 0), ("out", 0xA4, 0)])
        self.assertLess(events.index(("vsync_end",)), events.index(("mem_unassign",)))
        self.assertEqual(events[-3:], (("key_beep_on",), ("text_systemline_show",), ("text_cursor_show",)))

    def test_four_far_pointer_stores_cover_the_complete_plane_owner(self):
        machine = Machine(self.target, 0x1000)
        events, pointers = machine.run("planes", seed=0x8000, flags=0x402)
        self.assertEqual(events, ())
        self.assertEqual(pointers.hex(), "000000a8000000b0000000b8000000e0")
        self.assertEqual(len(machine.covered), 41)

    def test_nine_actual_guest_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)["count"], 9)
