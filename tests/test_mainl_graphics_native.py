"""Generated graphics masks and ordinary far-call production of page copy."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_graphics_native import verify, REPORT


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected graphics pair absent')
class GraphicsNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_graphics_and_heap_keep_aliases_and_borrowed_exits_separate(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['procedures'], row['source_CODE_bytes'],
                          row['source_initialized_DATA_bytes']), (18, 26, 2143, 66))
        self.assertEqual(sum(len(s['fields']) for s in row['native_scopes']), 93)
        self.assertEqual(len(row['packed_pixel_table_operand_fields']), 16)
        self.assertEqual((row['generated_edge_WORDs'], row['generated_BYTE_masks']), (17, 8))
        self.assertTrue(row['EGC_END_START_same_body'])
        egc, = [o for o in row['owners'] if o['unit_id'].endswith('egc-library')]
        self.assertEqual(egc['procedure_count'], 3)
        calls = row['native_far_call_review']
        self.assertEqual((calls['native_copy_bytes'], calls['literal_far_pointer_fixups'],
                          calls['naturally_relaxed_instruction_bytes']), (108, 2, 2))
        self.assertFalse(calls['source_NOP_added'])
        self.assertEqual(len(calls['memory_native_fields']), 44)
        self.assertEqual((row['heap_BSS_bytes'], row['BSS_file_byte_credit']), (8, 0))

    def test_equal_corrupted_relaxed_call_images_cannot_hide_native_link_mismatch(self):
        image = bytearray(self.target.program_image)
        image[0xEB7] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_generated_edge_table_requires_complete_semantic_bytes(self):
        image = bytearray(self.target.program_image)
        image[0xE3F * 16 + 0x532 + 18] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_cs_table_offset_does_not_gain_mz_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x168F)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
