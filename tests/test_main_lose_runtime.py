"""Native lose behavior checks include terminal states and semantic mutations."""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lib.main_lose_runtime import execute, negative_controls  # noqa: E402
from lib.pc98 import parse_mz  # noqa: E402
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact  # noqa: E402


@unittest.skipUnless(
    (ROOT / ".analysis/targets/th03/main.exe").is_file(), "local target absent"
)
class MainLoseRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.image = parse_mz(
            read_verified_artifact(
                ROOT,
                find_artifact(
                    load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
                ),
            )
        )

    def test_boundaries_and_call_frames(self):
        for kind, seeds in (
            ("update", (0, 1, 2, 3, 96, 97, 510, 511, 3680, 3681)),
            ("particle", (0, 1, 510, 511)),
            ("banner", (0, 1, 30, 31, 32, 33, 126, 127)),
        ):
            for seed in seeds:
                with self.subTest(kind=kind, seed=seed):
                    execute(self.image, kind, seed)

    def test_semantic_mutations_fail_independent_contracts(self):
        self.assertEqual(negative_controls(self.image)["count"], 4)


if __name__ == "__main__":
    unittest.main()
