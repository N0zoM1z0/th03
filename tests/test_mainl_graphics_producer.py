import unittest
import replay_th03_mainl_graphics_producer as producer
from pathlib import Path
from replay_th03_mainl_graphics_producer import parse_fields, FIELDS, EXTERNALS, BODIES

ROOT = Path(__file__).resolve().parents[1]

class GraphicsProducerTests(unittest.TestCase):
    def test_recipe_provenance_is_hash_bound(self):
        class BadPath:
            def read_bytes(self):
                return b"{}"
        class BadRoot:
            def __truediv__(self, unused):
                return BadPath()
        with self.assertRaisesRegex(ValueError, "recipe identity"):
            producer.replay(BadRoot())

    def test_native_provenance_mutation_is_rejected(self):
        recipe = (ROOT/producer.RECIPE).read_bytes()
        class FakePath:
            def __init__(self, name):
                self.name = name
            def read_bytes(self):
                return recipe if self.name == producer.RECIPE else b"altered native proof"
        class FakeRoot:
            def __truediv__(self, name):
                return FakePath(name)
        with self.assertRaisesRegex(ValueError, "retained native proof changed"):
            producer.replay(FakeRoot())

    def test_complete_scope(self):
        self.assertEqual([x[3] for x in BODIES], [123, 21, 211])
        self.assertEqual(sum(x[3] for x in BODIES), 355)
        self.assertEqual(sum(x[1] for x in FIELDS), 22)
        self.assertEqual(len(FIELDS), 9)

    def test_explicit_offset_external(self):
        self.assertEqual(parse_fields(bytes.fromhex("c40e160101")), [(14, 2, 1)])

    def test_explicit_pointer_external(self):
        self.assertEqual(parse_fields(bytes.fromhex("ccee5606")), [(238, 4, 6)])

    def test_unknown_or_truncated_fixups_rejected(self):
        for raw in (b"\x00", bytes.fromhex("c40e1602"), bytes.fromhex("c40e160107"), bytes.fromhex("c40e5601")):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    parse_fields(raw)

    def test_symbolic_abi_and_no_opcode_arrays(self):
        source = (ROOT/"src/mainl/formats/cdg_effects.cpp").read_text()
        self.assertEqual(source.count('extern "C" void near pascal'), 2)
        self.assertIn('and si, 3', source)
        self.assertIn('_DX >>= 4;', source)
        self.assertIn('_BX <<= 3;', source)
        self.assertIn('sizeof(mainl_cdg_slot_t)==16', source)
        for forbidden in ('__emit__', '#pragma codestring', 'db 0', 'target_bytes'):
            self.assertNotIn(forbidden, source)

    def test_data_provider_names_not_addresses(self):
        self.assertEqual(EXTERNALS[:4], ['_cdg_slots', '_mainl_dissolve_alpha_enabled', '_mainl_dissolve_alpha_requested', '_mainl_dissolve_pattern'])

if __name__ == '__main__':
    unittest.main()
