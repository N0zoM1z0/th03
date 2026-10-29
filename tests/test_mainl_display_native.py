"""Palette operand aliases, genuine far calls and the VSync IRQ segment field."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_display_native import verify, REPORT


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected display pair absent')
class DisplayNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_bodies_interrupts_state_and_natural_calls(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['procedures'], row['source_CODE_bytes'],
                          row['source_file_DATA_bytes']), (15, 22, 1362, 77))
        self.assertEqual(sum(len(s['fields']) for s in row['native_scopes']), 57)
        self.assertEqual(row['IRQ_entries'], [0x1FD8, 0x1FE2])
        self.assertTrue(row['VSYNC_END_LEAVE_same_body'])
        self.assertTrue(row['palette_XOR_source_ORG_removed'])
        self.assertEqual(row['palette_XOR_operand_alias'], 0x18B8)
        mini = row['independent_native_modules']
        self.assertEqual((mini['modules'], mini['rounds'], len(mini['far_calls'])), (6, 2, 19))
        self.assertFalse(mini['source_padding_added'])
        self.assertEqual((row['BSS_bytes'], row['BSS_file_byte_credit']), (58, 0))
        self.assertFalse(row['source_CS_vector_initializer_added'])
        self.assertEqual(row['uncredited_DATA0849_byte'], 0x90)

    def test_equal_corrupted_saved_vector_cannot_hide_real_link_output(self):
        image = bytearray(self.target.program_image)
        image[0x1F6A] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_smc_operand_requires_complete_native_bytes(self):
        image = bytearray(self.target.program_image)
        image[0x18B8] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_irq_ds_segment_load_requires_its_literal_mz_entry(self):
        bad = replace(self.target, relocations=[r for r in self.target.relocations
                                              if (r.segment, r.offset) != (0, 0x1FE5)])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
