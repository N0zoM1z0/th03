"""Failure controls for compiler-coordinate diagnostics, without target data."""
import sys
from pathlib import Path
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_th03_decoded_code import code_rows, extent_observation, function_observation


def image(data, records=()):
    return SimpleNamespace(program_image=data, relocations=[
        SimpleNamespace(segment=segment, offset=offset, linear=segment * 16 + offset)
        for segment, offset in records])


class DecodedCodeReviewTests(unittest.TestCase):
    def test_map_separator_and_zero_contribution(self):
        text = (" 0000:0002 0002 C=CODE S=SHARED G=(none) M=th03\\x.asm   ACBP=48\n"
                " 0000:0004 0000 C=CODE S=EMPTY G=(none) M=th03\\x.asm ACBP=48\n")
        rows = code_rows(text, 4)
        self.assertEqual([r["size"] for r in rows], [2, 0])
        self.assertEqual(rows[0]["module"], "th03/x.asm")

    def test_unparsed_code_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unparsed CODE"):
            code_rows(" 0000:0000 0001 C=CODE unexpected", 4)

    def test_overlap_and_truncated_image_are_rejected(self):
        row = " 0000:0000 0002 C=CODE S=X G=(none) M=x ACBP=48\n"
        with self.assertRaisesRegex(ValueError, "overlapping"):
            code_rows(row + row, 4)
        with self.assertRaisesRegex(ValueError, "exceeds"):
            code_rows(row, 1)

    def test_equal_bytes_do_not_hide_ordered_relocation_failure(self):
        target = image(b"1234", [(0, 0), (0, 2)])
        candidate = image(b"1234", [(0, 2), (0, 0)])
        observed = extent_observation(target, candidate, dict(start=0, size=4))
        self.assertTrue(observed["raw_slice_equal"])
        self.assertFalse(observed["ordered_relocations_equal"])
        self.assertFalse(observed["source_acceptance"])
        self.assertFalse(observed["target_boundary_reviewed"])

    def test_relocated_word_is_compared_without_masking(self):
        observed = extent_observation(image(b"1234", [(0, 0)]),
                                      image(b"9234", [(0, 0)]), dict(start=0, size=4))
        self.assertEqual(observed["different_bytes"], 1)
        self.assertFalse(observed["raw_slice_equal"])

    def test_straddling_relocation_and_out_of_bounds_slice_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "straddles"):
            extent_observation(image(b"1234", [(0, 1)]), image(b"1234"),
                               dict(start=2, size=2))
        with self.assertRaisesRegex(ValueError, "exceed"):
            extent_observation(image(b"12"), image(b"12"), dict(start=1, size=2))

    def test_complete_function_requires_the_reviewed_return(self):
        function = dict(segment=0, offset=0, size=2, return_hex="c3",
                        carrier="a.cpp", implementation="b.cpp")
        files = {"a.cpp": b"include", "b.cpp": b"function"}
        with self.assertRaisesRegex(ValueError, "reviewed return"):
            function_observation(image(b"\x90\xcb"), image(b"\x90\xcb"), function, files)
        with self.assertRaisesRegex(ValueError, "fully decode"):
            function_observation(image(b"\x90\x0f"), image(b"\x90\x0f"), function, files)
        observed = function_observation(image(b"\x90\xc3"), image(b"\x90\xc3"),
                                        function, files)
        self.assertFalse(observed["source_acceptance"])


if __name__ == "__main__":
    unittest.main()
