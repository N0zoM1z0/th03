"""Score ownership checks cover actual native codecs, near DATA and MZ order."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_score_native import verify, CS, DS, DATA


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class ScoreNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_codecs_and_near_filename_storage(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([(o['size'], o['procedure_count']) for o in row['owners']], [(165, 1), (11, 0), (229, 3)])
        self.assertEqual(sum(len(o['native_fields']) for o in row['native_objects']), 33)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']), 7)
        self.assertEqual((row['BSS_extent'], row['BSS_raw_byte_credit']), ([DS, 0x2394, 206], 0))

    def test_equal_corrupted_checksum_images_do_not_replace_native_code(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x19C8 + 1] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate CODE'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_equal_bad_near_pointers_do_not_replace_native_data(self):
        raw = bytearray(self.target.program_image)
        raw[DS * 16 + DATA] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'semantic/native/target/candidate DATA'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_random_and_file_relocations_keep_literal_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if CS * 16 + 0x1868 <= r.linear < CS * 16 + 0x190D]
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
