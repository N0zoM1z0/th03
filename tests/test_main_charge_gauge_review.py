import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from review_th03_main_charge_gauge import OWNERS


class ChargeGaugeBoundaryManifestTests(unittest.TestCase):
    def test_complete_five_owner_partition(self):
        self.assertEqual(len(OWNERS), 5)
        self.assertEqual(sum(owner["size"] for owner in OWNERS), 5802)
        self.assertEqual(sum(len(owner["functions"]) for owner in OWNERS), 48)
        self.assertEqual(len({owner["id"] for owner in OWNERS}), 5)

        for owner in OWNERS:
            cursor = owner["start"]
            for function in owner["functions"]:
                _, _, offset, size, return_mnemonic, _ = function
                self.assertEqual(offset, cursor)
                self.assertGreater(size, 0)
                self.assertIn(return_mnemonic, {"ret", "retf"})
                cursor += size
            self.assertEqual(cursor, owner["start"] + owner["size"])

    def test_owner_ranges_are_disjoint(self):
        spans = sorted(
            (
                owner["segment"] * 16 + owner["start"],
                owner["segment"] * 16 + owner["start"] + owner["size"],
                owner["id"],
            )
            for owner in OWNERS
        )
        for left, right in zip(spans, spans[1:]):
            self.assertLessEqual(left[1], right[0], (left[2], right[2]))

    def test_role_specific_return_contracts_are_explicit(self):
        # Turbo C++ Pascal helpers retain stack cleanup in the target while
        # cdecl entries do not. Keeping this in the reviewed boundary manifest
        # prevents a later source probe from silently changing the ABI.
        functions = {
            function[0]: (function[4], function[5])
            for owner in OWNERS
            for function in owner["functions"]
        }
        self.assertEqual(functions["chargeshot_add_chiyuri"], ("retf", "4"))
        self.assertEqual(functions["gauge_pattern_chiyuri"], ("ret", "2"))
        self.assertEqual(functions["ellen_chargeshot_private"], ("ret", "4"))
        self.assertEqual(functions["gauge_pattern_rikako"], ("ret", "2"))


if __name__ == "__main__":
    unittest.main()
