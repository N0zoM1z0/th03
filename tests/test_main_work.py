"""Current mixed-link comparisons reject raw and literal relocation regressions."""

from pathlib import Path
from unittest.mock import patch
import tempfile
import unittest
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_th03_main_work as work
from lib.pc98 import parse_mz


@unittest.skipUnless(
    (work.WORK / "bin/th03/main.exe").is_file(), "current MAIN work tree unavailable"
)
class MainWorkTests(unittest.TestCase):
    def setUp(self):
        self.raw = (work.WORK / "bin/th03/main.exe").read_bytes()
        self.image = parse_mz(self.raw)
        self.cfg = tomllib.loads(
            (ROOT / "config/th03_main_exact_units.toml").read_text()
        )

    def run_image(self, raw):
        with tempfile.TemporaryDirectory(dir=ROOT / ".analysis/work") as folder:
            root = Path(folder)
            p = root / "bin/th03/main.exe"
            p.parent.mkdir(parents=True)
            p.write_bytes(raw)
            with patch.object(work, "WORK", root):
                return work.review()

    def extents(self):
        for u in self.cfg["units"]:
            for e in u.get("code_extents", [u]):
                lo = (
                    e.get("segment", u.get("segment", self.cfg["segment"])) * 16
                    + e["start"]
                )
                yield lo, lo + e["size"]

    def test_current_raw_result_does_not_promote_exact(self):
        result = self.run_image(self.raw)
        self.assertEqual(
            (result["checked_accepted_extents"], result["checked_accepted_bytes"]),
            (87, 66843),
        )
        self.assertTrue(all(s["raw_equal"] for s in result["new_scopes"]))
        self.assertFalse(result["new_scopes"][2]["ordered_relocations_equal"])
        self.assertFalse(result["exact_acceptance"])
        self.assertFalse(result["cold_build"])

    def test_last_owned_byte_mutation_rejected(self):
        lo, hi = next(self.extents())
        raw = bytearray(self.raw)
        raw[self.image.header.header_paragraphs * 16 + hi - 1] ^= 1
        with self.assertRaisesRegex(ValueError, "accepted scope regressed"):
            self.run_image(raw)

    def test_literal_relocation_reorder_rejected(self):
        for lo, hi in self.extents():
            sites = [
                i for i, r in enumerate(self.image.relocations) if lo <= r.linear < hi
            ]
            if len(sites) >= 2:
                break
        else:
            self.fail("no reviewed multi-relocation extent")
        a, b = (self.image.header.relocation_table_offset + i * 4 for i in sites[:2])
        raw = bytearray(self.raw)
        raw[a : a + 4], raw[b : b + 4] = raw[b : b + 4], raw[a : a + 4]
        self.assertEqual(parse_mz(raw).program_image, self.image.program_image)
        with self.assertRaisesRegex(ValueError, "accepted scope regressed"):
            self.run_image(raw)


if __name__ == "__main__":
    unittest.main()
