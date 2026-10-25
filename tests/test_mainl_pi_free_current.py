"""PI release ownership, full-WORD tests, aliasing and bounded heap replies."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_pi_free_work import REPORT, witness
from lib.decoded_mainl_pi_free_layout import verify
from lib.decoded_mainl_pi_free_runtime import Machine, address, negative_controls

WORK = ROOT / '.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK / 'bin/th03/mainl.exe').is_file(), 'private current MAINL absent')
class PiFree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work, cls.target, cls.candidate, _, _, cls.graph, cls.files = images(ROOT)

    def machine(self):
        machine = Machine(self.target, 0x3000)
        self.addCleanup(machine.close)
        return machine

    def test_complete_native_owner_has_no_fields_and_keeps_macro_calls(self):
        scope = verify(self.work, self.target, self.candidate, self.graph, self.files)
        self.assertEqual((scope['functions'], scope['code_bytes']), (1, 76))
        self.assertEqual(scope['ordered_native_fields'], [])
        self.assertEqual(scope['ordered_relocations'], [])
        self.assertEqual(scope['native_nopcall_sites'], [0xFFD, 0x1016, 0x102F])
        self.assertFalse(scope['heap_body_accepted'])
        self.assertFalse(scope['containing_producer_accepted'])

    def test_matching_corruption_in_both_images_cannot_hide_native_disagreement(self):
        def corrupt(image):
            raw = bytearray(image.program_image)
            raw[0xFF7] ^= 2
            return replace(image, program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError, 'complete unmodified native function bytes'):
            verify(self.work, corrupt(self.target), corrupt(self.candidate), self.graph, self.files)

    def test_both_segment_bytes_matter_and_repeated_segments_are_not_deduplicated(self):
        machine = self.machine()
        for value in (1, 0x100, 0x8000, 0xFFFF):
            result = machine.run(segments=(value,) * 3)
            self.assertEqual([e[1] for e in result['events'] if e[0] == 'heap'], [value] * 3)

    def test_zero_segments_preserve_nonzero_offset_and_length_fields(self):
        machine = self.machine()
        result = machine.run(segments=(0, 0, 0))
        self.assertEqual(result['heap_calls'], 0)
        self.assertEqual(len(result['events']), 1)  # Only the saved BP.
        self.assertNotEqual(bytes(machine.u.mem_read(address(0x5000, 0x1234, 4), 2)), b'\0\0')
        self.assertEqual(result['registers']['ax'], 0)

    def test_failed_frees_still_clear_all_six_fields_and_forward_final_reply(self):
        machine = self.machine()
        result = machine.run(replies=((0xFFFF, 0x895),) * 3, flags=0xED7)
        for offset in (0, 2, 4, 14, 16, 18):
            self.assertEqual(bytes(machine.u.mem_read(address(0x5000, 0x1234, offset), 2)), b'\0\0')
        self.assertEqual(result['registers']['ax'], 0xFFFF)
        self.assertEqual(result['flags'], 0xE95)

    def test_effective_offsets_wrap_before_segment_addition(self):
        result = self.machine().run(header_offset=0xFFFF, ss=0x8000, stack=0x80, foreign_ds=True)
        stores = [e[1] for e in result['events'] if e[0] == 'store']
        for offset in (0, 2, 4, 14, 16, 18):
            self.assertIn(address(0x5000, 0xFFFF, offset), stores)
        self.assertEqual((result['registers']['bx'], result['registers']['es'], result['registers']['ds']),
                         (0xFFFF, 0x5000, 0x6000))

    def test_header_alias_with_frame_changes_the_later_image_argument(self):
        result = self.machine().run(alias_frame=True)
        # Comment segment aliases image.segment. Clearing it suppresses the last
        # free even though that argument entered nonzero; LES already latched BX.
        self.assertEqual([e[1] for e in result['events'] if e[0] == 'heap'], [0x3333, 0x2222])
        self.assertEqual(result['registers']['ax'], 0)
        self.assertEqual(result['registers']['bx'], 0xF804)

    def test_image_offset_is_ignored_and_stack_frames_remain_native(self):
        machine = self.machine()
        a = machine.run(image_offset=0)
        b = machine.run(image_offset=0xFFFF)
        self.assertEqual(a, b)
        calls = [e for e in a['events'] if e[0] == 'heap']
        self.assertEqual([e[2] for e in calls], [0x1002, 0x101B, 0x1034])
        self.assertTrue(all(e[3]['sp'] == 0xF7F8 for e in calls))
        self.assertEqual(a['registers']['sp'], 0xF80C)

    def test_twenty_real_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'], 20)

    @unittest.skipUnless(REPORT.is_file(), 'complete PI release report absent')
    def test_witness_rejects_partial_paths_ignored_stack_and_heap_credit(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('PI release review running')
        scope = report['scope']
        witness(scope)
        for part, key, value in (('runtime', 'ignored_stack_bytes', 8), ('runtime', 'executed_owner_bytes', 75),
                                 ('runtime', 'heap_body_executed', True), ('layout', 'heap_body_accepted', True)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)


class PointerArithmetic(unittest.TestCase):
    def test_word_starts_wrap_but_physical_second_byte_is_adjacent(self):
        self.assertEqual(address(0x5000, 0xFFFF, 2), 0x50001)
        self.assertEqual(address(0x5000, 0xFFFF), 0x5FFFF)
