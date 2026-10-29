"""File ABI and the hook's actual uninitialized file-backed sentinel."""
from dataclasses import replace
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_th03_mainl_work as build
from lib.pc98 import parse_mz
from lib.decoded_mainl_file_native import verify, REPORT, SENTINEL


@unittest.skipUnless((ROOT / REPORT).is_file(), 'private selected file pair absent')
class FileNative(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.graph, _ = build.sources()
        cls.target = parse_mz((build.WORK / 'bin/th03/mainl.target.exe').read_bytes())
        cls.candidate = parse_mz((build.WORK / 'bin/th03/mainl.exe').read_bytes())

    def check(self, target=None, candidate=None):
        return verify(ROOT, build.WORK, target or self.target, candidate or self.candidate,
                      self.graph, self.files)

    def test_complete_apis_hook_and_state_preserve_storage_classes(self):
        result = self.check()
        self.assertEqual([(o['size'], o['procedure_count'], o['code_bytes'], o['initialized_data_bytes'])
                          for o in result['owners']],
                         [(786, 11, 786, 0), (80, 2, 80, 0), (605, 3, 550, 55), (4, 0, 0, 4)])
        self.assertEqual((result['file_BSS_bytes'], result['hook_BSS_bytes'], result['BSS_file_byte_credit']),
                         (20, 134, 0))
        self.assertEqual(sum(len(n['fields']) for n in result['native_scopes']), 140)
        hook = result['native_scopes'][-1]
        self.assertEqual(len(hook['dispatch_records']), 12)
        self.assertFalse(hook['native_LEDATAs_cover_uninitialized_slot'])
        self.assertTrue(hook['slot_bytes_from_two_real_link_rounds'])
        self.assertFalse(hook['source_initializer_added'])

    def test_equal_corrupted_sentinel_images_cannot_hide_linked_storage_mismatch(self):
        image = bytearray(self.target.program_image)
        image[SENTINEL[0]] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_equal_corrupted_api_images_cannot_hide_native_mismatch(self):
        image = bytearray(self.target.program_image)
        image[0x9F2 + 10] ^= 1
        bad = replace(self.target, program_image=bytes(image))
        with self.assertRaisesRegex(ValueError, 'independently resolved native/target/candidate bytes'):
            self.check(bad, bad)

    def test_dispatch_offset_does_not_gain_mz_segment_relocation(self):
        extra = replace(self.target.relocations[0], segment=0, offset=0x29B0)
        bad = replace(self.target, relocations=[*self.target.relocations, extra])
        with self.assertRaisesRegex(ValueError, 'complete literal ordered MZ vector'):
            self.check(bad, bad)


if __name__ == '__main__':
    unittest.main()
