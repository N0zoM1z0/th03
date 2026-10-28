"""Small regressions for the Music Room exact comparator."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.op_music_menu import layout, START
from review_th03_op_cfg_work import images
import review_th03_op_music_menu_work as review


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class MusicNative(unittest.TestCase):
    def test_complete_current_native_receipt(self):
        import json
        row = review.examine()
        self.assertEqual((row['procedures'], row['code_bytes']), (14, 2244))
        self.assertEqual(row, json.loads(review.REPORT.read_bytes()))

    def test_equal_corrupted_images_cannot_hide_native_mismatch(self):
        work, target, *_ = images(ROOT)
        raw = bytearray(target.program_image)
        raw[START + 1] ^= 1
        bad = replace(target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'complete native/target/candidate menu bytes'):
            layout(ROOT, work, bad, bad)


if __name__ == '__main__':
    unittest.main()
