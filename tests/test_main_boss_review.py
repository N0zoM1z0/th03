import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "review_th03_main_boss", ROOT / "scripts/review_th03_main_boss.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class MainBossReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.review = MODULE.review()

    def test_complete_main_03_partition(self):
        self.assertTrue(self.review["pass"])
        self.assertEqual(self.review["owner_count"], 10)
        self.assertEqual(self.review["function_count"], 93)
        self.assertEqual(self.review["owned_bytes"], 0x47E0)
        self.assertEqual(self.review["function_bytes"], 17683)
        self.assertEqual(self.review["producer_owned_bytes"], 717)
        self.assertEqual(
            self.review["function_bytes"] + self.review["producer_owned_bytes"],
            self.review["owned_bytes"],
        )
        self.assertTrue(all(owner["complete_partition"] for owner in self.review["owners"]))

    def test_nine_update_switch_tables_are_explicit_data(self):
        tables = [
            table
            for owner in self.review["owners"]
            for table in owner["producer_owned_ranges"]
        ]
        self.assertEqual(len(tables), 9)
        self.assertEqual(
            [table["size"] for table in tables],
            [81, 81, 80, 72, 81, 80, 81, 80, 81],
        )
        self.assertEqual(sum(table["size"] for table in tables), 717)
        self.assertTrue(all(table["kind"] == "tc4-switch-table" for table in tables))
        self.assertTrue(all(table["relocation_count"] == 0 for table in tables))

    def test_large_update_functions_use_real_retf_boundaries(self):
        expected = {
            "gba_boss_update_marisa": 269,
            "gba_boss_update_mima": 298,
            "gba_boss_update_yumemi": 368,
            "gba_boss_update_reimu": 296,
            "gba_boss_update_ellen": 269,
            "gba_boss_update_kotohime": 332,
            "gba_boss_update_chiyuri": 613,
            "gba_boss_update_kana": 316,
            "gba_boss_update_rikako": 285,
        }
        functions = {
            function["name"]: function
            for owner in self.review["owners"]
            for function in owner["functions"]
        }
        for name, size in expected.items():
            with self.subTest(name=name):
                self.assertEqual(functions[name]["size"], size)
                self.assertEqual(functions[name]["return_mnemonic"], "retf")
                self.assertEqual(functions[name]["return_operand"], "")

    def test_switch_destinations_land_inside_update_instructions(self):
        functions = {
            function["name"]: function
            for owner in self.review["owners"]
            for function in owner["functions"]
        }
        for owner in self.review["owners"]:
            for table in owner["producer_owned_ranges"]:
                update = functions[table["update_function"]]
                start = update["segment_offset"]
                end = start + update["size"]
                self.assertTrue(all(start <= d < end for d in table["destinations"]))
                if table["key_count"] == 20:
                    self.assertEqual(table["keys"][-2:], [0x80, 0xFF])
                else:
                    self.assertEqual(table["key_count"], 18)
                    self.assertEqual(table["keys"][:2], [2, 3])
                    self.assertEqual(table["keys"][-2:], [0x80, 0xFF])


if __name__ == "__main__":
    unittest.main()
