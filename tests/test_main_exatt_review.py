import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "review_th03_main_exatt_family",
    ROOT / "scripts/review_th03_main_exatt_family.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MainExtraAttackReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = MODULE.review()

    def test_complete_residual_partition(self):
        self.assertTrue(self.review["pass"])
        self.assertEqual(self.review["owner_count"], 10)
        self.assertEqual(self.review["function_count"], 52)
        self.assertEqual(self.review["p_exatt_bytes"], 4500)
        self.assertEqual(self.review["main06_bytes"], 4281)
        self.assertEqual(self.review["owned_bytes"], 8781)
        self.assertEqual(self.review["function_bytes"], 8781)
        self.assertEqual(self.review["producer_owned_bytes"], 0)

    def test_generic_exatt_owner_gap_is_explicit(self):
        self.assertEqual(self.review["generic_exatt_gap_start"], 0x119E)
        self.assertEqual(self.review["generic_exatt_gap_end"], 0x11C7)
        self.assertEqual(
            self.review["generic_exatt_gap_end"]
            - self.review["generic_exatt_gap_start"],
            41,
        )

    def test_large_functions_are_in_complete_owners(self):
        funcs = {
            f["name"]: f
            for owner in self.review["owners"]
            for f in owner["functions"]
        }
        expected = {
            "yumemi_1A9B0": 1150,
            "exatt_update_ellen": 470,
            "exatt_update_mima": 398,
            "exatt_update_kotohime": 351,
            "exatt_update_yumemi": 324,
            "exatt_update_rikako": 300,
            "exatt_update_chiyuri": 298,
            "exatt_update_reimu": 281,
        }
        for name, size in expected.items():
            with self.subTest(name=name):
                self.assertEqual(funcs[name]["size"], size)

    def test_relocation_partition(self):
        self.assertEqual(self.review["relocation_count"], 140)
        expected = {
            "th03-main-exatt-chiyuri": 23,
            "th03-main-exatt-ellen": 14,
            "th03-main-exatt-kana": 8,
            "th03-main-exatt-marisa": 7,
            "th03-main-exatt-kotohime": 15,
            "th03-main-exatt-shared-main06": 4,
            "th03-main-exatt-reimu": 14,
            "th03-main-exatt-mima": 10,
            "th03-main-exatt-yumemi": 36,
            "th03-main-exatt-rikako": 9,
        }
        for owner in self.review["owners"]:
            with self.subTest(owner=owner["id"]):
                self.assertEqual(owner["relocation_count"], expected[owner["id"]])

    def test_every_owner_is_a_function_only_partition(self):
        for owner in self.review["owners"]:
            with self.subTest(owner=owner["id"]):
                self.assertTrue(owner["complete_partition"])
                self.assertEqual(owner["function_bytes"], owner["owner_size"])
                self.assertEqual(owner["producer_owned_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
