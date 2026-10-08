"""Negative controls: exact CODE and unchanged FIXUPP descriptors."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from lib.omf import parse_omf
from lib.tc4_omf_bridge import _record, reframe_ellen_tc4_fixupp, validate_ellen_omf_recipe


class EllenOmfBridgeTests(unittest.TestCase):
    def setUp(self):
        first_code = bytearray(b"\x90" * 1024)
        first_code[1000:1005] = b"\x9a\x00\x00\x00\x00"
        second_code = bytes(b"\x90" * 54)
        self.record_bytes = [
            _record(0x80, b"\x04test"),
            _record(0xA0, b"\x04\x00\x00" + first_code),
            _record(0x9C, bytes.fromhex("cf e9 56 15 c4 0d 56 14")),
            _record(0xA0, b"\x04\x00\x04" + second_code),
            _record(0x9C, bytes.fromhex(
                "c4 24 16 01 19 c4 13 16 01 18 c4 0a 16 01 02")),
            _record(0x8A, b"\x00"),
        ]
        self.raw = b"".join(self.record_bytes)

    def test_reframes_only_data_record_boundaries_and_one_10bit_location(self):
        got = parse_omf(reframe_ellen_tc4_fixupp(self.raw))
        self.assertEqual(got[1].data[:3], b"\x04\0\0")
        self.assertEqual(len(got[1].data[3:]), 1000)
        self.assertEqual(got[2].data, bytes.fromhex("c4 0d 56 14"))
        self.assertEqual(got[3].data[:3], b"\x04\xe8\x03")
        self.assertEqual(len(got[3].data[3:]), 78)
        original = parse_omf(self.raw)
        self.assertEqual(got[1].data[3:] + got[3].data[3:],
                         original[1].data[3:] + original[3].data[3:])
        self.assertEqual(got[4].data, bytes.fromhex(
            "cc 01 56 15 c4 3c 16 01 19 c4 2b 16 01 18 c4 22 16 01 02"))
        self.assertEqual((got[0].data, got[-1].data),
                         (original[0].data, original[-1].data))

    def test_rejects_unsupported_code_mutation_and_framing(self):
        for replace in (
            (b"\x9a\0\0\0\0", b"\x90\0\0\0\0"),
            (bytes.fromhex("cf e9 56 15"), bytes.fromhex("c7 e9 56 15")),
            (bytes.fromhex("04 00 04"), bytes.fromhex("04 01 04")),
        ):
            with self.subTest(replace=replace), self.assertRaises(ValueError):
                reframe_ellen_tc4_fixupp(self.raw.replace(*replace, 1))
        with self.assertRaises(ValueError):
            reframe_ellen_tc4_fixupp(reframe_ellen_tc4_fixupp(self.raw))

    def test_only_declared_eIlen_compiler_producer_allowed(self):
        obj = dict(
            object="ex_ellen", object_path="obj/th03/ex_ellen.obj",
            wrapper="th03/ex_ellen.cpp", source="src/main/player/exatt_ellen.cpp",
            translator_comment="TC86 Borland C++ 4.02",
            tc4_omf_reframe="ellen-ledata-1000",
        )
        self.assertEqual(validate_ellen_omf_recipe(obj), obj["wrapper"])
        for changed in (
            {"wrapper": "th03/other.cpp"},
            {"object_path": "obj/th03/other.obj"},
            {"tc4_omf_reframe": "arbitrary-byte-edit"},
            {"source": "../wrong.cpp"},
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                validate_ellen_omf_recipe({**obj, **changed})
