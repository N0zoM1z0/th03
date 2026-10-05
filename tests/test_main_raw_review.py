"""Negative controls for the raw target owner boundary exporter."""

import hashlib
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from test_pc98 import synthetic_mz

try:
    from review_th03_main_code import observe
except ModuleNotFoundError as error:
    if error.name != "capstone":
        raise
    observe = None


@unittest.skipIf(observe is None, "optional diagnostic Capstone decoder unavailable")
class RawReviewTests(unittest.TestCase):
    def fixture(self, code=b"\x90\xc3"):
        target = bytearray(synthetic_mz())
        target[32:32 + len(code)] = code
        target = bytes(target)
        return target, {"target_sha256": hashlib.sha256(target).hexdigest(), "segment": 0,
            "units": [{"id": "owner", "object": "unit", "start": 0, "size": len(code)}],
            "functions": [{"name": "function", "object": "unit", "offset": 0, "size": len(code)}]}

    def test_complete_extent_has_raw_digest_and_return(self):
        target, config = self.fixture()
        result, _ = observe(config, target, ["owner"])
        self.assertEqual(result[0]["functions"][0]["return"], "ret")
        self.assertEqual(result[0]["sha256"], hashlib.sha256(b"\x90\xc3").hexdigest())

    def test_unknown_target_and_owner_are_rejected(self):
        target, config = self.fixture()
        with self.assertRaisesRegex(ValueError, "selection"):
            observe(config, target, ["unknown"])
        config["target_sha256"] = "incorrect"
        with self.assertRaisesRegex(ValueError, "identity"):
            observe(config, target, ["owner"])

    def test_holes_overlaps_and_extra_functions_cannot_claim_a_complete_owner(self):
        for kind in ("hole", "overlap", "extra"):
            target, config = self.fixture()
            if kind == "hole":
                config["units"][0]["size"] = 3
            else:
                config["functions"].append({"name": "extra", "object": "unit",
                    "offset": 0 if kind == "overlap" else 8, "size": 2})
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                observe(config, target, ["owner"])

    def test_data_after_a_return_cannot_be_silently_owned_as_the_function(self):
        target, config = self.fixture(b"\xc3\x90")
        with self.assertRaisesRegex(ValueError, "end in RET"):
            observe(config, target, ["owner"])
