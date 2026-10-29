"""Actual native module gaps, packed archive state and reader ABI."""
from dataclasses import replace
import csv
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_archive_native import verify, REPORT


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected archive pair absent')
class ArchiveNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_readers_and_state_exclude_real_linker_gaps(self):
        row = self.check()
        self.assertEqual((len(row['owners']), row['procedures']), (24, 17))
        self.assertEqual((sum(o['size'] for o in row['owners']), row['source_CODE_bytes'],
                          row['source_initialized_DATA_bytes']), (1045, 1040, 5))
        self.assertEqual((row['authored_CODE_bytes'], row['library_CODE_bytes']), (281, 759))
        self.assertEqual((row['packed_BFILE_bytes'], row['packed_PFILE_bytes']), (9, 31))
        self.assertEqual(len(row['near_dispatch_consumers']), 5)
        self.assertEqual(sum(len(n['fields']) for n in row['native_scopes']), 13)
        gaps = row['independent_native_module_layout']
        self.assertEqual(gaps['reader_native_bytes'], 175)
        self.assertTrue(gaps['source_explicit_zero_removed'])
        self.assertEqual(gaps['gap_source_byte_credit'], 0)
        self.assertFalse(gaps['source_padding_added'])
        with (ROOT / 'config/units.csv').open() as stream:
            gap, = [u for u in csv.DictReader(stream)
                    if u['id'] == 'th03-mainl-decoded-root-tail-pfgetc-zero']
        self.assertEqual((gap['state'], gap['kind']), ('excluded', 'linker-gap'))
        self.assertNotIn(gap['id'], {o['unit_id'] for o in row['owners']})

    def test_equal_corrupted_reader_images_cannot_hide_independent_native_mismatch(self):
        image = bytearray(self.target.program_image)
        image[0x1904 + 8] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_contextual_gap_is_compared_without_source_credit(self):
        image = bytearray(self.target.program_image)
        image[0x19A3] = 0x90
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'matching contextual target gap bytes'):
            self.check(bad, bad)

    def test_dispatch_offset_does_not_gain_mz_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x2B92)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
