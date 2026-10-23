"""The original four palette entries satisfy independent state and ABI contracts."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_stage_palette_runtime import compare, negative_controls
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact


@unittest.skipUnless((ROOT / ".analysis/targets/th03/main.exe").is_file(), "private Japanese MAIN unavailable")
class StagePaletteRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main")
        cls.image = parse_mz(read_verified_artifact(ROOT, artifact))

    def test_target_against_the_independent_memory_and_abi_model(self):
        result = compare(self.image, self.image)
        self.assertTrue(result["equal"])
        self.assertEqual((result["cases"], result["code_bytes_executed"]), (1556, 128))

    def test_semantic_abi_and_unrelated_memory_mutations_are_rejected(self):
        result = negative_controls(self.image)
        self.assertEqual(result["count"], 8)


if __name__ == "__main__":
    unittest.main()
