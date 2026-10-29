"""Complete SUPER self-modifying operands and CS DATA ownership."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_resources_native import verify, REPORT, TABLE_START, SUPER_START


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private actual selected resources pair absent')
class ResourcesNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def test_complete_super_and_generated_table_keep_code_data_and_entries_separate(self):
        row = verify(ROOT, build.WORK, self.target, self.candidate, self.graph, self.files)
        self.assertEqual([(o['size'], o['procedure_count'], o['code_bytes'], o['initialized_data_bytes'])
                          for o in row['owners']], [(1008, 11, 1008, 0), (1024, 0, 0, 1024)])
        self.assertEqual(len(row['native_fields']), 50)
        self.assertEqual(len(row['SMC_writers']), 13)
        self.assertEqual(len({s['destination'] for s in row['SMC_writers']}), 10)
        self.assertFalse(row['borrowed_errors_are_procedures'])
        self.assertFalse(row['table_is_instruction_bytes'])
        self.assertTrue(row['original_native_public_records_equal'])
        self.assertTrue(row['native_FIXUPP_order_unchanged'])
        self.assertEqual(row['selected_assembly_link_rounds'], 2)

    def test_equal_corrupted_table_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[TABLE_START + 43] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, build.WORK, bad, bad, self.graph, self.files)

    def test_equal_corrupted_self_modifying_images_cannot_hide_native_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[0x276C] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, build.WORK, bad, bad, self.graph, self.files)

    def test_near_offset_fields_do_not_gain_mz_segment_relocations(self):
        extra = replace(self.target.relocations[0], segment=0, offset=SUPER_START + 2)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, build.WORK, bad, bad, self.graph, self.files)


if __name__ == '__main__':
    unittest.main()
