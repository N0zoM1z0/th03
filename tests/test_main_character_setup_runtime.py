"""Character-resource and callback contracts are independent of compiler output."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_character_setup_runtime import compare, negative_controls
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact


@unittest.skipUnless((ROOT / ".analysis/targets/th03/main.exe").is_file(), "private Japanese MAIN unavailable")
class CharacterSetupRuntime(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main")
        cls.image = parse_mz(read_verified_artifact(ROOT, artifact))

    def test_target_has_complete_memory_and_abi_coverage(self):
        result = compare(self.image, self.image)
        self.assertTrue(result["equal"])
        self.assertEqual((result["cases"], result["code_bytes_executed"], result["primitive_code_bytes_executed"]),
                         (1020, 3888, 80))

    def test_semantic_pointer_argument_and_abi_mutations_are_rejected(self):
        self.assertEqual(negative_controls(self.image)["count"], 16)


if __name__ == "__main__":
    unittest.main()
