"""Current title OMF resolves independently of equal candidate/target images."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_title_native import verify, CS, BASE


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class TitleNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_five_procedures_including_unmodified_column(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([(o['size'], o['procedure_count']) for o in row['owners']], [(808, 4), (94, 1)])
        self.assertEqual((len(row['native_fields']), len(row['ordered_relocations'])), (97, 53))
        self.assertEqual(row['owners'][1]['procedures'][0]['callee_pop_bytes'], 2)
        self.assertEqual(row['owners'][1]['ordered_relocations'], [])

    def test_equal_corrupted_column_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + BASE + 808 + 14] ^= 1  # Original ADD DI,AX encoding.
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_intro_relocations_remain_in_literal_emitted_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if CS * 16 + BASE <= r.linear < CS * 16 + BASE + 550]
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
