"""Complete real selection objects, including the historical relocation seam."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_select_native import verify, CS


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class SelectNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_two_tus_and_all19_function_abis(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([(o['size'], o['procedure_count']) for o in row['owners']], [(107,1),(48,1),(2858,17)])
        self.assertEqual((row['code_bytes'], row['procedures']), (3013,19))
        self.assertEqual(sum(len(o['native_fields']) for o in row['native_objects']),287)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']),91)

    def test_equal_corrupted_large_menu_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x2188 + 1] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_curve_relocation_order_cannot_be_replaced_with_membership(self):
        relocs = list(self.target.relocations)
        slots = [i for i,r in enumerate(relocs) if CS * 16 + 0x1E47 <= r.linear < CS * 16 + 0x1FA6]
        self.assertGreaterEqual(len(slots),2)
        relocs[slots[0]],relocs[slots[1]] = relocs[slots[1]],relocs[slots[0]]
        bad = replace(self.target,relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT,self.work,bad,bad,self.files)


if __name__ == '__main__':
    unittest.main()
