"""The full library decoder, shared error frame and actual native field order."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_pi_decoder_native import verify, START, SIZE


@unittest.skipUnless((ROOT / '.analysis/work/mainl-build.json').is_file(), 'private current MAINL cold proof absent')
class PiDecoderNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def test_full_decoder_is_library_with_four_procedures_and_shared_exit(self):
        row = verify(ROOT, build.WORK, self.target, self.candidate, self.graph, self.files)
        owner, = row['owners']
        self.assertEqual((owner['origin'], owner['size'], owner['procedure_count']), ('library', 1524, 4))
        self.assertEqual(owner['shared_exit']['size'], 11)
        self.assertEqual([p['size'] for p in owner['procedures']], [1211, 238, 44, 18])
        self.assertEqual(len(row['native_fields']), 6)
        self.assertEqual(row['ordered_relocations'], [[0, a] for a in (0x103C, 0x1120, 0x1179, 0x14EC)])
        self.assertFalse(row['shared_error_is_procedure'])

    def test_equal_corrupted_images_cannot_hide_native_decoder_mismatch(self):
        raw = bytearray(self.target.program_image)
        raw[START + SIZE - 3] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            verify(ROOT, build.WORK, bad, bad, self.graph, self.files)

    def test_four_segment_relocations_keep_literal_order(self):
        relocs = list(self.target.relocations)
        slots = [i for i, r in enumerate(relocs) if START <= r.linear < START + SIZE]
        self.assertEqual(len(slots), 4)
        relocs[slots[0]], relocs[slots[1]] = relocs[slots[1]], relocs[slots[0]]
        bad = replace(self.target, relocations=relocs)
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            verify(ROOT, build.WORK, bad, bad, self.graph, self.files)


if __name__ == '__main__':
    unittest.main()
