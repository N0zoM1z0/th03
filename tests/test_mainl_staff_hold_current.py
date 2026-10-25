"""Whole hold controller: live nested state, normal loops and proved prefixes."""
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
from review_th03_mainl_staff_hold_work import REPORT, witness
from lib.decoded_mainl_staff_hold_layout import verify, CS, START, DATA
from lib.decoded_mainl_staff_hold_runtime import Machine, DEFAULT_SCHEDULE, STAFF, SNOW, geometry_proof

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffHoldCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def data(self,m,off,size=2):
        return int.from_bytes(m.u.mem_read(m.ds*16+off,size),'little')

    def test_complete_native_owner_has_fifteen_fields_six_calls_and_no_MZ(self):
        p = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['functions'],p['code_bytes'],len(p['ordered_native_fields']),len(p['internal_near_calls']),p['mz_relocation_count']),(1,139,15,6,0))
        self.assertEqual([f['addend'] for f in p['ordered_native_fields']].count(2),1)
        self.assertEqual(p['owners'][0]['callee_pop_bytes'],6)
        self.assertFalse(p['enclosing_DATA_or_other_functions_accepted'])

    def test_equal_corruption_cannot_replace_independent_native_ownership(self):
        def change(image):
            raw = bytearray(image.program_image)
            raw[CS*16+START] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,change(self.target),change(self.candidate),self.graph,self.files)

    def test_empty_MZ_vector_rejects_an_extra_owner_field(self):
        extra = replace(self.target.relocations[0],segment=CS,offset=START)
        bad = replace(self.target,relocations=(*self.target.relocations,extra))
        with self.assertRaisesRegex(ValueError,'empty ordered MZ'):
            verify(self.work,bad,self.candidate,self.graph,self.files)

    def test_speed_two_initializes_raw_page_and_XOR_one_not_boolean_toggle(self):
        m = self.machine()
        m.run(speed=2,page=255)
        self.assertEqual(self.data(m,DATA['centers']+255*2),262)
        self.assertEqual(self.data(m,DATA['centers']+254*2),263)
        self.assertEqual(self.data(m,DATA['centers']+2*2),0)
        self.assertEqual((self.data(m,DATA['page'],1),self.data(m,DATA['secondary_y'])),(255,262))

    def test_other_speed_initializes_fixed_pages_even_for_raw_page255(self):
        m = self.machine()
        m.run(speed=3,page=255)
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(280,280))
        self.assertEqual(self.data(m,DATA['secondary_y']),0)

    def test_height_subtraction_wraps_before_signed_enter_comparison(self):
        m = self.machine()
        m.run(height_offset=0x8000,blit_width=0,requested=0,enabled=0,secondary=0)
        self.assertEqual(self.data(m,DATA['secondary_y']),(280-0x8000)&65535)

    def test_original_three_WORD_arguments_and_exact_near_cleanup(self):
        m = self.machine()
        r = m.run(slot=0x1000,enter_measure=0x8000,hold_measure=0xFFFF,ss=0x8000,stack=0x80)
        self.assertEqual(struct.unpack('<3H',bytes(m.u.mem_read(0x8000*16+0x82,6))),(0xFFFF,0x8000,0x1000))
        self.assertEqual((r['registers']['sp']&65535,r['registers']['ss']),(0x88,0x8000))
        self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_both_phases_execute_actual_children_and_live_page_copy(self):
        m = self.machine()
        r = m.run()
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates'],r['actual_clear_WORD_callbacks']),([1,1],2,2,32000))
        self.assertEqual(sum(e[:2]==('entry','enter') for e in m.events),1)
        self.assertEqual(sum(e[:2]==('entry','clear') for e in m.events),2)
        self.assertEqual(sum(e[:2]==('entry','gate') for e in m.events),2)
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['secondary_y'])),(193,277))

    def test_no_music_actually_runs257_iterations_per_phase(self):
        m = self.machine()
        r = m.run(active=0)
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks']),('return',[257,257],514))
        self.assertEqual(r['actual_clear_WORD_callbacks'],8224000)
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['secondary_y'])),(257,180))
        self.assertFalse(any(e[0]=='pmd' for e in m.events))

    def test_clock_prefix_has_identical_full_state_after_one_and_seven_cycles(self):
        m = self.machine()
        a = m.run(clock_prefix=1,ticks=None,vsync=0)
        memory = bytes(m.u.mem_read(0,1<<20))
        b = m.run(clock_prefix=7,ticks=None,vsync=0)
        self.assertEqual((a['ending'],b['ending']),('clock-prefix','clock-prefix'))
        self.assertEqual((a['registers'],a['flags']),(b['registers'],b['flags']))
        self.assertEqual(bytes(m.u.mem_read(0,1<<20)),memory)
        self.assertEqual((b['phase_iterations'],b['ticks'],b['gates']),([0,0],1,0))

    def test_closed_enter_prefix_retains_inductive_state_without_terminal_credit(self):
        m = self.machine()
        r = m.run(loop_prefix=7,schedule=((0,(),0x8D5),))
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('enter-prefix',[7,0],7,7))
        self.assertEqual((self.data(m,DATA['frame']),self.data(m,DATA['page'],1)),(7,1))
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(268,271))
        self.assertEqual(self.data(m,DATA['secondary_y']),200)
        self.assertEqual(r['actual_clear_WORD_callbacks'],112000)

    def test_enter_prefix_rejects_changed_invariant_assumptions(self):
        m = self.machine()
        for p in (dict(cap=1),dict(vsync=2),dict(enter_measure=0),dict(persistent=True)):
            with self.subTest(p=p),self.assertRaisesRegex(ValueError,'fixture assumptions'):
                m.run(loop_prefix=3,schedule=((0,(),0x8D5),),**p)

    def test_divide_fault_keeps_outer_frame_and_no_tick_or_gate_credit(self):
        m = self.machine()
        r = m.run(duration=0)
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('divide-fault',[0,0],0,0))
        self.assertEqual((r['flag_mask'],r['registers']['sp']&65535),(0x600,0xF7F4))
        self.assertEqual(m.events[-1][:2],('divide-error',0x2885))
        self.assertEqual(m.run()['ending'],'return')

    def test_live_PMD_writes_can_trigger_second_iteration_overflow_fault(self):
        m = self.machine()
        r = m.run(schedule=((0,((STAFF['frame'],b'\0\x80'),(STAFF['duration'],b'\xF8\xFF')),0x8D5),))
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('divide-fault',[1,0],1,1))
        self.assertEqual(r['registers']['bx']&65535,65535)

    def test_PMD_192_minimum_still_requires_another_actual_iteration(self):
        m = self.machine()
        r = m.run(schedule=((0xFFFF,((STAFF['frame'],b'\xC0\0'),),0x8D5),*DEFAULT_SCHEDULE))
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates']),([2,1],3,3))

    def test_actual_rng_and_particle_lifetime_survive_phase_frame_reset(self):
        m = self.machine()
        r = m.run(cap=1)
        self.assertEqual(sum(e[:2]==('entry','rand') for e in m.events),4)
        state = 1
        for _ in range(4):
            state = (state*0x015A4E35+1)&0xFFFFFFFF
        self.assertEqual(self.data(m,SNOW['seed'],4),state)
        self.assertEqual(self.data(m,SNOW['flakes'],1),1)
        self.assertNotEqual(r['registers']['ax']>>16,0x1357^0x5AA5)

    def test_real_adaptation_reads_initial_counter_and_preserves_new_cap(self):
        m = self.machine()
        m.run(cap=255,alive='all',vsync=2)
        self.assertEqual((self.data(m,SNOW['cap'],1),self.data(m,SNOW['adapt'],1),self.data(m,STAFF['requested'],1)),(50,0,0))

    def test_actual_update_wraps_both_coordinates_inside_the_controller(self):
        m = self.machine()
        m.run(cap=1,particle0=(2,1,6271,65535,1,3))
        self.assertEqual((self.data(m,SNOW['flakes']+2),self.data(m,SNOW['flakes']+4)),(10111,1))

    def test_native_geometry_rejects_changed_backedge_or_clock_CFG(self):
        for at in (0x2C65,0x2C82,0x26C9,0x270E):
            raw = bytearray(self.target.program_image)
            raw[CS*16+at] ^= 1
            with self.subTest(at=at),self.assertRaisesRegex(ValueError,'native two-stage CFG'):
                geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_full_witness_keeps_returns_faults_and_prefixes_separate(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete hold witness absent')
        scope = json.loads(REPORT.read_text())['scope']
        witness(scope)
        for row in scope['runtime']['observations']:
            self.assertEqual(row['endings'],{'return':4891,'divide-fault':48,'clock-prefix':48,'enter-prefix':48})
        bad = deepcopy(scope)
        bad['runtime']['native_geometry_proof']['loop_prefixes_are_not_terminal_calls'] = False
        with self.assertRaises(ValueError):
            witness(bad)

    def test_witness_cannot_claim_physical_or_vector_library_ownership(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete hold witness absent')
        bad = deepcopy(json.loads(REPORT.read_text())['scope'])
        bad['runtime']['physical_driver_IRQ_assets_or_vector_library_proved'] = True
        with self.assertRaises(ValueError):
            witness(bad)


if __name__=='__main__':
    unittest.main()
