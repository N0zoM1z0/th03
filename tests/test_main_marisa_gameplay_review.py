"""Keep the original 1958-byte gameplay body partition fail-closed."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from review_th03_main_marisa_gameplay import inspect_body,FUNCTIONS


class MarisaGameplayReviewTests(unittest.TestCase):
    def test_expected_complete_intervals_include_boss_sized_functions(self):
        self.assertEqual(len(FUNCTIONS),10)
        self.assertEqual(FUNCTIONS[0][1],0x142D0)
        self.assertEqual(FUNCTIONS[-1][2],0x14A76)
        self.assertEqual(sum(b-a for _,a,b,_,_ in FUNCTIONS),1958)
        self.assertEqual([b-a for _,a,b,_,_ in FUNCTIONS][5:7],[414,470])
        self.assertEqual(FUNCTIONS[-1][2]-FUNCTIONS[-1][1],449)
    def test_return_abi_and_decode_cannot_be_guessed(self):
        img=SimpleNamespace(valid=True,program_image=b"\x55\x8b\xec\xcb",relocations=[])
        result=inspect_body(img,("x",0,4,"retf",None))
        self.assertEqual(result["size"],4)
        self.assertFalse(result["exact"])
        with self.assertRaises(ValueError):
            inspect_body(img,("x",0,4,"ret",None))
        with self.assertRaises(ValueError):
            inspect_body(img,("x",0,3,"retf",None))
    def test_boundary_crossing_fixup_rejected(self):
        img=SimpleNamespace(valid=True,program_image=b"\x55\x8b\xec\xcb",
                            relocations=[SimpleNamespace(linear=3)])
        with self.assertRaises(ValueError):
            inspect_body(img,("x",0,4,"retf",None))
