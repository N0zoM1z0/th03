"""Loss rings, near-this stack width and state ownership use real guest code."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.pc98 import parse_mz
from lib.main_lose_renderer_runtime import Machine, negative_controls, specification


@unittest.skipUnless((ROOT / ".analysis/targets/th03/main.exe").is_file(), "private target absent")
class LoseRendererRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = parse_mz((ROOT / ".analysis/targets/th03/main.exe").read_bytes())

    def test_three_rings_cover_all_177_instruction_bytes(self):
        machine = Machine(self.image, 0x2000)
        seen = set()
        for pid in (0, 1, 2, 255):
            result, visited = machine.run(127, pid, pid)
            seen.update(visited)
            self.assertEqual(len(result["calls"]), 48)
        self.assertEqual(len(seen), 177)

    def test_negative_odd_radius_divides_toward_zero_and_wraps_byte_angles(self):
        result, _ = Machine(self.image, 0x3000).run(-5, 0)
        self.assertEqual([result["calls"][i] for i in (0, 16, 32, 47)],
                         [(255, 31), (1, 225), (255, 255), (239, 239)])

    def test_extreme_signed_radii_and_both_stack_locations(self):
        machine = Machine(self.image, 0x3000)
        for seed, radius in enumerate((-32768, -32767, 32766, 32767)):
            result, _ = machine.run(radius, seed & 1, seed)
            self.assertEqual(result["calls"], specification(radius))

    def test_eight_actual_guest_mutations_fail_independent_contracts(self):
        self.assertEqual(negative_controls(self.image)["count"], 8)
