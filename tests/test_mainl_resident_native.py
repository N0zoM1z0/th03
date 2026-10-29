"""Natural resident calls and corrected ownership of the TH03 joystick bank."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_resident_native import verify, REPORT


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private resident native pair absent')
class ResidentNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_bodies_origins_and_natural_calls(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['procedures'], row['source_CODE_bytes'],
                          row['source_initialized_DATA_bytes']), (9, 13, 559, 18))
        self.assertEqual((row['authored_CODE_bytes'], row['library_bytes']), (76, 501))
        self.assertEqual(sum(len(s['fields']) for s in row['native_scopes']), 13)
        mini = row['independent_native_modules']
        self.assertEqual((mini['modules'], mini['rounds'], len(mini['far_calls'])), (6, 2, 2))
        self.assertEqual(sum(len(m['fields']) for m in mini['native_modules']), 18)
        self.assertFalse(mini['native_source_padding_added'])
        self.assertTrue(mini['linked_WORD_gap_after_joystick103'])
        self.assertEqual(row['uncredited_legacy_zero_bytes'], [0x2AAD, 0x2B15])
        self.assertEqual((row['joystick_BSS_bytes'], row['BSS_file_byte_credit']), (4, 0))
        js = [o for o in row['owners'] if o['origin'] == 'authored']
        self.assertEqual([o['size'] for o in js], [42, 34])

    def test_equal_corrupted_create_call_cannot_hide_native_projection(self):
        image = bytearray(self.target.program_image)
        image[0x27AC] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_resident_signature_requires_its_complete_native_data(self):
        image = bytearray(self.target.program_image)
        image[0xE3F * 16 + 0x882 + 9] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_near_angle_table_reference_cannot_gain_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x1794)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
