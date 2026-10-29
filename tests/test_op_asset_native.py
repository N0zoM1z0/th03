"""Current PI producers and PFOPEN's real split carrier, without image-only proof."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_asset_native import verify, CS, PF_START


@unittest.skipUnless((ROOT / '.analysis/work/op-build.json').is_file(), 'private current OP proof absent')
class AssetNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_pi_and_actual_split_pfopen_procedures(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual([o['size'] for o in row['owners']], [37, 136, 70, 281])
        self.assertEqual([o['procedures'][0]['callee_pop_bytes'] for o in row['owners']], [2, 6, 6, 8])
        self.assertEqual(sum(len(o['native_fields']) for o in row['native_objects']), 28)
        self.assertEqual(sum(len(o['ordered_relocations']) for o in row['owners']), 5)
        self.assertEqual(row['owners'][-1]['object'], 'obj/th03/optail.obj')
        self.assertEqual(row['native_objects'][-1]['complete_containing_CODE_bytes'], 1258)

    def test_equal_corrupted_pfopen_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[PF_START + 1] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_equal_corrupted_pi_headers_cannot_hide_native_field_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + 0x4A6 + 160] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_palette_relocations_keep_literal_emitted_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if CS * 16 + 0x4A6 <= r.linear < CS * 16 + 0x4CB]
        self.assertEqual(len(slots), 2)
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_pfopen_same_cs_bridges_cannot_gain_segment_relocations(self):
        relocation = replace(self.target.relocations[0], segment=0, offset=PF_START + 0x10)
        bad = replace(self.target, relocations=[*self.target.relocations, relocation])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
