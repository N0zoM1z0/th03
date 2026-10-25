"""Complete ending orchestration, live pointers and real native helper frames."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_ending_work import REPORT, witness
from lib.decoded_mainl_ending_layout import verify, CS, START, SIZE, DATA
from lib.decoded_mainl_ending_runtime import Machine, CONTEXT

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class EndingCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def requests(self,m,role):
        return [e[2] for e in m.events if e[:2]==('service',role)]

    def test_complete_native_entry_and_separate_enclosing_storage(self):
        r = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields']),r['mz_relocation_count']),(1,280,34,14))
        self.assertEqual((r['enclosing_CODE_bytes'],r['enclosing_initialized_DATA_bytes'],r['enclosing_procedures']),(3695,224,19))
        self.assertFalse(r['enclosing_DATA_or_other_functions_accepted'])

    def test_equal_corruption_cannot_replace_native_owner_comparison(self):
        def changed(image):
            raw = bytearray(image.program_image)
            raw[CS*16+START+SIZE-1] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native ending'):
            verify(self.work,changed(self.target),changed(self.candidate),self.graph,self.files)

    def test_MZ_field_order_is_literal(self):
        changed = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_compiler_input_is_the_current_maintained_source_copy(self):
        files = dict(self.files)
        files['staffdat.cpp'] += b'\n// different transport\n'
        with self.assertRaisesRegex(ValueError,'source consumption and transport'):
            verify(self.work,self.target,self.candidate,self.graph,files)

    def test_all_actual_nested_helper_bytes_execute_in_one_UC(self):
        m = self.machine()
        r = m.run()
        helpers = {at for s,o,n in CONTEXT.values() for at in range(s*16+o,s*16+o+n)}
        self.assertTrue(helpers<=m.covered)
        self.assertEqual((len(helpers),r['stack_depth']),(227,24))
        self.assertEqual((r['counts']['free'],r['counts']['pi_heap']),(6,3))

    def test_character_zero_truncates_negative_one_divided_by_two_to_zero(self):
        m = self.machine()
        m.run(character=0)
        self.assertEqual(bytes(m.u.mem_read(0x60201,2)),b'00')

    def test_character_255_uses_signed_BYTE_127_and_wraps_decimal_additions(self):
        m = self.machine()
        m.run(character=255,digits=(255,255))
        self.assertEqual(bytes(m.u.mem_read(0x60201,2)),b'\x0B\x06')

    def test_bonus_uses_original_character_BYTE_and_exact_three_credits(self):
        m = self.machine()
        for character,credits,bonus in ((0,3,1),(14,3,1),(15,3,0),(255,3,0),(14,2,0),(14,255,0)):
            self.assertEqual(m.run(character=character,credits=credits)['counts']['bonus'],bonus)

    def test_regist_reply_can_enable_bonus_after_staff_and_stage_store(self):
        m = self.machine()
        r = m.run(character=255,credits=0,writes=(('regist',1,0x5008C,b'\x0E'),('regist',1,0x500B6,b'\x03')))
        self.assertEqual(r['counts']['bonus'],1)
        self.assertEqual(bytes(m.u.mem_read(0x500B3,1)),b'\x63')
        self.assertEqual(self.requests(m,'load'),[[0x200,0x6000],[DATA['bonus'],m.ds]])

    def test_staff_reply_redirects_the_live_resident_pointer_before_stage_store(self):
        m = self.machine()
        r = m.run(writes=(('staff',1,m.ds*16+DATA['resident'],struct.pack('<HH',0x80,0x6000)),
                          ('staff',1,0x6008C,b'\x0E'),('staff',1,0x600B6,b'\x03')))
        self.assertEqual(r['counts']['bonus'],1)
        self.assertEqual(bytes(m.u.mem_read(0x600B3,1)),b'\x63')
        self.assertEqual(bytes(m.u.mem_read(0x500B3,1)),b'\xA5')

    def test_far_script_effective_offsets_wrap_before_adding_segment(self):
        m = self.machine()
        m.run(character=255,script=(0xFFFF,0x6000))
        self.assertEqual(bytes(m.u.mem_read(0x60000,2)),b'<7')

    def test_script_digit_alias_can_change_the_next_far_pointer(self):
        m = self.machine()
        m.run(character=255,script=(0xA5D,m.ds))
        # Tens adds12 to the low byte of its own stored near offset: A5D -> A69.
        self.assertEqual(self.requests(m,'load'),[[0xA69,m.ds]])

    def test_script_pointer_is_reloaded_after_show_reply(self):
        m = self.machine()
        m.run(writes=(('show',1,m.ds*16+DATA['script'],struct.pack('<HH',0xFFFF,0x6000)),))
        self.assertEqual(self.requests(m,'load')[0],[0xFFFF,0x6000])

    def test_PI_release_receives_full_buffer_DWORD_and_actual_header_pointer(self):
        m = self.machine()
        m.run()
        entry, = [e for e in m.events if e[0]=='pi-entry']
        self.assertEqual(struct.unpack('<6H',bytes.fromhex(entry[2])),(0x23A9,m.cs,0xFFFE,0x3333,DATA['headers'],m.ds))

    def test_failed_execl_returns_through_near_cdecl_epilogue(self):
        m = self.machine()
        r = m.run(status=0xFFFF,ss=0x8000,stack=0x80)
        self.assertEqual(r['registers']['ax']&65535,0xFFFF)
        self.assertEqual((r['registers']['sp']&65535,r['registers']['cs'],r['registers']['ss']),(0x82,m.cs,0x8000))
        self.assertEqual(self.requests(m,'execl'),[[DATA['op'],m.ds,DATA['op'],m.ds,0,0]])

    def test_counter_reply_can_move_backwards_then_exit_unsigned(self):
        m = self.machine()
        r = m.run(ticks=(95,0,0xFFFF))
        self.assertEqual(r['polls'],3)
        self.assertEqual(bytes(m.u.mem_read(m.ds*16+0x144E,2)),b'\xFF\xFF')

    def test_incoming_IF_DF_and_declared_clear_DF_replies(self):
        m = self.machine()
        for clear in (False,True):
            r = m.run(flags=0xED7,clear_df=clear)
            self.assertEqual(r['flags']&0x600,0x200 if clear else 0x600)
            self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_persistent_reentry_keeps_digit_additions_and_uncleared_image_pointer(self):
        m = self.machine()
        m.run(character=21)
        r = m.run(character=21,persistent=True)
        self.assertEqual(bytes(m.u.mem_read(0x60201,2)),b'20')
        self.assertEqual((r['counts'].get('free',0),r['counts']['pi_heap']),(0,1))

    @unittest.skipUnless(REPORT.is_file(),'complete ending witness absent')
    def test_witness_refuses_partial_frames_and_enclosing_or_hardware_credit(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('ending review running')
        scope = report['scope']
        witness(scope)
        for part,key,value in (('runtime','ignored_stack_bytes',24),('runtime','executed_owner_bytes',279),
                ('runtime','actual_owned_nested_helpers',False),('runtime','physical_IRQ_graphics_exec_proved',True),
                ('runtime','interface_bodies_or_assets_owned',True),('layout','enclosing_DATA_or_other_functions_accepted',True),
                ('layout','mz_relocation_count',13),('negative_controls','count',38)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)
