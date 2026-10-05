"""Negative controls for storage/decoded separation and legacy tool status."""
import hashlib
import unittest

from review_th03_diet import check_restored, check_stored_diet, restore_succeeded
from test_pc98 import synthetic_mz


class DietReviewTests(unittest.TestCase):
    def test_stored_diet_requires_the_reviewed_mz_envelope(self):
        data = bytearray(synthetic_mz())
        data[6:8] = b"\x00\x00"
        data[28:32] = b"diet"
        check_stored_diet(bytes(data))
        for mutation in (b"not an MZ image", bytes(data[:28]),
                         bytes(data[:28]) + b"DIET" + bytes(data[32:])):
            with self.subTest(data=mutation), self.assertRaises(ValueError):
                check_stored_diet(mutation)

    def test_decoded_full_hash_does_not_mask_relocated_bytes(self):
        data = synthetic_mz()
        expected = {"decoded_format": "mz", "decoded_size": len(data),
                    "decoded_sha256": hashlib.sha256(data).hexdigest()}
        self.assertTrue(check_restored(data, expected)["format_integrity"]["valid"])
        changed_relocation = bytearray(data)
        changed_relocation[34:36] = b"\x35\x12"
        for changed in (data[:-1], data[:-1] + b"\xc3", bytes(changed_relocation)):
            with self.assertRaises(ValueError):
                check_restored(changed, expected)
        for declaration in ({**expected, "decoded_format": "com"},
                            {**expected, "reference_input_md5": "0" * 32}):
            with self.assertRaises(ValueError):
                check_restored(data, declaration)

    def test_flat_decoded_com_remains_distinct_from_stored_mz(self):
        data = b"\xeb\x00\xcd\x20"
        expected = {"decoded_format": "com", "decoded_size": len(data),
                    "decoded_sha256": hashlib.sha256(data).hexdigest()}
        self.assertEqual(check_restored(data, expected)["format"], "com")
        with self.assertRaises(ValueError):
            check_stored_diet(data)

    def test_legacy_success_status_needs_the_success_message(self):
        self.assertTrue(restore_succeeded(1, b"Success! (100 to 200 bytes)"))
        for status, output in ((1, b"Failure"), (0, b"Success!"), (2, b"Success!")):
            with self.subTest(status=status):
                self.assertFalse(restore_succeeded(status, output))


if __name__ == "__main__":
    unittest.main()
