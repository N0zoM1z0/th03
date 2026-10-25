"""Whole paired controller: live secondary state, WORD wrap and native ABI."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import struct
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_mainl_sound_work import images
from review_th03_mainl_staff_pair_work import REPORT,witness
from lib.decoded_mainl_staff_pair_layout import verify,CS,START,DATA
from lib.decoded_mainl_staff_pair_runtime import Machine,DEFAULT_SCHEDULE,STAFF,SNOW,geometry_proof,exit_schedule

WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class StaffPairCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files=images(ROOT)

    def machine(self):
        m=Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def data(self,m,off,size=2):
        return int.from_bytes(m.u.mem_read(m.ds*16+off,size),'little')

    def dissolve_frames(self,m):
        return [struct.unpack('<5H',bytes.fromhex(e[-1])) for e in m.events if e[:2]==('entry','dissolve')]

    def test_complete_native_fields_order_and_natural_producer(self):
        p=verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((p['functions'],p['code_bytes'],len(p['ordered_native_fields']),len(p['internal_near_calls']),p['mz_relocation_count']),(1,358,34,11,9))
        self.assertEqual([f['addend'] for f in p['ordered_native_fields']].count(2),1)
        self.assertEqual(p['owners'][0]['unit_id'],'th03-mainl-decoded-staff-double')
        self.assertEqual((p['enclosing_CODE_bytes'],p['enclosing_initialized_DATA_bytes'],p['enclosing_BSS_bytes']),(3695,224,0))
        self.assertFalse(p['enclosing_DATA_or_other_functions_accepted'])
        self.assertFalse(p['bytebox_library_accepted'])

    def test_equal_image_corruption_cannot_replace_independent_native_bytes(self):
        raw=bytearray(self.target.program_image)
        raw[CS*16+START]^=1
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native'):
            verify(self.work,bad,bad,self.graph,self.files)

    def test_literal_MZ_order_cannot_be_replaced_by_membership(self):
        positions=[i for i,r in enumerate(self.target.relocations) if CS*16+START<=r.linear<CS*16+START+358]
        rows=list(self.target.relocations)
        rows[positions[0]],rows[positions[1]]=rows[positions[1]],rows[positions[0]]
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,replace(self.target,relocations=tuple(rows)),self.candidate,self.graph,self.files)

    def test_default_speed_initializes_fixed_pages_with_raw_page255(self):
        m=self.machine()
        m.run(page=255)
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2)),(280,280))
        self.assertEqual((self.data(m,DATA['centers']+510),self.data(m,DATA['centers']+508)),(0,0))
        self.assertEqual((self.data(m,DATA['centers']+4),self.data(m,DATA['page'],1)),(65535,255))
        self.assertEqual(self.data(m,DATA['secondary_y']),200)

    def test_speed_two_uses_raw_page_XOR_one_and_tick_uses_one_minus_page(self):
        m=self.machine()
        m.run(speed=2,page=255)
        self.assertEqual((self.data(m,DATA['centers']+510),self.data(m,DATA['centers']+508)),(262,263))
        self.assertEqual((self.data(m,DATA['centers']+4),self.data(m,DATA['page'],1)),(65535,255))

    def test_selected_slot_minus_one_wraps_as_WORD_before_metadata_lookup(self):
        m=self.machine()
        m.run(slot=0,secondary=0,requested=0,enabled=0,blit_width=0)
        paired=[f for f in self.dissolve_frames(m) if f[0] in (0x2B05,0x2B81)]
        self.assertEqual([f[2] for f in paired],[65535,65535])
        self.assertEqual([f[4] for f in paired],[320,320])

    def test_force_alpha_draws_slot_minus_one_even_when_secondary_is_disabled(self):
        m=self.machine()
        m.run(secondary=0,requested=1,enabled=0)
        paired=[f for f in self.dissolve_frames(m) if f[0] in (0x2B05,0x2B81)]
        self.assertEqual(paired,[(0x2B05,0,0,200,320),(0x2B81,0,0,200,320)])
        self.assertEqual(sum(e[:2]==('blit-entry','alpha') for e in m.events),2)
        self.assertEqual(sum(e[:2]==('blit-entry','noalpha') for e in m.events),2)
        self.assertEqual(self.data(m,DATA['enabled'],1),0)

    def test_requested_zero_still_draws_pair_but_selects_noalpha(self):
        m=self.machine()
        m.run(secondary=0,requested=0,enabled=0)
        paired=[f for f in self.dissolve_frames(m) if f[0] in (0x2B05,0x2B81)]
        self.assertEqual([f[2] for f in paired],[0,0])
        self.assertEqual(sum(e[:2]==('blit-entry','alpha') for e in m.events),0)
        self.assertEqual(sum(e[:2]==('blit-entry','noalpha') for e in m.events),4)
        self.assertEqual(self.data(m,DATA['enabled'],1),0)

    def test_saved_SI_DI_and_original_Pascal_arguments_survive_foreign_stack(self):
        m=self.machine()
        r=m.run(slot=0x1000,enter_measure=0x8000,leave_measure=0xFFFF,ss=0x8000,stack=0x80)
        self.assertEqual(struct.unpack('<3H',bytes(m.u.mem_read(0x8000*16+0x82,6))),(65535,0x8000,0x1000))
        self.assertEqual((r['registers']['sp']&65535,r['registers']['ss']),(0x88,0x8000))
        self.assertEqual((r['registers']['si']&65535,r['registers']['di']&65535),((0x1357+4*0x231)&65535,(0x1357+5*0x231)&65535))
        self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))

    def test_two_actual_phases_and_two_unconditional_final_ticks(self):
        m=self.machine()
        r=m.run()
        self.assertEqual((r['phase_iterations'],r['ticks'],r['gates'],r['actual_clear_WORD_callbacks']),([1,1],4,2,32000))
        self.assertEqual(sum(e[:2]==('entry','enter') for e in m.events),1)
        self.assertEqual(sum(e[:2]==('entry','leave') for e in m.events),1)
        self.assertEqual(sum(e[0]=='box' for e in m.events),2)
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2),self.data(m,DATA['secondary_y'])),(277,279,200))

    def test_no_music_executes516_ticks_and_both_reachable_clamps(self):
        m=self.machine()
        r=m.run(active=0)
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks']),('return',[257,257],516))
        self.assertEqual(r['actual_clear_WORD_callbacks'],8224000)
        self.assertEqual(sum(e[0]=='box' for e in m.events),6)
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2),self.data(m,DATA['secondary_y'])),(100,100,119))
        self.assertTrue(set(range(CS*16+0x2B57,CS*16+0x2B5A))<=m.covered)
        self.assertFalse(set(range(CS*16+0x2925,CS*16+0x2928))&m.covered)
        self.assertFalse(any(e[0]=='pmd' for e in m.events))

    def test_frame161_reaches_pair_clamp_with_pre_clamp_AX8(self):
        m=self.machine()
        m.run(schedule=exit_schedule(161))
        entries=[e for e in m.events if e[0]=='color-entry' and int.from_bytes(bytes.fromhex(e[2])[:2],'little')==0x2B8E]
        self.assertEqual(len(entries),1)
        self.assertEqual((entries[0][1]['ax']&65535,entries[0][1]['di']&65535),(8,7))
        self.assertEqual(self.data(m,DATA['secondary_y']),199)

    def test_frame8000_wraps_DEC_before_IDIV_and_draws_strength7(self):
        m=self.machine()
        m.run(schedule=exit_schedule(0x8000),flags=0xED7,ss=0x8000,stack=0x80)
        paired=[f for f in self.dissolve_frames(m) if f[0]==0x2B81]
        self.assertEqual([f[1] for f in paired],[0,7])
        self.assertTrue(set(range(CS*16+0x2B57,CS*16+0x2B5A))<=m.covered)
        self.assertEqual(self.data(m,DATA['secondary_y']),199)

    def test_skip_unput_and_shared_alpha_epilogue_do_not_invent_owned_returns(self):
        m=self.machine()
        r=m.run(schedule=exit_schedule(162))
        unput=[e for e in m.events if e[:2]==('entry','unput')]
        self.assertEqual((r['phase_iterations'],len(unput)),([1,2],3))
        self.assertEqual(sum(e[:2]==('owned-return','unput') for e in m.events),3)
        self.assertEqual(self.data(m,DATA['secondary_y']),200)

    def test_bytebox_frame_write_is_reloaded_before_second_live_predicate(self):
        m=self.machine()
        m.run(schedule=exit_schedule(160),box_writes=((DATA['frame'],b'\0\0'),))
        paired=[f for f in self.dissolve_frames(m) if f[0]==0x2B81]
        self.assertEqual([f[1] for f in paired],[0,0])
        self.assertEqual(sum(e[0]=='box' for e in m.events),3)
        self.assertEqual(self.data(m,DATA['secondary_y']),199)

    def test_bytebox_can_skip_second_predicate_and_preserve_raw_alpha_state(self):
        m=self.machine()
        m.run(schedule=exit_schedule(160),box_writes=((DATA['frame'],b'\xA2\0'),(DATA['enabled'],b'\x07')))
        self.assertEqual(len([f for f in self.dissolve_frames(m) if f[0]==0x2B81]),1)
        self.assertEqual(self.data(m,DATA['enabled'],1),7)
        self.assertEqual(self.data(m,DATA['secondary_y']),200)

    def test_secondary_y_is_a_wrapping_WORD_in_the_explicit_interface_fixture(self):
        m=self.machine()
        m.run(secondary_y=0,secondary=0,requested=0,enabled=0,blit_width=0,schedule=exit_schedule(161))
        self.assertEqual(self.data(m,DATA['secondary_y']),65535)

    def test_closed_enter_prefix_keeps_secondary_y_immutable(self):
        m=self.machine()
        r=m.run(loop_prefix=7,schedule=((0,(),0x8D5),))
        self.assertEqual((r['ending'],r['phase_iterations'],r['ticks'],r['gates']),('enter-prefix',[7,0],7,7))
        self.assertEqual((self.data(m,DATA['centers']),self.data(m,DATA['centers']+2),self.data(m,DATA['secondary_y'])),(268,271,200))
        self.assertEqual(len([f for f in self.dissolve_frames(m) if f[0]==0x2B05]),7)
        with self.assertRaisesRegex(ValueError,'fixture assumptions'):
            m.run(loop_prefix=3,schedule=((0,(),0x8D5),),secondary_y=201)

    def test_readonly_clock_prefix_retains_identical_complete_state(self):
        m=self.machine()
        a=m.run(clock_prefix=1,ticks=None,vsync=0)
        memory=bytes(m.u.mem_read(0,1<<20))
        b=m.run(clock_prefix=7,ticks=None,vsync=0)
        self.assertEqual((a['ending'],b['ending']),('clock-prefix','clock-prefix'))
        self.assertEqual((a['registers'],a['flags']),(b['registers'],b['flags']))
        self.assertEqual(bytes(m.u.mem_read(0,1<<20)),memory)
        self.assertEqual((b['ticks'],b['gates']),(1,0))

    def test_native_divide_fault_keeps_both_outer_saved_registers(self):
        m=self.machine()
        r=m.run(duration=0)
        self.assertEqual((r['ending'],r['ticks'],r['gates'],r['flag_mask']),('divide-fault',0,0,0x600))
        self.assertEqual(r['registers']['sp']&65535,0xF7F0)
        self.assertEqual(m.events[-1][:2],('divide-error',0x2885))
        self.assertEqual(m.run()['ending'],'return')

    def test_capacity82_retains_particle80_81_aliases(self):
        m=self.machine()
        r=m.run(cap=82,secondary=0,requested=0,enabled=0,blit_width=0)
        self.assertEqual((r['phase_iterations'],r['ticks']),([1,1],4))
        self.assertEqual((self.data(m,SNOW['cap'],1),self.data(m,DATA['frame']),self.data(m,DATA['page'],1),self.data(m,STAFF['secondary'],1)),(82,1,128,93))

    def test_entire_WORD_domain_proves_two_pair_clamps_and_safe_signed_quotients(self):
        p=geometry_proof(self.target)
        self.assertEqual(p['pair_clamp_frame_WORDs'],[161,32768])
        self.assertEqual((p['pair_IDIV_quotient_range'],p['pair_strength_range']),([-1638,1638],[-1638,7]))
        for at in (0x2B49,0x2B4D,0x2B54,0x2B1C,0x2BBB):
            raw=bytearray(self.target.program_image)
            raw[CS*16+at]^=1
            with self.subTest(at=at),self.assertRaises(ValueError):
                geometry_proof(replace(self.target,program_image=bytes(raw)))

    def test_full_witness_keeps_unreachable_leave_and_reachable_pair_clamps_separate(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete pair witness absent')
        scope=json.loads(REPORT.read_text())['scope']
        witness(scope)
        for row in scope['runtime']['observations']:
            self.assertEqual(row['endings'],{'return':5953,'divide-fault':48,'clock-prefix':48,'enter-prefix':48})
        bad=deepcopy(scope)
        bad['runtime']['native_geometry_proof']['pair_clamp_frame_WORDs']=[]
        with self.assertRaises(ValueError):witness(bad)

    def test_witness_cannot_promote_bytebox_or_unowned_vector_library(self):
        if not REPORT.is_file() or not json.loads(REPORT.read_text()).get('complete'):
            self.skipTest('complete pair witness absent')
        scope=json.loads(REPORT.read_text())['scope']
        for field in ('bytebox_library_accepted','physical_IRQ_driver_assets_or_vector_library_accepted'):
            bad=deepcopy(scope)
            bad['layout'][field]=True
            with self.subTest(field=field),self.assertRaises(ValueError):witness(bad)


if __name__=='__main__':
    unittest.main()
