"""Native grouping cannot borrow bytes from missing owners or forged metadata."""

from copy import deepcopy
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_reimu_layout import verify
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"


@unittest.skipUnless((WORK / "obj/th03/ex_rfly.obj").is_file(), "live flight/Reimu producer absent")
class ReimuLayout(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.work = Path(self.folder.name)
        (self.work / "obj/th03").mkdir(parents=True)
        for name in ("main.map", "ex_rfly.obj", "ex_reup.obj"):
            shutil.copyfile(WORK / "obj/th03" / name, self.work / "obj/th03" / name)
        self.cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
        self.target = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())
        self.candidate = parse_mz((WORK / "bin/th03/main.exe").read_bytes())

    def run_layout(self, cfg=None, candidate=None):
        return verify(self.work, self.cfg if cfg is None else cfg, self.target,
                      self.candidate if candidate is None else candidate)

    def test_two_records_cover_both_existing_owners_without_new_credit(self):
        result = self.run_layout()
        self.assertEqual((result["functions"], result["code_bytes"], result["ordered_relocations"]), (10, 1156, 18))
        self.assertEqual(result["code_record_sizes"], [825, 331])
        self.assertEqual(result["new_source_exact_credit"], 0)

    def test_checksum_valid_private_storage_is_rejected(self):
        path = self.work / "obj/th03/ex_rfly.obj"
        raw = path.read_bytes()
        segment, = [s for s in segment_definitions(raw) if s["name"] == "_DATA"]
        record = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment["index"] - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == record.offset,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            self.run_layout()

    def test_wrong_public_cannot_borrow_an_unchanged_map(self):
        path = self.work / "obj/th03/ex_rfly.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90,
                                      lambda data: data.replace(b"_exatt_fly_update", b"_exatt_fly_updatf")))
        with self.assertRaisesRegex(ValueError, "OMF public ownership"):
            self.run_layout()

    def test_code_record_offset_cannot_hide_an_uncovered_byte(self):
        path = self.work / "obj/th03/ex_rfly.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.name == "LEDATA",
                                      lambda data: data[:1] + b"\x01\0" + data[3:]))
        with self.assertRaises(ValueError):
            self.run_layout()

    def test_literal_map_module_cannot_substitute_the_old_split(self):
        path = self.work / "obj/th03/main.map"
        path.write_text(path.read_text().replace("th03/ex_rfly.cpp", "th03/ex_repre.cpp"))
        with self.assertRaisesRegex(ValueError, "literal MAP contribution"):
            self.run_layout()

    def test_equal_program_bytes_do_not_hide_relocation_reordering(self):
        sites = [i for i, r in enumerate(self.candidate.relocations) if 0x1A1A7 <= r.linear < 0x1A62B]
        self.assertEqual(len(sites), 18)
        raw = bytearray(self.candidate.raw)
        a, b = [self.candidate.header.relocation_table_offset + i * 4 for i in sites[:2]]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, "literal relocation pairs"):
            self.run_layout(candidate=changed)

    def test_shared_record_cannot_hide_a_missing_semantic_function(self):
        cfg = deepcopy(self.cfg)
        cfg["functions"] = [f for f in cfg["functions"] if f["name"] != "exatt_collmap_set"]
        with self.assertRaisesRegex(ValueError, "function coverage"):
            self.run_layout(cfg=cfg)
