"""Current native ownership and independent resident boundary/ABI controls."""

from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.zun import parse_launcher
from lib.zun_resident_layout import verify, DATA, DEFAULTS
from lib.zun_resident_runtime import Machine, negative_controls
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"


@unittest.skipUnless((WORK / "product/zun.target.com").is_file(), "private current ZUN target absent")
class CurrentResident(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        decoded = (WORK / "product/zun.target.com").read_bytes()
        row = parse_launcher(decoded, 223)["payloads"][4]
        cls.offset = row["decoded_file_offset"]
        cls.target = decoded[cls.offset:cls.offset + row["size"]]
        cls.candidate = (WORK / "bin/th03/res_yume.com").read_bytes()

    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.work = Path(folder.name)
        for name in ("obj/th03/res_yume.obj", "obj/th03/res_yume.map"):
            dest = self.work / name; dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(WORK / name, dest)

    def machine(self):
        result = Machine(self.target, 0x3000)
        self.addCleanup(result.close)
        return result

    def test_complete_native_owner_partition_and_namespace(self):
        result = verify(self.work, self.target, self.candidate, self.offset)
        self.assertEqual((result["code_bytes"], result["data_bytes"], result["bss_bytes"]), (322, 307, 0))
        self.assertEqual(result["native_code_records"], [322])
        self.assertEqual(result["map_public_table_entries"], 6)
        self.assertEqual(len(DATA), 307)
        self.assertEqual({o["payload_option"] for o in result["owners"]}, {"-5"})
        self.assertTrue(all(o["canonical_file_offset"] is None and not o["ordered_relocations"]
                            and o["callee_pop_bytes"] == 0 for o in result["owners"]))

    def test_reference_body_cannot_replace_actual_maintained_include(self):
        path = self.work / "obj/th03/res_yume.obj"
        path.write_bytes(mutate_record(path.read_bytes(), lambda r: b"src/zun/cfg_init.inl" in r.data,
                                      lambda d: d.replace(b"src/zun/cfg_init.inl", b"src/zun/old_init.inl")))
        with self.assertRaisesRegex(ValueError, "maintained source dependencies"):
            verify(self.work, self.target, self.candidate, self.offset)

    def test_both_map_public_tables_and_last_data_byte_are_required(self):
        path = self.work / "obj/th03/res_yume.map"
        original = path.read_text()
        path.write_text(original.replace("cfg_init(resident_t _seg *)", "cfg_init(other)", 1))
        with self.assertRaisesRegex(ValueError, "both MAP public tables"):
            verify(self.work, self.target, self.candidate, self.offset)
        path.write_text(original)
        raw = bytearray(self.candidate); raw[0x1350] ^= 1
        with self.assertRaisesRegex(ValueError, "linked DATA"):
            verify(self.work, self.target, bytes(raw), self.offset)

    def test_signed_handles_and_defaults_have_independent_write_snapshots(self):
        m = self.machine()
        for opened in (0, 0x7FFF, 0x8000, 0xFFFF):
            row = m.run("cfg_init", opened=opened, created=0xFFFF, segment=0xBEEF, debug=0xA7)
            writes = [e for e in row["events"] if e[0] == "write"]
            if opened == 0x7FFF:
                self.assertEqual(writes, [("write", opened, "efbe"), ("write", opened, "a7")])
            else:
                self.assertEqual(writes, [("write", 0xFFFF, DEFAULTS.hex()),
                                          ("write", 0xFFFF, "efbe"), ("write", 0xFFFF, "a7")])

    def test_only_argc_two_parses_prefix_and_ignores_argument_tail(self):
        m = self.machine()
        for argc in (0, 1, 3, 0xFFFF):
            self.assertEqual(m.run("main", argc=argc, argument=b"/R")["ax"], 0)
        row = m.run("main", argument=b"-rignored", existing=0x900)
        self.assertIn(("free", 0x900), row["events"])
        self.assertEqual(row["ax"], 0)

    def test_allocation_failure_and_already_present_retain_error_returns(self):
        m = self.machine()
        self.assertEqual(m.run("main", allocated=0)["ax"], 1)
        row = m.run("main", existing=0x900)
        self.assertEqual((row["ax"], row["debug"]), (1, 1))
        self.assertFalse(row["resident_tail_cleared"])

    def test_actual_copy_helper_clears_df_and_main_ignores_io_errors(self):
        m = self.machine()
        for flags in (2, 0x202, 0x402, 0x602):
            row = m.run("main", argc=1, opened=0xFFFF, created=0xFFFF, reply=0x8000, flags=flags)
            self.assertEqual(row["ax"], 0)
            self.assertTrue(row["df_cleared"])
            self.assertTrue(row["resident_tail_cleared"])

    def test_sixteen_actual_guest_mutations_are_rejected(self):
        controls = negative_controls(self.target)
        self.assertEqual(controls["count"], 16)
        self.assertEqual(len(set(controls["rejected"])), 16)
