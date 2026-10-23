"""Read-only source-contract checks. These never invoke an assembler."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/toolchain/wineprefix/drive_c/MPC01/R1/th03_mainl.asm').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import hashlib
import json
from pathlib import Path
import re
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib import mainl_staff_source as staff


def checked(root, path, expected):
    raw = (root / path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("source identity differs: " + path)
    return raw


class StaffSourceTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads((ROOT / "config/th03_mainl_staff_source.json").read_text())
        c = self.config
        g = json.loads(checked(ROOT, c["graphics_recipe"], c["graphics_recipe_sha256"]))
        self.original = checked(ROOT, c["original_root"], c["original_root_sha256"])
        self.previous = checked(ROOT, c["previous_generated_root"], c["previous_generated_root_sha256"])
        self.graphics = checked(ROOT, g["source"], g["source_sha256"])
        checked(ROOT, c["composer"], c["composer_sha256"])
        self.fragments = {n: checked(ROOT, r["path"], r["sha256"]) for n, r in c["fragments"].items()}

    def test_all_source_tokens_and_complete_procedures(self):
        for n, (segment, path, size) in staff.FRAGMENTS.items():
            original = staff.fragment_body(self.previous.replace(b"\r\n", b"\n"), segment)
            self.assertEqual(staff.statements(original), staff.statements(self.fragments[n]))
            count = len(re.findall(rb"(?m)^\S+\s+proc near", self.fragments[n]))
            self.assertEqual(count, self.config["fragments"][n]["complete_procedures"])
            self.assertEqual(len(re.findall(rb"(?m)^\S+\s+endp", self.fragments[n])), count)

    def test_composition_is_only_two_source_includes(self):
        result = staff.generate(self.original, self.graphics, self.fragments)
        expanded = result["th03_mainl.asm"]
        for n, (_, path, _) in staff.FRAGMENTS.items():
            marker = ("include " + path + "\r\n").encode()
            self.assertEqual(expanded.count(marker), 1)
            self.assertEqual(result[path], self.fragments[n].replace(b"\n", b"\r\n"))
            expanded = expanded.replace(marker, result[path])
        self.assertEqual(staff.statements(expanded), staff.statements(self.previous))
        self.assertEqual(self.config["new_symbolic_bytes"] + self.config["previous_graphics_bytes"], 3339)
        self.assertFalse(self.config["native_fragment_consumption_proven"])

    def test_changed_instruction_rejected(self):
        fragments = dict(self.fragments)
        fragments["snow"] = fragments["snow"].replace(b"xor\tax, ax", b"sub\tax, ax", 1)
        with self.assertRaisesRegex(ValueError, "tokens differ"):
            staff.generate(self.original, self.graphics, fragments)

    def test_removed_branch_rejected(self):
        fragments = dict(self.fragments)
        fragments["staff"] = fragments["staff"].replace(b"\t\tjg\tloc_BEC1", b"; removed branch", 1)
        with self.assertRaisesRegex(ValueError, "tokens differ"):
            staff.generate(self.original, self.graphics, fragments)

    def test_raw_padding_or_incomplete_partition_rejected(self):
        fragments = dict(self.fragments)
        fragments["snow"] += b"db 90h\n"
        with self.assertRaises(ValueError): staff.generate(self.original, self.graphics, fragments)
        with self.assertRaises(ValueError): staff.generate(self.original, self.graphics, {"snow":self.fragments["snow"]})

    def test_near_abi_and_hazard_tokens_retained(self):
        snow = staff.statements(self.fragments["snow"])
        staff_rows = staff.statements(self.fragments["staff"])
        for row in [(b"push",b"word",b"ptr",b"[bp+@@angle]"), (b"retn",b"4"),
                    (b"cmp",b"word_10BB2,",b"0C0h"), (b"jbe",b"short",b"loc_BCFE")]:
            self.assertIn(row, snow)
        for row in [(b"idiv",b"bx"), (b"retn",b"6"), (b"cmp",b"word_10BB2,",b"100h"),
                    (b"test",b"byte",b"ptr",b"word_10BB2,",b"1")]:
            self.assertIn(row, staff_rows)

    def test_comment_and_quoted_text_handling(self):
        self.assertEqual(staff.statements(b"mov ax, 1 ; hello\n"), staff.statements(b" mov  ax,  1\n"))
        self.assertNotEqual(staff.statements(b'db "a;b"\n'), staff.statements(b'db "a;c"\n'))
        self.assertNotEqual(staff.statements(b"mov ax, 1\nret\n"), staff.statements(b"mov ax, 1 ret\n"))

if __name__ == "__main__": unittest.main()
