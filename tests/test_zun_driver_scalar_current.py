"""Current bounded library services, native ownership and real guest mutants."""

from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.zun import parse_launcher
from lib.zun_driver_scalar_layout import verify, native_image
from lib.zun_driver_scalar_runtime import Machine, ENTRIES, FIELDS, negative_controls
from lib.zun_work_source import compose
from test_main_enemy_layout import mutate_record

WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"


@unittest.skipUnless((WORK / "product/zun.target.com").is_file(), "private current ZUN target absent")
class CurrentDriverScalar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (WORK / "product/zun.target.com").read_bytes()
        row = parse_launcher(raw, 223)["payloads"][3]
        cls.offset = row["decoded_file_offset"]
        cls.target = raw[cls.offset:cls.offset + row["size"]]
        cls.candidate = (WORK / "driver/driver.com").read_bytes()
        cls.files, cls.maintained, _ = compose(ROOT)

    def machine(self):
        machine = Machine(self.target, 0x3000)
        self.addCleanup(machine.close)
        return machine

    def test_exact_include_owners_and_native_fixups_do_not_own_driver_gaps(self):
        result = verify(WORK, self.target, self.candidate, self.offset, self.files, self.maintained)
        self.assertEqual((result["functions"], result["code_bytes"]), (16, 428))
        self.assertEqual((result["private_data_bytes"], result["private_bss_bytes"]), (0, 0))
        self.assertEqual(len(result["ordered_native_fixups"]), 152)
        self.assertEqual(sum(len(o["ordered_native_fixups"]) for o in result["owners"]), 8)
        self.assertFalse(result["enclosing_driver_accepted"])
        self.assertFalse(result["reserved_spans_owned"])
        self.assertEqual({o["origin"] for o in result["owners"]}, {"library"})
        self.assertTrue(all(o["canonical_file_offset"] is None and not o["ordered_relocations"] for o in result["owners"]))

    def test_wrong_actual_include_cannot_inherit_source_owner(self):
        with TemporaryDirectory() as name:
            work = Path(name)
            shutil.copytree(WORK / "driver", work / "driver")
            path = work / "driver/procs/p008.inc"
            path.write_bytes(path.read_bytes().replace(b", dx", b", ax"))
            with self.assertRaisesRegex(ValueError, "consumed bounded include"):
                verify(work, self.target, self.candidate, self.offset, self.files, self.maintained)

    def test_native_module_identity_cannot_borrow_other_producer(self):
        raw = (WORK / "driver/driver.obj").read_bytes()
        # Rewrite the first record's source name with a checksum-correct record.
        changed = mutate_record(raw, lambda r: r.name == "THEADR", lambda d: d.replace(b"driver.asm", b"copied.asm"))
        with self.assertRaisesRegex(ValueError, "native module and COM entry"): native_image(changed)

    def test_equal_com_bytes_cannot_hide_a_moved_native_fixup(self):
        with TemporaryDirectory() as name:
            work = Path(name); shutil.copytree(WORK / "driver", work / "driver")
            path = work / "driver/driver.obj"
            # Shift the state operand's fixup by one byte. Zero CODE/DGROUP
            # bases keep every linked byte equal; literal fixup sites must fail.
            old, new = bytes.fromhex("c6435401"), bytes.fromhex("c6445401")
            changed = mutate_record(path.read_bytes(), lambda r: r.name == "FIXUPP" and old in r.data,
                                    lambda d: d.replace(old, new, 1))
            self.assertEqual(native_image(changed)[0], self.candidate)
            path.write_bytes(changed)
            with self.assertRaisesRegex(ValueError, "eight literal ordered"):
                verify(work, self.target, self.candidate, self.offset, self.files, self.maintained)

    def test_setters_preserve_all_flags_and_use_cs_with_a_foreign_data_segment(self):
        machine = self.machine()
        for kind in FIELDS:
            row = machine.run(kind, value=0xFF80, flags=0xED7, split_stack=True)
            self.assertEqual(row["ordered_writes"], [(0x30000 + FIELDS[kind], 2, 0xFF80)])
            self.assertEqual(row["result_flags"], 0xED7)

    def test_empty_number_suffix_reads_and_restores_the_preceding_byte(self):
        machine = self.machine()
        for before in (ord("H"), ord("h"), ord("B"), ord("b")):
            row = machine.run("parse_number", text=b"", before=before)
            self.assertEqual((row["ax"], row["result_flags"]), (0, 0))
            self.assertEqual([w[2] for w in row["ordered_writes"]], [0, before])

    def test_numeric_wrap_partial_failures_and_quoted_word_order(self):
        machine = self.machine()
        cases = (("parse_number", b"65536", 0, 0), ("parse_decimal", b"-12x", 12, 1),
                 ("parse_number", b"-12x", 0, 1), ("parse_number", b"'AB'", 0x4142, 0),
                 ("parse_number", b"'A'x", 0, 1), ("parse_binary", b"101x", 5, 1))
        for kind, text, ax, cf in cases:
            row = machine.run(kind, text=text)
            self.assertEqual((row["ax"], row["result_flags"]), (ax, cf))

    def test_original_hex_punctuation_and_ascii_fold_flags(self):
        machine = self.machine()
        for text, value in ((b":", 3), (b"@", 9), (b"[", 4), (b"`", 9)):
            row = machine.run("parse_hex", text=text)
            self.assertEqual((row["ax"], row["result_flags"]), (value, 0))
        for value in range(256):
            machine.run("is_decimal_digit", value=value, flags=0xED7)
            machine.run("ascii_upper", value=value, flags=0xED7)

    def test_case_comparison_ignores_df_and_supports_aliased_far_segments(self):
        machine = self.machine()
        for alias in (False, True):
            row = machine.run("string_equal_folded", text=b"aBc", other=b"ABC", flags=0xED7, alias=alias, split_stack=True)
            self.assertEqual(row["result_flags"] & 0x41, 0x40)
        for kind in ("string_length", "parse_hex", "parse_binary"):
            with self.assertRaisesRegex(ValueError, "forward LODSB precondition"): machine.run(kind, flags=0x646)

    def test_fourteen_actual_guest_mutations_fail_independent_contracts(self):
        controls = negative_controls(self.target)
        self.assertEqual(controls["count"], 14)
        self.assertEqual(len(set(controls["rejected"])), 14)
