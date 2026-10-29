"""Native CDG SMC destinations and ordinary assembler layout remain distinct."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_cdg_draw_native import verify, CS


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class CdgDrawNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_smc_procedures_and_separate_even_layout(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([(o['size'], o['procedure_count']) for o in row['owners']], [(382, 2), (114, 1)])
        self.assertEqual((row['procedure_body_bytes'], row['outer_EVEN_bytes'], row['self_modifying_WORDs']), (493, 3, 12))
        self.assertEqual(sum(len(o['native_fields']) for o in row['native_objects']), 19)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']), 2)

    def test_equal_corrupted_smc_targets_do_not_replace_native(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x170 + 31] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved OP native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_ordinary_even_byte_is_checked_against_actual_object(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x170 + 179] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved OP native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_two_far_calls_keep_literal_relocation_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if CS * 16 + 0x170 <= r.linear < CS * 16 + 0x2EE]
        self.assertEqual(len(slots), 2)
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered OP MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
