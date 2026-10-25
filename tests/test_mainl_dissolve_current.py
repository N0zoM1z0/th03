"""Natural dissolve owner, actual nested SMC and complete caller memory."""
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
from review_th03_mainl_dissolve_work import REPORT, witness
from lib.decoded_mainl_dissolve_layout import verify, CS, DATA, START
from lib.decoded_mainl_dissolve_runtime import Machine, PATTERNS, geometry_proof

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class DissolveCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def args(self,m,stack=0xF800,ss=0x7000):
        return struct.unpack('<4H',bytes(m.u.mem_read(ss*16+stack+2,8)))

    def test_complete_native_body_has_seven_fields_two_ordered_MZs(self):
        p = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['functions'],p['code_bytes'],len(p['ordered_native_fields']),p['mz_relocation_count']),(1,211,7,2))
        self.assertEqual([f['addend'] for f in p['ordered_native_fields']],[0,0,4,2,68,0,0])
        owner, = p['owners']
        self.assertEqual((owner['argument_bytes'],owner['callee_pop_bytes'],owner['private_data_bytes']),(8,8,0))
        self.assertFalse(p['enclosing_DATA_or_other_functions_accepted'])

    def test_equal_corruption_is_not_native_source_ownership(self):
        def change(image):
            raw = bytearray(image.program_image)
            raw[CS*16+START] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,change(self.target),change(self.candidate),self.graph,self.files)

    def test_literal_MZ_order_is_required(self):
        bad = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,bad,self.candidate,self.graph,self.files)

    def test_negative_pixel_dimensions_center_toward_zero_in_real_caller_WORDs(self):
        m = self.machine()
        m.run(width=0x8001,height=0xFFFF,blit_width=0,strength=0)
        self.assertEqual(self.args(m),(0,0,200,320+16383))

    def test_strength_is_masked_in_the_actual_caller_frame(self):
        m = self.machine()
        a = m.run(strength=0xFFFF)
        self.assertEqual(self.args(m),(7,0,200,304))
        self.assertEqual(a['summary']['WORD_stores'],2)
        b = m.run(strength=0x8000)
        self.assertEqual(self.args(m)[0],0)
        self.assertEqual(b['summary']['WORD_stores'],0)

    def test_alpha_selection_uses_both_raw_BYTE_flags(self):
        m = self.machine()
        for enabled,requested,kind in ((0,255,'noalpha'),(255,0,'noalpha'),(128,255,'alpha')):
            with self.subTest(enabled=enabled,requested=requested):
                r = m.run(enabled=enabled,requested=requested)
                self.assertEqual(r['summary']['blitter'],kind)

    def test_actual_alpha_and_color_frames_execute_with_all_six_OUTs(self):
        m = self.machine()
        r = m.run(enabled=255,flags=0xED7)
        entry, = [e for e in m.events if e[:2]==('blit-entry','alpha')]
        self.assertEqual(struct.unpack('<5H',bytes.fromhex(entry[3])),(0x2793,m.cs,0,200,304))
        self.assertEqual(sum(e[0]=='color-entry' for e in m.events),1)
        self.assertEqual(len([e for e in m.events if e[0]=='out']),6)
        self.assertEqual(r['stack_depth'],38)
        self.assertEqual(r['flags']&0x600,0x200)  # Actual blitter CLD.

    def test_actual_noalpha_return_frame_and_SMC_are_present(self):
        m = self.machine()
        r = m.run(enabled=0,blit_width=3)
        entry, = [e for e in m.events if e[:2]==('blit-entry','noalpha')]
        self.assertEqual(struct.unpack('<5H',bytes.fromhex(entry[3])),(0x2783,m.cs,0,200,304))
        at = (m.load+0xC7E)*16+0xF32+71
        self.assertEqual(int.from_bytes(m.u.mem_read(at,2),'little'),3)
        self.assertEqual(r['stack_depth'],30)
        self.assertFalse(any(e[0]=='out' for e in m.events))

    def test_pattern_selects_strength_and_low_two_row_bits(self):
        m = self.machine()
        for phase in range(4):
            r = m.run(width=16,height=1,top=phase,blit_width=0,strength=5)
            writes = [e for e in m.events if e[0]=='store' and 0xE0000<=e[1]<0xF0001]
            self.assertEqual(len(writes),1)
            _,at,size,value = writes[0]
            initial = int.from_bytes(m.initial[at:at+size],'little')
            self.assertEqual(value,initial&(~PATTERNS[20+phase]&65535))
            self.assertEqual(r['summary']['rows'],1)

    def test_zero_inner_count_actually_executes65536_WORDs(self):
        m = self.machine()
        r = m.run(width=15,height=1,top=0,blit_width=0)
        self.assertEqual((r['summary']['rows'],r['summary']['WORD_stores']),(1,65536))
        writes = [e for e in m.events if e[0]=='store' and 0xE0000<=e[1]<0xF0001]
        self.assertEqual(writes[32768],writes[0])

    def test_signed_IDIV_width_differs_from_unsigned_shift(self):
        m = self.machine()
        r = m.run(width=0x8001,height=1,top=0,blit_width=0)
        self.assertEqual(r['summary']['WORD_stores'],63489)

    def test_wrapped_unsigned_row_bound_is_not_signed_or_pretested(self):
        m = self.machine()
        r = m.run(width=16,height=3,top=0,blit_width=0)
        self.assertEqual(r['summary']['rows'],3)  # adjusted topFFFF,end2.
        self.assertEqual(r['registers']['dx']&65535,2)
        r = m.run(width=16,height=0,top=0,blit_width=0)
        self.assertEqual(r['summary']['rows'],1)

    def test_WORD_at_FFFF_spans_physical_bytes(self):
        m = self.machine()
        m.run(width=16,height=1,left=0,top=0,blit_width=0)
        writes = [e for e in m.events if e[0]=='store' and 0xE0000<=e[1]<0xF0001]
        self.assertEqual(writes[0][1:3],(0xEFFFF,2))
        self.assertEqual(bytes(m.u.mem_read(0xEFFFF,2)),writes[0][3].to_bytes(2,'little'))

    def test_slot_shift_wraps_with_full_unsanitized_argument_WORD(self):
        m = self.machine()
        m.run(slot=0x1000)
        entry, = [e for e in m.events if e[0]=='blit-entry']
        self.assertEqual(struct.unpack('<5H',bytes.fromhex(entry[3]))[2],0x1000)
        self.assertEqual(self.args(m)[1],0x1000)

    def test_foreign_SS_and_small_stack_keep_all_caller_bytes(self):
        m = self.machine()
        r = m.run(ss=0x8000,stack=0x80,enabled=1,flags=0xED7)
        self.assertEqual((r['registers']['ss'],r['registers']['sp']&65535),(0x8000,0x8A))
        self.assertEqual(self.args(m,0x80,0x8000),(3,0,200,304))
        self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_actual_DWORD_blitter_result_survives_outer_WORD_code(self):
        m = self.machine()
        r = m.run(enabled=1,strength=0)
        self.assertNotEqual(r['registers']['ax']>>16,0x1357^0x5AA5)
        self.assertEqual(r['summary']['blitter_summary']['SMC_WORD_writes'],5)

    def test_reentry_keeps_actual_SMC_and_prior_graph_memory(self):
        m = self.machine()
        a = m.run(enabled=1)
        b = m.run(enabled=1,persistent=True)
        self.assertEqual(a['registers'],b['registers'])
        self.assertEqual(a['summary'],b['summary'])

    def test_geometry_rejects_signed_row_branch_and_changed_LOOP(self):
        for at,xor in ((0x27FC,0x0E),(0x27F2,1),(0x27A4,8)):
            raw = bytearray(self.target.program_image)
            raw[CS*16+at] ^= xor
            with self.subTest(at=at),self.assertRaisesRegex(ValueError,'finite CFG'):
                geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_full_report_separates_executed_maxima_from_combined_bound(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete dissolve witness absent')
        scope = json.loads(REPORT.read_text())['scope']
        witness(scope)
        self.assertFalse(scope['runtime']['native_geometry_proof']['maximum_combined_case_executed'])
        for row in scope['runtime']['observations']:
            self.assertEqual((row['maximum_rows'],row['maximum_inner_iterations']),(65536,65536))
            self.assertEqual(row['maximum_WORD_stores'],65536)

    def test_report_cannot_grant_unowned_pattern_or_hardware_credit(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete dissolve witness absent')
        scope = json.loads(REPORT.read_text())['scope']
        for section,key in (('layout','enclosing_DATA_or_other_functions_accepted'),
                            ('runtime','external_patterns_or_slots_owned'),
                            ('runtime','physical_planar_pixels_or_timing_proved')):
            bad = deepcopy(scope)
            bad[section][key] = True
            with self.subTest(key=key),self.assertRaises(ValueError):
                witness(bad)


if __name__=='__main__':
    unittest.main()
