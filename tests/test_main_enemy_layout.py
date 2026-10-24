"""Actual native OMF/MAP mutations must not hide lost or extra enemy ownership."""

from pathlib import Path
import re
import shutil
import sys
from tempfile import TemporaryDirectory
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_enemy_layout import OBJECTS, verify
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"


def mutate_record(raw, selected, transform):
    result = bytearray()
    for record in parse_omf(raw):
        data = transform(record.data) if selected(record) else record.data
        prefix = bytes([record.record_type]) + (len(data) + 1).to_bytes(2, "little") + data
        result.extend(prefix + bytes([-sum(prefix) & 255]))
    assert describe_omf(bytes(result))["valid"]
    return bytes(result)


@unittest.skipUnless(all((WORK / f"obj/th03/{n}.obj").is_file() for n in OBJECTS),
                     "current four-object native enemy producer absent")
class EnemyPhysicalLayout(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        (self.work / "obj/th03").mkdir(parents=True)
        for name in [*(n + ".obj" for n in OBJECTS), "main.map"]:
            shutil.copyfile(WORK / "obj/th03" / name, self.work / "obj/th03" / name)
        self.config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())

    def test_all_allocations_and_both_public_tables_are_owned(self):
        result = verify(self.work, self.config)
        self.assertEqual((result["functions"], result["code_bytes"]), (19, 3325))
        self.assertEqual((result["literal_map_parts"], result["literal_public_table_entries"]), (6, 38))

    def test_moved_map_contribution_cannot_borrow_equal_program_bytes(self):
        path = self.work / "obj/th03/main.map"
        text = path.read_text().replace("139D:024E 028A", "139D:024F 028A", 1)
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "literal MAP contribution"):
            verify(self.work, self.config)

    def test_missing_second_public_table_is_rejected(self):
        path = self.work / "obj/th03/main.map"
        text, count = re.subn(r"(?m)^.*enemy_formation_spawn\(int,unsigned char,unsigned char\).*\n",
                              "", path.read_text(), count=1)
        self.assertEqual(count, 1)
        path.write_text(text)
        with self.assertRaisesRegex(ValueError, "both literal MAP public tables"):
            verify(self.work, self.config)

    def test_checksum_valid_private_data_allocation_is_rejected(self):
        path = self.work / "obj/th03/eforna.obj"
        raw = path.read_bytes()
        index, = [s["index"] for s in segment_definitions(raw) if s["name"] == "_DATA"]
        chosen = [r for r in parse_omf(raw) if r.record_type == 0x98][index - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == chosen.offset,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            verify(self.work, self.config)

    def test_checksum_valid_extra_code_is_rejected(self):
        path = self.work / "obj/th03/eforna.obj"
        raw = path.read_bytes()
        index, = [s["index"] for s in segment_definitions(raw) if s["name"] == "ENEMY_2_TEXT"]
        chosen = [r for r in parse_omf(raw) if r.record_type == 0x98][index - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == chosen.offset,
                                      lambda data: data[:1] + b"\x8b\x02" + data[3:]))
        with self.assertRaisesRegex(ValueError, "complete CODE allocation"):
            verify(self.work, self.config)

    def test_map_names_cannot_cover_a_different_omf_public(self):
        path = self.work / "obj/th03/eforna.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90,
                                      lambda data: data.replace(b"@ENEMIES_ADD", b"@ENEMIES_BDD")))
        with self.assertRaisesRegex(ValueError, "complete OMF public ownership"):
            verify(self.work, self.config)
