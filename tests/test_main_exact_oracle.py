"""Negative controls for complete, unnormalized owned-extent comparison."""
import struct
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from test_pc98 import synthetic_mz, synthetic_mz_with_relocations
from replay_th03_main_exact_units import (
    add_candidate_owners, compare_extent, normalized_code_extents, sha, verify_include_carrier,
    verify_disjoint_ownership,
    verify_private_calls,
)
from lib.pc98 import parse_mz


class MainExactManifestTests(unittest.TestCase):
    def test_private_near_entry_requires_complete_owned_public_callers(self):
        private = {"name": "helper", "object": "include", "offset": 0,
                   "private_callers": [{"name": "wrapper", "count": 2}]}
        wrapper = {"name": "wrapper", "object": "include", "offset": 1,
                   "size": 7, "map_public": "WRAPPER"}
        payload = b"\xc3\xe8\xfc\xff\xe8\xf9\xff\xcb"
        self.assertEqual(verify_private_calls(private, [wrapper], payload, 0),
                         [{"caller": "wrapper", "direct_near_call_sites": [1, 4]}])
        for caller in ({**wrapper, "object": "unowned"}, {**wrapper, "map_public": ""},
                       {**wrapper, "size": 6}, {**wrapper, "segment": 1}):
            with self.subTest(caller=caller), self.assertRaises(ValueError):
                verify_private_calls(private, [caller], payload, 0)
        with self.assertRaises(ValueError):
            verify_private_calls(private, [wrapper], b"\xc3\xe8\xfd\xff" + payload[4:], 0)
        with self.assertRaises(ValueError):
            verify_private_calls({**private, "map_public": "FAKE_HELPER"}, [wrapper], payload, 0)

    def test_shared_map_carrier_does_not_allow_duplicate_code_credit(self):
        a = {"segment": 1, "start": 0x20, "size": 4, "map_start": 0, "map_size": 0x100}
        b = {**a, "start": 0x24}
        verify_disjoint_ownership({"a": [a], "b": [b]})
        with self.assertRaisesRegex(ValueError, "overlapping CODE ownership"):
            verify_disjoint_ownership({"a": [a], "b": [{**b, "start": 0x23}]})
        verify_disjoint_ownership({"a": [a], "other_segment": [{**a, "segment": 2}]})

    def test_interior_owner_requires_explicit_contained_include(self):
        unit = {"id": "include", "object": "logical-include", "source": "src/main/unit.inl",
                "start": 0x20, "size": 4, "map_start": 0x10, "map_size": 0x30,
                "ownership": "bounded-include", "carrier_path": "carrier.asm",
                "carrier_sha256": "pinned", "overlay_path": "th03/unit.asm",
                "object_path": "obj/th03/main.obj"}
        extent = normalized_code_extents(unit, 0x1234)[0]
        self.assertEqual((extent["start"], extent["size"]), (0x20, 4))
        self.assertEqual((extent["map_start"], extent["map_size"]), (0x10, 0x30))
        for mutation in ({"map_size": 0x12}, {"map_start": 0x21},
                         {"source": "src/main/unit.asm"}, {"ownership": "translation-unit"},
                         {"carrier_sha256": ""}, {"object_path": ""}):
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                normalized_code_extents({**unit, **mutation}, 0x1234)

    def test_include_carrier_is_frozen_and_contains_one_include(self):
        with TemporaryDirectory() as temporary:
            work = Path(temporary)
            carrier = work / "carrier.asm"
            unit = {"id": "include", "ownership": "bounded-include",
                    "carrier_path": "carrier.asm", "overlay_path": "th03/unit.asm",
                    "map_module": "carrier.asm"}
            carrier.write_bytes(b"; legacy comment \x96\nINCLUDE th03/unit.asm\n")
            unit["carrier_sha256"] = sha(carrier.read_bytes())
            verify_include_carrier(unit, work)
            carrier.write_text("include th03/other.asm\n")
            with self.assertRaisesRegex(ValueError, "drifted"):
                verify_include_carrier(unit, work)
            for text in ("include th03/other.asm\n", "include th03/unit.asm\n" * 2):
                carrier.write_text(text)
                unit["carrier_sha256"] = sha(carrier.read_bytes())
                with self.assertRaisesRegex(ValueError, "occur once"):
                    verify_include_carrier(unit, work)

    def test_nested_include_chain_reaches_the_actual_map_module(self):
        with TemporaryDirectory() as temporary:
            work = Path(temporary)
            (work / "root.asm").write_text("include context.inc\n")
            (work / "context.inc").write_text("include getters.inc\n")
            parent = {"path": "root.asm", "sha256": sha((work / "root.asm").read_bytes())}
            unit = {"id": "getters", "ownership": "bounded-include",
                    "carrier_path": "context.inc", "overlay_path": "getters.inc",
                    "carrier_sha256": sha((work / "context.inc").read_bytes()),
                    "parent_carriers": [parent], "map_module": "root.asm"}
            verify_include_carrier(unit, work)
            with self.assertRaisesRegex(ValueError, "MAP module"):
                verify_include_carrier({**unit, "parent_carriers": []}, work)
            with self.assertRaisesRegex(ValueError, "cycle"):
                verify_include_carrier({**unit, "parent_carriers": [parent, parent]}, work)
            (work / "root.asm").write_text("include unrelated.inc\n")
            with self.assertRaisesRegex(ValueError, "drifted"):
                verify_include_carrier(unit, work)
            parent["sha256"] = sha((work / "root.asm").read_bytes())
            with self.assertRaisesRegex(ValueError, "occur once"):
                verify_include_carrier(unit, work)

    def test_candidates_cannot_replace_accepted_inputs_or_owners(self):
        config = {"target_sha256": "pinned", "units": [{"id": "accepted", "object": "owned"}],
                  "functions": [{"name": "accepted_function"}]}
        for candidate in (
            {"schema_version": 1, "units": [], "functions": [], "target_sha256": "changed"},
            {"schema_version": 1, "units": [{"id": "accepted", "object": "new"}], "functions": []},
            {"schema_version": 1, "units": [{"id": "new", "object": "owned"}], "functions": []},
            {"schema_version": 1, "units": [], "functions": [{"name": "accepted_function"}]},
        ):
            with self.assertRaises(ValueError):
                add_candidate_owners(config, candidate)
        result = add_candidate_owners(config, {"schema_version": 1,
            "units": [{"id": "candidate", "object": "candidate"}], "functions": []})
        self.assertEqual(result["target_sha256"], "pinned")
        self.assertEqual(result["units"][0], config["units"][0])
        self.assertEqual(len(config["units"]), 1)

    def test_legacy_owner_normalizes_to_one_code_extent(self):
        unit = {
            "id": "legacy", "object": "legacy", "start": 0x20, "size": 4,
            "padding_ranges": [[2, 1]],
        }
        extents = normalized_code_extents(unit, 0x1234)
        self.assertEqual(len(extents), 1)
        self.assertEqual(extents[0]["ledger_id"], "legacy")
        self.assertEqual(extents[0]["segment"], 0x1234)
        self.assertEqual(
            extents[0]["producer_ranges"],
            [{"relative": 2, "size": 1, "kind": "padding"}],
        )

    def test_split_owner_keeps_discontiguous_extents_separate(self):
        unit = {
            "id": "split", "object": "split",
            "code_extents": [
                {
                    "name": "a", "ledger_id": "split-a", "segment": 0x1000,
                    "start": 0x10, "size": 2, "map_segment": "A",
                },
                {
                    "name": "b", "ledger_id": "split-b", "segment": 0x1000,
                    "start": 0x30, "size": 8, "map_segment": "B",
                    "producer_ranges": [
                        {"relative": 2, "size": 2, "kind": "switch-table"}
                    ],
                },
            ],
        }
        extents = normalized_code_extents(unit, 0x9999)
        self.assertEqual(
            [(e["name"], e["ledger_id"], e["start"], e["size"]) for e in extents],
            [("a", "split-a", 0x10, 2), ("b", "split-b", 0x30, 8)],
        )
        self.assertEqual(extents[1]["producer_ranges"][0]["kind"], "switch-table")


class MainExactOracleTests(unittest.TestCase):
    def test_equal_payload_can_have_different_header_size(self):
        a = synthetic_mz_with_relocations(((2, 0),))
        b = bytearray(a[:32] + bytes(16) + a[32:])
        struct.pack_into("<H", b, 8, 3)
        struct.pack_into("<H", b, 2, len(b))
        result = compare_extent(a, bytes(b), 0, 64)
        self.assertTrue(result["raw_equal"])
        self.assertTrue(result["relocations_equal"])
        self.assertNotEqual(result["target_file_offset"], result["candidate_file_offset"])

    def test_last_owned_byte_is_not_omitted(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 15] ^= 1
        result = compare_extent(a, bytes(b), 0, 16)
        self.assertFalse(result["raw_equal"])
        self.assertEqual(result["differing_bytes"], 1)

    def test_relocated_word_values_are_never_masked(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 2] ^= 1
        result = compare_extent(a, bytes(b), 0, 16)
        self.assertFalse(result["raw_equal"])
        self.assertTrue(result["relocations_equal"])

    def test_relocation_order_and_duplicates_are_not_sets(self):
        a = synthetic_mz_with_relocations(((2, 0), (4, 0), (4, 0)))
        b = synthetic_mz_with_relocations(((4, 0), (2, 0), (4, 0)))
        c = synthetic_mz_with_relocations(((2, 0), (4, 0), (2, 0)))
        for changed in (b, c):
            self.assertTrue(compare_extent(a, changed, 0, 16)["raw_equal"])
            self.assertFalse(compare_extent(a, changed, 0, 16)["relocations_equal"])

    def test_outside_bytes_do_not_receive_owned_extent_credit(self):
        a = synthetic_mz()
        b = bytearray(a)
        b[32 + 40] ^= 1
        self.assertTrue(compare_extent(a, bytes(b), 0, 16)["raw_equal"])

    def test_split_relocation_and_out_of_bounds_are_rejected(self):
        a = synthetic_mz()
        for start, size in ((0, 3), (3, 8), (0, 65), (-1, 8), (0, 0)):
            with self.assertRaises(ValueError):
                compare_extent(a, a, start, size)

    def test_invalid_container_is_rejected(self):
        a = synthetic_mz()
        b = bytearray(a)
        struct.pack_into("<H", b, 2, 600)
        self.assertFalse(parse_mz(bytes(b)).valid)
        with self.assertRaises(ValueError):
            compare_extent(a, bytes(b), 0, 16)


if __name__ == "__main__":
    unittest.main()
