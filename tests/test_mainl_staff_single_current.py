"""Complete single controller: live phases, final ticks and native ABI hazards."""
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
from review_th03_mainl_staff_single_work import REPORT, witness
from lib.decoded_mainl_staff_single_layout import verify, CS, START, DATA
from lib.decoded_mainl_staff_single_runtime import Machine, DEFAULT_SCHEDULE, STAFF, SNOW, geometry_proof

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffSingleCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def data(self,m,off,size=2):
        return int.from_bytes(m.u.mem_read(m.ds*16+off,size),'little')

    def test_complete_native_owner_has_literal_fields_and_ordered_far_relocations(self):
        p = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['functions'],p['code_bytes'],len(p['ordered_native_fields']),len(p['internal_near_calls']),p['mz_relocation_count']),(1,229,21,8,6))
        self.assertEqual(sum(f['width']==4 for f in p['ordered_native_fields']),6)
        self.assertEqual(p['owners'][0]['unit_id'],'th03-mainl-decoded-staff-normal')
        self.assertFalse(p['enclosing_DATA_or_other_functions_accepted'])
        self.assertFalse(p['bytebox_library_accepted'])

    def test_equal_corruption_cannot_replace_independent_native_ownership(self):
        raw = bytearray(self.target.program_image)
        raw[CS*16+START] ^= 1
        bad = replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,bad,bad,self.graph,self.files)

    def test_reversed_MZ_order_is_rejected_even_with_identical_bytes(self):
        positions=[i for i,r in enumerate(self.target.relocations) if CS*16+START<=r.linear<CS*16+START+229]
        rows=list(self.target.relocations)
        rows[positions[0]],rows[positions[1]]=rows[positions[1]],rows[positions[0]]
        bad=replace(self.target,relocations=tuple(rows))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,bad,self.candidate,self.graph,self.files)

    def test_default_speed_also_initializes_raw_page_and_XOR_one(self):
        m = self.machine()
        m.run(page=255)
        self.assertEqual((self.data(m,DATA['centers']+510),self.data(m,DATA['centers']+508)),(277,280))
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(0,0))
        self.assertEqual((self.data(m,DATA['page'],1),self.data(m,DATA['secondary_y'])),(255,200))

    def test_speed_two_keeps_asymmetric_centers_and_restores_selected_slot(self):
        m = self.machine()
        r = m.run(speed=2,page=255,slot=1)
        self.assertEqual((self.data(m,DATA['centers']+510),self.data(m,DATA['centers']+508)),(262,263))
        self.assertEqual(r['registers']['si']&65535,(0x1357+4*0x231)&65535)
        # Tick maps raw page255 to2; leave decrements that live page.
        self.assertEqual(self.data(m,DATA['centers']+4),65535)

    def test_height_subtraction_wraps_before_signed_movement(self):
        m = self.machine()
        m.run(height_offset=0x8000,blit_width=0,requested=0,enabled=0,secondary=0)
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),((280-0x8000)&65535,(280-0x8000-1)&65535))

    def test_original_three_WORD_arguments_and_exact_near_cleanup(self):
        m = self.machine()
        r = m.run(slot=0x1000,enter_measure=0x8000,leave_measure=0xFFFF,ss=0x8000,stack=0x80)
        self.assertEqual(struct.unpack('<3H',bytes(m.u.mem_read(0x8000*16+0x82,6))),(0xFFFF,0x8000,0x1000))
        self.assertEqual((r['registers']['sp']&65535,r['registers']['ss']),(0x88,0x8000))
        self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_both_actual_children_and_two_unconditional_final_ticks(self):
        m = self.machine()
        r = m.run()
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates'],r['actual_clear_WORD_callbacks']),([1,1],4,2,32000))
        self.assertEqual(sum(e[:2]==('entry','enter') for e in m.events),1)
        self.assertEqual(sum(e[:2]==('entry','leave') for e in m.events),1)
        self.assertEqual(sum(e[0]=='box' for e in m.events),2)
        self.assertEqual(sum(e[:2]==('owned-return','off') for e in m.events),2)
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['secondary_y'])),(193,200))

    def test_no_music_executes257_iterations_per_phase_and516_ticks(self):
        m = self.machine()
        r = m.run(active=0)
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks']),('return',[257,257],516))
        self.assertEqual(r['actual_clear_WORD_callbacks'],8224000)
        self.assertEqual(sum(e[0]=='box' for e in m.events),4)
        self.assertFalse(any(e[0]=='pmd' for e in m.events))
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(257,100,100))

    def test_clock_prefix_has_identical_full_state_at_one_and_seven_cycles(self):
        m = self.machine()
        a = m.run(clock_prefix=1,ticks=None,vsync=0)
        memory=bytes(m.u.mem_read(0,1<<20))
        b = m.run(clock_prefix=7,ticks=None,vsync=0)
        self.assertEqual((a['ending'],b['ending']),('clock-prefix','clock-prefix'))
        self.assertEqual((a['registers'],a['flags']),(b['registers'],b['flags']))
        self.assertEqual(bytes(m.u.mem_read(0,1<<20)),memory)
        self.assertEqual((b['phase_iterations'],b['ticks'],b['gates']),([0,0],1,0))

    def test_closed_entrance_prefix_retains_native_state_without_terminal_credit(self):
        m=self.machine()
        r=m.run(loop_prefix=7,schedule=((0,(),0x8D5),))
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('enter-prefix',[7,0],7,7))
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(268,271))
        self.assertFalse(any(e[:2]==('entry','leave') for e in m.events))

    def test_prefix_rejects_changed_inductive_assumptions(self):
        m=self.machine()
        for p in (dict(cap=1),dict(vsync=2),dict(enter_measure=0),dict(persistent=True)):
            with self.subTest(p=p),self.assertRaisesRegex(ValueError,'fixture assumptions'):
                m.run(loop_prefix=3,schedule=((0,(),0x8D5),),**p)

    def test_divide_fault_preserves_outer_saved_SI_and_skips_ticks(self):
        m=self.machine()
        r=m.run(duration=0)
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('divide-fault',[0,0],0,0))
        self.assertEqual((r['flag_mask'],r['registers']['sp']&65535),(0x600,0xF7F2))
        self.assertEqual(m.events[-1][:2],('divide-error',0x2885))
        self.assertEqual(m.run()['ending'],'return')

    def test_live_PMD_writes_can_trigger_second_entrance_divide_overflow(self):
        m=self.machine()
        r=m.run(schedule=((0,((STAFF['frame'],b'\0\x80'),(STAFF['duration'],b'\xF8\xFF')),0x8D5),))
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('divide-fault',[1,0],1,1))

    def test_gate192_minimum_and_leave_backedge_execute_actual_extra_iterations(self):
        m=self.machine()
        r=m.run(schedule=((0xFFFF,((STAFF['frame'],b'\xC0\0'),),0x8D5),*DEFAULT_SCHEDULE))
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates']),([2,1],5,3))
        r=m.run(schedule=(*DEFAULT_SCHEDULE,(0,((STAFF['frame'],b'\xC1\0'),),0x8D5),*DEFAULT_SCHEDULE))
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates']),([1,2],5,3))

    def test_particle_rng_lifetime_and_actual_ticks_survive_both_phases_and_tail(self):
        m=self.machine()
        r=m.run(cap=1)
        self.assertEqual(sum(e[:2]==('entry','rand') for e in m.events),4)
        state=1
        for _ in range(4):state=(state*0x015A4E35+1)&0xFFFFFFFF
        self.assertEqual(self.data(m,SNOW['seed'],4),state)
        self.assertEqual(self.data(m,SNOW['flakes'],1),1)
        self.assertNotEqual(r['registers']['ax']>>16,0x1357^0x5AA5)

    def test_capacity82_retains_live_aliases_without_clamping_or_geometry_normalization(self):
        m=self.machine()
        r=m.run(cap=82,secondary=0,requested=0,enabled=0,blit_width=0)
        self.assertEqual((r['phase_iterations'],r['ticks']),([1,1],4))
        self.assertEqual(self.data(m,SNOW['cap'],1),82)
        # Particle80/81 overwrite FRAME/PAGE and secondary state even after
        # PMD has written frame193. Zero graphics width bounds only the fixture.
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['page'],1),self.data(m,STAFF['secondary'],1)),(1,128,93))

    def test_unowned_box_reply_writes_and_registers_are_live_before_final_ticks(self):
        m=self.machine()
        m.run(box_seed=0x0123,box_writes=((DATA['secondary_y'],b'\x56\x34'),))
        self.assertEqual(self.data(m,DATA['secondary_y']),0x3456)
        self.assertEqual(sum(e[0]=='box-write' for e in m.events),2)
        self.assertEqual(sum(e[:2]==('owned-return','color') for e in m.events),2)

    def test_native_proof_binds_both_backedges_and_unreachable_leave_clamp(self):
        p=geometry_proof(self.target)
        self.assertEqual((p['leave_unreachable_bytes'],p['leave_unreachable_range']),(3,[0x2925,0x2928]))
        for at in (0x2A3A,0x2A58,0x2920,0x270E):
            raw=bytearray(self.target.program_image)
            raw[CS*16+at]^=1
            with self.subTest(at=at),self.assertRaises(ValueError):
                geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_full_witness_keeps_unreachable_context_and_waiting_classes_separate(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete single witness absent')
        scope=json.loads(REPORT.read_text())['scope']
        witness(scope)
        for row in scope['runtime']['observations']:
            self.assertEqual(row['endings'],{'return':4891,'divide-fault':48,'clock-prefix':48,'enter-prefix':48})
        bad=deepcopy(scope)
        bad['runtime']['proved_unreachable_context_bytes']=0
        with self.assertRaises(ValueError):witness(bad)

    def test_witness_cannot_claim_bytebox_library_or_physical_behavior(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete single witness absent')
        bad=deepcopy(json.loads(REPORT.read_text())['scope'])
        bad['layout']['bytebox_library_accepted']=True
        with self.assertRaises(ValueError):witness(bad)


if __name__=='__main__':
    unittest.main()
