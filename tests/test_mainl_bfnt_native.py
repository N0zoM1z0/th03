"""BFNT packed types, borrowed unwind and actual self-modifying operands."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_bfnt_native import verify, REPORT


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected BFNT pair absent')
class BfntNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_bodies_and_typed_storage_keep_original_unwind(self):
        row = self.check()
        self.assertEqual([(o['size'], o['procedure_count'], o['code_bytes'], o['initialized_data_bytes'])
                          for o in row['owners']], [(512, 4, 512, 0), (64, 1, 64, 0), (6, 0, 0, 6)])
        self.assertEqual(row['packed_header_bytes'], 32)
        self.assertEqual([(f['name'], f['offset']) for f in row['packed_header_fields']][-2:],
                         [('extSize', 28), ('hdrSize', 30)])
        self.assertEqual((len(row['SMC_writers']), len(row['saved_DS_operand_reads'])), (8, 3))
        self.assertEqual(sum(len(n['fields']) for n in row['native_scopes']), 13)
        self.assertFalse(row['borrowed_error_is_procedure'])
        self.assertTrue(row['original_SI_DI_swap_preserved'])
        self.assertFalse(row['header_scratch_or_palette_BSS_credited'])

    def test_equal_corrupted_operand_images_cannot_hide_native_mismatch(self):
        image = bytearray(self.target.program_image)
        image[0x35F] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_signature_terminator_requires_complete_data_equality(self):
        image = bytearray(self.target.program_image)
        image[0xE3F * 16 + 0x521] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_saved_ds_offset_does_not_gain_mz_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x296)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
