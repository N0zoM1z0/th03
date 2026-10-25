"""Whole staff callers, real nested code and native fault/unused-code bounds."""
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
from review_th03_mainl_staff_callers_work import REPORT, witness
from lib.decoded_mainl_staff_callers_layout import verify, CS, DATA
from lib.decoded_mainl_staff_callers_runtime import Machine, geometry_proof

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffCallersCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def data(self,m,name,size=2):
        return int.from_bytes(m.u.mem_read(m.ds*16+DATA[name],size),'little')

    def entries(self,m):
        return [struct.unpack('<5H',bytes.fromhex(e[3])) for e in m.events if e[:2]==('entry','dissolve')]

    def test_three_whole_native_callers_and_all_literal_fields(self):
        p = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['functions'],p['code_bytes'],len(p['ordered_native_fields']),p['mz_relocation_count'],len(p['internal_near_calls'])),(3,446,44,3,9))
        self.assertEqual([o['size'] for o in p['owners']],[211,183,52])
        self.assertEqual([o['callee_pop_bytes'] for o in p['owners']],[2,2,6])
        self.assertFalse(p['enclosing_DATA_or_other_functions_accepted'])

    def test_equal_corruption_of_unreachable_bytes_still_rejects_native_ownership(self):
        def change(image):
            raw = bytearray(image.program_image)
            raw[CS*16+0x2926] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,change(self.target),change(self.candidate),self.graph,self.files)

    def test_all_three_literal_MZ_sites_keep_their_original_order(self):
        bad = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,bad,self.candidate,self.graph,self.files)

    def test_enter_clamps_after_signed_movement(self):
        m = self.machine()
        m.run('enter',center=200,speed=100,limit=180)
        self.assertEqual(self.data(m,'centers'),180)
        self.assertEqual(self.entries(m)[-1][3],180)

    def test_enter_movement_wraps_in_WORD_before_signed_comparison(self):
        m = self.machine()
        m.run('enter',center=200,speed=0xFFFF,limit=180)
        self.assertEqual(self.data(m,'centers'),201)
        m.run('enter',center=0x8000,requested=0,secondary=0,blit_width=0)
        self.assertEqual(self.data(m,'centers'),0x8000)

    def test_all_raw_pages_address_the_unchecked_center_table(self):
        m = self.machine()
        m.run('enter',page=255)
        self.assertEqual(int.from_bytes(m.u.mem_read(m.ds*16+DATA['centers']+510,2),'little'),197)
        self.assertEqual(self.data(m,'centers'),200)
        self.assertEqual(self.data(m,'page',1),255)

    def test_enter_past_duration_only_runs_real_clear_and_keeps_alpha(self):
        m = self.machine()
        r = m.run('enter',frame=641,duration=640,enabled=255)
        self.assertEqual((r['actual_calls']['clear'],r['actual_calls']['unput'],r['actual_calls']['dissolve']),(1,0,0))
        self.assertEqual(self.data(m,'enabled',1),255)
        self.assertEqual(r['actual_clear_WORD_stores'],16000)

    def test_zero_divisor_is_actual_INT0_after_clear_unput_and_movement(self):
        m = self.machine()
        r = m.run('enter',duration=7,frame=0,enabled=255)
        self.assertTrue(r['divide_fault'])
        self.assertEqual(r['actual_calls']['dissolve'],0)
        self.assertEqual((r['flag_mask'],r['registers']['sp']&65535),(0x600,0xF7FA))
        self.assertEqual(self.data(m,'centers'),197)
        self.assertEqual(self.data(m,'enabled',1),255)
        self.assertEqual(m.events[-1][:2],('divide-error',0x2885))

    def test_overflow_fault_after_prior_fault_uses_fresh_CPU_with_exact_state(self):
        m = self.machine()
        m.run('enter',duration=7,frame=0)
        r = m.run('enter',duration=0xFFF8,frame=0x8000)
        self.assertTrue(r['divide_fault'])
        self.assertEqual((r['registers']['ax']&65535,r['registers']['bx']&65535,r['registers']['dx']&65535),(0x8000,0xFFFF,0xFFFF))
        self.assertEqual(m.events[-1][1],0x2885)

    def test_persistent_fault_preserves_memory_across_fresh_CPU(self):
        m = self.machine()
        m.run('enter',duration=7,frame=0)
        self.assertEqual(self.data(m,'centers'),197)
        r = m.run('enter',persistent=True)
        self.assertTrue(r['divide_fault'])
        self.assertEqual(self.data(m,'centers'),194)

    def test_enter_strength_WORD_overflow_precedes_lower_clamp(self):
        m = self.machine()
        m.run('enter',duration=8,frame=0x8000)
        self.assertEqual([f[1] for f in self.entries(m)],[0,0])

    def test_secondary_uses_raw_predicates_then_enables_main_alpha(self):
        m = self.machine()
        r = m.run('enter',enabled=0,requested=255,secondary=255)
        self.assertEqual([e[1] for e in m.events if e[0]=='blit-entry'],['noalpha','alpha'])
        self.assertEqual([e[2] for e in self.entries(m)],[255,0])
        self.assertEqual((r['actual_calls']['dissolve'],self.data(m,'enabled',1)),(2,0))

    def test_secondary_metadata_may_alias_live_frame_without_slot_clamp(self):
        m = self.machine()
        m.run('enter',frame=0,secondary=171)
        self.assertEqual([e[2] for e in self.entries(m)],[171,0])
        self.assertEqual(self.data(m,'frame'),0)

    def test_leave_159_moves_but_160_and161_call_box_then162_only_clears(self):
        m = self.machine()
        for frame,draw,box in ((159,2,0),(160,0,1),(161,0,1),(162,0,0)):
            r = m.run('leave',frame=frame)
            self.assertEqual((r['actual_calls']['dissolve'],r['actual_calls']['box']),(draw,box))
            self.assertEqual(r['actual_calls']['clear'],1)
            if draw:
                self.assertEqual(self.data(m,'centers'),199)

    def test_leave_negative_strength_is_passed_unsanitized(self):
        m = self.machine()
        m.run('leave',frame=(-25)&65535)
        self.assertEqual([e[1] for e in self.entries(m)],[65535,65535])

    def test_bytebox_frame_reply_and_GRCG_off_execute_in_order(self):
        m = self.machine()
        r = m.run('leave',frame=160,box_seed=0xFFAA,flags=0xED7,
                  box_writes=((DATA['enabled'],b'\xFF'),(DATA['page'],b'\xFE')))
        box, = [e for e in m.events if e[0]=='box']
        self.assertEqual(struct.unpack('<6H',bytes.fromhex(box[2])),(0x2983,m.cs,391,78,8,1))
        self.assertEqual((r['registers']['ax']&65535,r['flags']&0x600),(0xFF00,0x600))
        ports = [e for e in m.events if e[0]=='out']
        self.assertEqual([e[-1] for e in ports],[0]*5+[0x200])
        self.assertEqual((self.data(m,'enabled',1),self.data(m,'page',1)),(255,254))

    def test_gallery_draws_at160_but_skips161_without_clear(self):
        m = self.machine()
        a = m.run('gallery',frame=160)
        self.assertEqual((a['actual_calls']['clear'],a['actual_calls']['dissolve']),(0,1))
        self.assertEqual(self.entries(m)[0][1],0)
        b = m.run('gallery',frame=161,flags=0xED7)
        self.assertEqual((b['actual_calls']['clear'],b['actual_calls']['dissolve']),(0,0))
        self.assertEqual(b['flags']&0x600,0x600)

    def test_gallery_keeps_original_caller_arguments_and_pushes_mutable_copies(self):
        m = self.machine()
        m.run('gallery',left=504,top=201,slot=1)
        self.assertEqual(struct.unpack('<3H',bytes(m.u.mem_read(0x7000*16+0xF802,6))),(1,201,504))
        self.assertEqual(self.entries(m)[0][2:],(1,201,504))

    def test_clear_compaction_still_checks_every_actual_WORD_and_DF(self):
        m = self.machine()
        for flags,step in ((0x202,2),(0xED7,-2)):
            r = m.run('enter',frame=641,flags=flags)
            self.assertEqual(r['actual_clear_WORD_stores'],16000)
            rep, = [e for e in m.events if e[0]=='rep-clear']
            self.assertEqual(rep,('rep-clear',0xA8000,16000,step))
            if step<0:
                self.assertEqual(bytes(m.u.mem_read(0xB0302,2)),b'\0\0')
                self.assertEqual(bytes(m.u.mem_read(0xB7FFE,2)),b'\0\0')

    def test_compacted_clear_rejects_both_short_and_long_actual_REP(self):
        for xor in (1,255):
            raw = bytearray(self.target.program_image)
            raw[CS*16+0x256F] ^= xor
            m = Machine(replace(self.target,program_image=bytes(raw)),0x3000)
            self.addCleanup(m.close)
            with self.subTest(xor=xor),self.assertRaises(ValueError):
                m.run('enter')

    def test_owned_return_guard_rejects_cleanup_error_masked_by_parent_restore(self):
        raw = bytearray(self.target.program_image)
        raw[0xC7E*16+0x2A5] ^= 1
        m = Machine(replace(self.target,program_image=bytes(raw)),0x3000)
        self.addCleanup(m.close)
        with self.assertRaisesRegex(ValueError,'owned-return'):
            m.run('enter')

    def test_foreign_SS_small_stack_and_complete_near_cleanup(self):
        m = self.machine()
        for kind,cleanup in (('enter',4),('leave',4),('gallery',8)):
            r = m.run(kind,ss=0x8000,stack=0x80,flags=0xED7)
            self.assertEqual((r['registers']['ss'],r['registers']['sp']&65535),(0x8000,0x80+cleanup))
            self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_geometry_enumerates_fault_domains_and_proves_three_bytes_unreachable(self):
        p = geometry_proof(self.target)
        self.assertEqual((len(p['zero_divisor_duration_WORDs']),len(p['overflow_duration_WORDs'])),(15,8))
        self.assertEqual((p['complete_raw_owner_bytes'],p['executed_owner_bytes'],p['proved_unreachable_bytes']),(446,443,3))
        self.assertEqual(p['proved_unreachable_ranges'],[dict(segment=CS,offset=0x2925,size=3)])
        self.assertFalse(p['guest_iterations_skipped'])

    def test_geometry_rejects_changed_frame_gate_or_IDIV(self):
        for at in (0x28F2,0x287D,0x2923,0x256F):
            raw = bytearray(self.target.program_image)
            raw[CS*16+at] ^= 1
            with self.subTest(at=at),self.assertRaisesRegex(ValueError,'native signed division'):
                geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_bound_full_witness_keeps_returns_faults_and_unreachable_bytes_separate(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete staff caller witness absent')
        scope = json.loads(REPORT.read_text())['scope']
        witness(scope)
        for row in scope['runtime']['observations']:
            self.assertEqual((row['returned_calls'],row['native_divide_faults']),(8280,78))
            self.assertEqual(row['actual_clear_WORD_callbacks'],92416000)
        bad = deepcopy(scope)
        bad['runtime']['executed_owner_bytes'] = 446
        with self.assertRaises(ValueError):
            witness(bad)

    def test_witness_cannot_claim_box_handler_or_physical_graphics(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete staff caller witness absent')
        scope = json.loads(REPORT.read_text())['scope']
        for section,key in (('layout','enclosing_DATA_or_other_functions_accepted'),
                            ('runtime','bytebox_body_or_INT0_handler_or_physical_graphics_proved')):
            bad = deepcopy(scope)
            bad[section][key] = True
            with self.subTest(section=section),self.assertRaises(ValueError):
                witness(bad)


if __name__=='__main__':
    unittest.main()
