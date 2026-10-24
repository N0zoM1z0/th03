"""Syntax transport and OMF ABI controls for the exact driver candidate."""

from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import stage_th03_zun_driver as base
import stage_th03_zun_driver_jwasm as stage
from lib.zun_driver_layout import object_layout, public_contract


def rec(kind, data):
    raw = bytes([kind]) + struct.pack("<H", len(data) + 1) + data
    return raw + bytes([-sum(raw) & 255])


def pascal(value):
    raw = value.encode()
    return bytes([len(raw)]) + raw


def fixture(*, swapped_indices=False, alignment=0x48, reversed_group=False, moved_public=False):
    names = ["", "CODE", "_TEXT", "DATA", "_DATA", "DGROUP"]
    if swapped_indices:
        names = ["", "_TEXT", "CODE", "_DATA", "DATA", "DGROUP"]
    idx = lambda n: names.index(n) + 1
    segment = lambda n, cls, size: rec(0x98, bytes([alignment]) + struct.pack("<H", size)
                                     + bytes([idx(n), idx(cls), 1]))
    public = b"\x01\x01"
    for name, offset in public_contract().items():
        if moved_public and name == "sprite16_draw_clipped":
            offset += 1
        public += pascal(name) + struct.pack("<H", offset) + b"\0"
    return (rec(0x80, pascal("fixture.asm")) + rec(0x96, b"".join(pascal(n) for n in names))
            + segment("_TEXT", "CODE", 0x1180) + segment("_DATA", "DATA", 0)
            + rec(0x9A, bytes([idx("DGROUP")]) + (b"\xff\x02\xff\x01" if reversed_group else b"\xff\x01\xff\x02"))
            + rec(0x90, public) + rec(0x8A, b"\0"))


class DriverTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = {n: (ROOT / n).read_bytes() for n in (base.LAYOUT, base.DATA, base.HARDWARE, *base.MODULES)}
        cls.old = base.prepare(cls.inputs)

    def test_every_procedure_data_and_link_input_is_unchanged(self):
        adapted = stage.adapt(self.old)
        changed = {n for n in adapted if adapted[n] != self.old[n]}
        self.assertEqual(changed, {"driver.asm", "hardware.inc"})
        self.assertEqual(len([n for n in adapted if n.startswith("procs/")]), 55)
        self.assertIn(b".model tiny\r\n.386", adapted["driver.asm"])
        self.assertIn(b"_TEXT segment use16", adapted["driver.asm"])
        self.assertIn(b"org 100h", adapted["driver.asm"])

    def test_model_or_macro_shape_drift_is_rejected(self):
        for name, old, new in (("driver.asm", b".model use16 tiny", b".model small"),
                               ("hardware.inc", b":rest", b":other")):
            files = dict(self.old)
            files[name] = files[name].replace(old, new)
            with self.subTest(name=name), self.assertRaises(ValueError):
                stage.adapt(files)


class DriverOmfTests(unittest.TestCase):
    def test_different_name_indices_preserve_the_same_literal_layout(self):
        first = object_layout(fixture())
        second = object_layout(fixture(swapped_indices=True))
        self.assertEqual(first, second)
        self.assertEqual(len(first["publics"]), 56)

    def test_changed_real_alignment_or_group_order_fails(self):
        for raw in (fixture(alignment=0x68), fixture(reversed_group=True)):
            with self.assertRaises(ValueError):
                object_layout(raw)

    def test_a_shifted_function_entry_fails(self):
        with self.assertRaisesRegex(ValueError, "public ABI drift"):
            object_layout(fixture(moved_public=True))

    def test_code_class_name_is_checked_not_just_its_index(self):
        raw = fixture()
        old = rec(0x96, b"".join(pascal(n) for n in ["", "CODE", "_TEXT", "DATA", "_DATA", "DGROUP"]))
        new = rec(0x96, b"".join(pascal(n) for n in ["", "WRONG", "_TEXT", "DATA", "_DATA", "DGROUP"]))
        with self.assertRaisesRegex(ValueError, "segment layout drift"):
            object_layout(raw.replace(old, new))


if __name__ == "__main__":
    unittest.main()
