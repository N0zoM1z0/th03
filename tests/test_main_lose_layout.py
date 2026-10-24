"""The grouped loss producer must own all four entries and every native byte."""
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_lose_layout import verify
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"


@unittest.skipUnless((WORK / "obj/th03/lose.obj").is_file(), "live loss producer absent")
class LoseLayout(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.work = Path(self.folder.name)
        (self.work / "obj/th03").mkdir(parents=True)
        for name in ("main.map", "lose.obj"):
            shutil.copyfile(WORK / "obj/th03" / name, self.work / "obj/th03" / name)
        self.target = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())
        self.candidate = parse_mz((WORK / "bin/th03/main.exe").read_bytes())

    def test_complete_record_four_entries_and_literal_relocations(self):
        result = verify(self.work, self.target, self.candidate)
        self.assertEqual((result["functions"], result["code_bytes"], result["ordered_relocations"]), (4, 664, 10))
        self.assertEqual(result["code_record_sizes"], [664])

    def test_checksum_valid_wrong_member_name_cannot_borrow_the_map(self):
        path = self.work / "obj/th03/lose.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90,
                                      lambda data: data.replace(b"lose_render", b"lose_rendex")))
        with self.assertRaisesRegex(ValueError, "native public set"):
            verify(self.work, self.target, self.candidate)

    def test_checksum_valid_private_data_cannot_hide_in_the_group(self):
        path = self.work / "obj/th03/lose.obj"
        raw = path.read_bytes()
        segment, = [s for s in segment_definitions(raw) if s["name"] == "_DATA"]
        definition = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment["index"] - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == definition.offset,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            verify(self.work, self.target, self.candidate)

    def test_unchanged_loaded_bytes_do_not_hide_literal_relocation_order(self):
        sites = [i for i, r in enumerate(self.candidate.relocations) if 0xC0D8 <= r.linear < 0xC370]
        self.assertEqual(len(sites), 10)
        raw = bytearray(self.candidate.raw)
        a, b = [self.candidate.header.relocation_table_offset + i * 4 for i in sites[:2]]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, "literal relocation pairs"):
            verify(self.work, self.target, changed)
