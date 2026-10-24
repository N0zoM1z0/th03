"""Native combo partitions cannot borrow missing bytes or altered group metadata."""
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_combo_layout import verify
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"


@unittest.skipUnless((WORK / "obj/th03/p_cmbhl.obj").is_file(), "live split combo producer absent")
class ComboLayout(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.work = Path(self.folder.name)
        (self.work / "obj/th03").mkdir(parents=True)
        for name in ("main.map", "p_combo.obj", "p_cmbhl.obj"):
            shutil.copyfile(WORK / "obj/th03" / name, self.work / "obj/th03" / name)
        self.cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
        self.target = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())
        self.candidate = parse_mz((WORK / "bin/th03/main.exe").read_bytes())

    def run_layout(self, candidate=None):
        return verify(self.work, self.cfg, self.target, self.candidate if candidate is None else candidate)

    def test_complete_five_function_partition_preserves_existing_credit(self):
        result = self.run_layout()
        self.assertEqual((result["functions"], result["code_bytes"], result["ordered_relocations"]), (5, 978, 9))
        self.assertEqual(result["code_record_sizes"], [491, 40, 103, 344])
        self.assertEqual(result["new_source_exact_credit"], 0)

    def test_zero_length_default_segment_identity_is_part_of_layout(self):
        path = self.work / "obj/th03/p_cmbhl.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.name == "LNAMES",
                                      lambda data: data.replace(b"P_COMBO_TEXT", b"P_XOMBO_TEXT")))
        with self.assertRaisesRegex(ValueError, "default CODE identity"):
            self.run_layout()

    def test_checksum_valid_wrong_helper_public_is_rejected(self):
        path = self.work / "obj/th03/p_cmbhl.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: r.record_type == 0x90,
                                      lambda data: data.replace(b"COMBO_ADD", b"COMBO_ADX")))
        with self.assertRaisesRegex(ValueError, "OMF public ownership"):
            self.run_layout()

    def test_checksum_valid_private_storage_is_rejected(self):
        path = self.work / "obj/th03/p_cmbhl.obj"
        raw = path.read_bytes()
        segment, = [s for s in segment_definitions(raw) if s["name"] == "_DATA"]
        record = [r for r in parse_omf(raw) if r.name == "SEGDEF"][segment["index"] - 1]
        path.write_bytes(mutate_record(raw, lambda r: r.offset == record.offset,
                                      lambda data: data[:1] + b"\x02\0" + data[3:]))
        with self.assertRaisesRegex(ValueError, "private DATA/BSS"):
            self.run_layout()

    def test_every_helper_byte_is_owned(self):
        raw = bytearray(self.candidate.raw)
        raw[self.candidate.header.header_size + 0x139D0 + 0x2D3D - 1] ^= 1
        with self.assertRaisesRegex(ValueError, "complete linked CODE"):
            self.run_layout(parse_mz(raw))

    def test_unchanged_loaded_bytes_do_not_hide_literal_relocation_order(self):
        sites = [i for i, r in enumerate(self.candidate.relocations) if 0x15CB9 <= r.linear < 0x15EA4]
        self.assertEqual(len(sites), 9)
        raw = bytearray(self.candidate.raw)
        a, b = [self.candidate.header.relocation_table_offset + i * 4 for i in sites[:2]]
        raw[a:a + 4], raw[b:b + 4] = raw[b:b + 4], raw[a:a + 4]
        changed = parse_mz(raw)
        self.assertEqual(changed.program_image, self.candidate.program_image)
        with self.assertRaisesRegex(ValueError, "literal relocation pairs"):
            self.run_layout(changed)
