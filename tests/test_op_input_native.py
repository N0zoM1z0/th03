"""The scanner is complete without accepting its containing producer's trailer."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_op_work as build
from review_th03_op_cfg_work import images
from lib.op_input_native import verify, CS, BASE


@unittest.skipUnless((ROOT / '.analysis/work/input-assembly.obj').is_file(), 'private native emitter proof absent')
class InputNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, *_ = images(ROOT)
        cls.files = build.source_graph()

    def test_complete_body_and_two_natural_emitters_exclude_trailer(self):
        row = verify(ROOT, self.work, self.target, self.candidate, self.files)
        self.assertEqual((row['code_bytes'], len(row['native_fields'])), (417, 42))
        self.assertEqual([p['CODE_bytes'] for p in row['natural_emitters']], [417, 417])
        self.assertEqual(row['owners'][0]['procedures'][0]['instruction_count'], 115)
        self.assertEqual(row['excluded_tail_extent'], [CS, 0x4A5, 1])
        self.assertFalse(row['legacy_codestring_accepted'])
        self.assertFalse(row['trailer_layout_or_provenance_resolved'])

    def test_equal_corrupted_bios_reads_do_not_replace_native_body(self):
        raw = bytearray(self.target.program_image)
        raw[CS * 16 + BASE + 25] ^= 1
        bad = replace(self.target, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'independently resolved function/target/candidate bytes'):
            verify(ROOT, self.work, bad, bad, self.files)

    def test_near_data_words_cannot_gain_a_segment_relocation(self):
        relocation = replace(self.target.relocations[0], segment=CS, offset=BASE + 3)
        bad = replace(self.target, relocations=[*self.target.relocations, relocation])
        with self.assertRaisesRegex(ValueError, 'complete empty ordered function MZ vector'):
            verify(ROOT, self.work, bad, bad, self.files)


if __name__ == '__main__':
    unittest.main()
