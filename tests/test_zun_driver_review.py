"""Reject misleading candidate boundaries using synthetic 16-bit code only."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_zun_driver import decode_procedures, procedure_ranges


def row(start=0x100, size=1, distance="near"):
    return dict(start=start, size=size, candidate_distance=distance)


class DriverReviewTests(unittest.TestCase):
    def test_gap_data_is_outside_complete_procedure(self):
        text = ("sub_100 proc near\nretn\nsub_100 endp\n"
                "db 2 dup(0)\nnop\nsub_104 proc far\niret\n"
                "sub_104 endp\naGbgvgkpkpmvOFs db 0\n")
        ranges = procedure_ranges(text, 0x105)
        self.assertEqual([r["size"] for r in ranges], [1, 1])
        decoded = decode_procedures(b"\xc3\0\0\x90\xcf", ranges)
        self.assertEqual([r["return_kind"] for r in decoded], ["ret", "iret"])

    def test_missing_and_overlapping_endp(self):
        with self.assertRaisesRegex(ValueError, "ENDP"):
            procedure_ranges("sub_100 proc near\n", 0x110)
        with self.assertRaisesRegex(ValueError, "overlapping"):
            procedure_ranges("sub_100 proc near\nsub_101 proc near\n"
                             "sub_100 endp\nsub_101 endp\naGbgvgkpkpmvOFs", 0x110)

    def test_nonmonotonic_candidate_addresses(self):
        with self.assertRaisesRegex(ValueError, "invalid"):
            procedure_ranges("sub_101 proc near\nsub_101 endp\n"
                             "sub_100 proc near\nsub_100 endp\naGbgvgkpkpmvOFs", 0x110)

    def test_bounds_incomplete_instruction_and_return(self):
        for data, ranges, error in [(b"\xc3", [row(size=2)], "exceeds"),
                                    (b"\xb8", [row()], "completely decode"),
                                    (b"\x90", [row()], "return"),
                                    (b"\xc3", [row(distance="far")], "interrupt"),
                                    (b"\xcf", [row()], "interrupt")]:
            with self.subTest(error=error):
                with self.assertRaisesRegex(ValueError, error):
                    decode_procedures(data, ranges)

    def test_branch_into_instruction_operand(self):
        # JMP to 103, inside the MOV AX immediate at 102.
        with self.assertRaisesRegex(ValueError, "noninstruction"):
            decode_procedures(b"\xeb\x01\xb8\0\0\xc3", [row(size=6)])

    def test_branch_into_unowned_gap(self):
        with self.assertRaisesRegex(ValueError, "noninstruction"):
            decode_procedures(b"\xeb\x01\xc3\0\xc3", [row(size=3), row(0x104)])

    def test_call_into_procedure_interior(self):
        with self.assertRaisesRegex(ValueError, "interior"):
            decode_procedures(b"\xe8\x01\0\x90\xc3", [row(size=5)])

    def test_direct_and_indirect_calls_remain_distinct(self):
        decoded = decode_procedures(b"\xe8\x01\0\xc3\xff\xd0\xc3",
                                    [row(size=4), row(0x104, 3)])
        self.assertEqual(decoded[0]["edges"][0]["target"], 0x104)
        self.assertIsNone(decoded[1]["edges"][0]["target"])


if __name__ == "__main__":
    unittest.main()
