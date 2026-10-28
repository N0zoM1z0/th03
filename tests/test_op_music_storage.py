"""Complete native DATA comparison and literal relocation-order regression."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib.op_music_storage import verify, DS, DATA, SIZE
from review_th03_op_cfg_work import images


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class MusicStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)

    def test_whole_data_and_separate_bss_layout(self):
        row = verify(ROOT, self.work, self.target, self.candidate)
        self.assertEqual((row['initialized_data_bytes'], len(row['ordered_native_fields']), len(row['ordered_relocations'])), (1008, 40, 40))
        self.assertEqual((row['bss_bytes'], row['BSS_raw_byte_credit'], row['bss_file_backed']), (1060, 0, False))

    def test_equal_corrupted_images_do_not_override_native_data(self):
        raw = bytearray(self.target.program_image)
        raw[DS * 16 + DATA + 162] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'complete semantic/native/target/candidate DATA'):
            verify(ROOT, self.work, bad, bad)

    def test_same_relocation_membership_with_wrong_order_rejects(self):
        relocs = list(self.target.relocations)
        slots = [i for i,r in enumerate(relocs) if DS * 16 + DATA <= r.linear < DS * 16 + DATA + SIZE]
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'literal ordered DATA relocation vector'):
            verify(ROOT, self.work, bad, bad)


if __name__ == '__main__':
    unittest.main()
