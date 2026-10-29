"""Complete OP native producers, including linker bridges and text classifiers."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_shared_native import verify, CS


@unittest.skipUnless((ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class SharedNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_six_far_pascal_procedures(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([(o['size'], o['procedure_count']) for o in row['owners']], [(593, 5), (613, 1)])
        self.assertEqual(sum(len(o['native_fields']) for o in row['native_objects']), 41)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']), 27)
        self.assertEqual([o['normal_tlink_relaxed_calls'] for o in row['native_objects']], [4, 0])
        self.assertEqual([p['callee_pop_bytes'] for o in row['owners'] for p in o['procedures']], [8, 8, 6, 6, 2, 10])

    def test_equal_corrupted_text_classifier_images_do_not_replace_native(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x82B + 103] ^= 1  # __mbctype plus-one WORD field.
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved OP native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_equal_corrupted_linker_bridges_do_not_replace_normal_tlink(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x5DA + 10] ^= 1  # Normal NOP/PUSH CS/CALL bridge.
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved OP native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_cdg_relocations_keep_literal_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if CS * 16 + 0x5DA <= r.linear < CS * 16 + 0x82B]
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered OP MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
