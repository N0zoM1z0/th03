"""Current original-ASM init ownership and independent interrupt/memory contracts."""

from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.zun import parse_launcher
from lib.zun_init_layout import verify
from lib.zun_init_runtime import Machine, convert, negative_controls, DATA1, DATA2, REMOTE, ENVIRONMENT

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"


@unittest.skipUnless((WORK / "product/zun.target.com").is_file(), "private current ZUN target absent")
class CurrentInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (WORK / "product/zun.target.com").read_bytes()
        row = parse_launcher(raw, 223)["payloads"][1]
        cls.offset = row["decoded_file_offset"]
        cls.target = raw[cls.offset:cls.offset + row["size"]]
        cls.candidate = (WORK / "init/init.com").read_bytes()

    def machine(self):
        result = Machine(self.target, 0x3000)
        self.addCleanup(result.close)
        return result

    def test_complete_native_fixups_storage_and_original_asm_lineage(self):
        result = verify(WORK, self.target, self.candidate, self.offset)
        self.assertEqual((result["code_bytes"], result["data_bytes"], result["bss_bytes"]), (607, 783, 0))
        self.assertEqual(len(DATA1) + len(DATA2), 783)
        self.assertEqual(len(result["ordered_native_fixups"]), 48)
        self.assertEqual(result["native_records"], [[0x100, 1000], [0x4E8, 390]])
        self.assertEqual(result["source_lineage"]["newly_authored_bytes"], 0)
        self.assertEqual(result["owners"][0]["origin"], "original-asm")
        self.assertIsNone(result["owners"][0]["canonical_file_offset"])

    def test_last_initialized_byte_and_second_map_table_are_required(self):
        raw = bytearray(self.candidate); raw[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "complete unmodified COM"):
            verify(WORK, self.target, bytes(raw), self.offset)
        with TemporaryDirectory() as name:
            work = Path(name); (work / "init").mkdir()
            shutil.copyfile(WORK / "init/init.obj", work / "init/init.obj")
            text = (WORK / "init/init.map").read_bytes()
            (work / "init/init.map").write_bytes(text.rsplit(b"start", 1)[0] + b"other" + text.rsplit(b"start", 1)[1])
            with self.assertRaisesRegex(ValueError, "Name/Value publics"):
                verify(work, self.target, self.candidate, self.offset)

    def test_suppressed_latches_and_complete_iret_flags(self):
        machine = self.machine()
        for kind in ("stop", "copy"):
            for latch in (1, 2, 7, 0x80, 0xFF):
                row = machine.run(kind, latch=latch, flags=0xED7)
                self.assertEqual(row["events"], [])
                self.assertEqual(row["ordered_state_stores"], [])
                self.assertEqual(row["final_latch"], latch)
        row = machine.run("stop", flags=0xED7)
        self.assertEqual([w[2] for w in row["ordered_state_stores"]], [1, 0])

    def test_error_index_word_wrap_and_arbitrary_ds_es(self):
        machine = self.machine()
        for index in range(6):
            a = machine.run("error", error=index, flags=0x646)
            b = machine.run("error", error=index + 0x8000, flags=0x646)
            self.assertEqual(a, b)

    def test_fixed_signature_offset_and_both_signature_words(self):
        machine = self.machine()
        for resident in (1, 2, 3):
            machine.run("detect", resident=resident, vector_offset=0x880, flags=0x646)

    def test_vector_save_restore_order_and_second_free_carry(self):
        machine = self.machine()
        installed = machine.run("start", tail=b" word")
        self.assertEqual(installed["terminal"], ("tsr", 0, 0x42))
        self.assertEqual(len(installed["ordered_state_stores"]), 6)
        for failures in ((ENVIRONMENT,), (REMOTE,), (ENVIRONMENT, REMOTE)):
            row = machine.run("start", tail=b" /r ignored", resident=1, failures=failures)
            self.assertEqual([e[1] for e in row["events"] if e[0] == "set"], [0x59, 6, 5])
            self.assertEqual([e[1] for e in row["events"] if e[0] == "free"], [ENVIRONMENT, REMOTE])
            self.assertEqual(row["terminal"], ("exit", 0))

    def test_inherited_df_odd_word_stores_and_empty_string_wrap(self):
        machine = self.machine()
        for flags in (0x246, 0x646):
            row = machine.run("draw", text=b"", offset=1, flags=flags)
            self.assertEqual(row["video_word_writes"], 65536)
        forward = machine.run("draw", offset=0xFFFF, flags=0x246)
        reverse = machine.run("draw", offset=0xFFFF, flags=0x646)
        self.assertNotEqual(forward["ordered_video_sha256"], reverse["ordered_video_sha256"])

    def test_scalar_conversion_checks_carry_boundaries_as_guest_instructions(self):
        machine = self.machine()
        values = [high * 256 + low for high in (0, 0x7F, 0x80, 0xFF) for low in (0, 0x7F, 0x80, 0x9E, 0x9F, 0xFF)]
        self.assertEqual(machine.conversions(values)["cases"], len(values))
        self.assertTrue(all(convert(v) & ~0x7F7F == 0 for v in values))

    def test_thirteen_actual_guest_mutations_fail_independent_contracts(self):
        controls = negative_controls(self.target)
        self.assertEqual(controls["count"], 13)
        self.assertEqual(len(set(controls["rejected"])), 13)
