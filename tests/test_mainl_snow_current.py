"""Whole live snow cluster, real nested code and conditional closed polling."""
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
from review_th03_mainl_snow_work import REPORT, witness
from lib.decoded_mainl_snow_layout import verify, CS, DATA, START
from lib.decoded_mainl_snow_runtime import Machine, CONTEXT, geometry_proof, seed_for_first_output, signed

WORK = ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'


@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class SnowCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files = images(ROOT)

    def machine(self):
        m = Machine(self.target,0x3000)
        self.addCleanup(m.close)
        return m

    def data(self,m,name,size=2):
        return int.from_bytes(m.u.mem_read(m.ds*16+DATA[name],size),'little')

    def particle(self,m,index=0):
        return struct.unpack('<BB5H4B',bytes(m.u.mem_read(m.ds*16+DATA['flakes']+index*16,16)))

    def test_one_extent_contains_seven_whole_native_procedures(self):
        r = verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['extents'],r['functions'],r['code_bytes'],len(r['ordered_native_fields']),r['mz_relocation_count']),(1,7,464,27,6))
        self.assertEqual(sum(p['size'] for p in r['procedures']),464)
        self.assertEqual(r['owners'][0]['procedure_count'],7)
        self.assertEqual([p['callee_pop_bytes'] for p in r['procedures']],[0,0,0,0,0,4,0])
        self.assertFalse(r['library_vector_or_tables_accepted'])

    def test_equal_corruption_is_not_native_ownership(self):
        def changed(image):
            raw = bytearray(image.program_image)
            raw[CS*16+START] ^= 1
            return replace(image,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'independently linked native snow'):
            verify(self.work,changed(self.target),changed(self.candidate),self.graph,self.files)

    def test_all_six_MZ_fields_preserve_literal_order(self):
        changed = replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ'):
            verify(self.work,changed,self.candidate,self.graph,self.files)

    def test_clear_inherits_DF_and_executes_all16000_WORD_stores(self):
        m = self.machine()
        for flags,second in ((0x202,0xA8002),(0xED7,0xB7FFE)):
            r = m.run('clear',flags=flags)
            stores = [e for e in m.events if e[0]=='store' and 0xA8000<=e[1]<0xB8002]
            self.assertEqual(len(stores),16000)
            self.assertEqual([e[1] for e in stores[:2]],[0xA8000,second])
            self.assertEqual((r['stack_depth'],r['flags']&0x600),(4,flags&0x600))

    def test_reset_changes_exactly80_alive_BYTES_regardless_of_capacity(self):
        m = self.machine()
        m.run('reset',cap=255,alive='all',frame=0x03FF)
        stores = [e for e in m.events if e[0]=='store' and m.ds*16+DATA['flakes']<=e[1]<m.ds*16+DATA['flakes']+255*16]
        self.assertEqual(stores,[('store',m.ds*16+DATA['flakes']+i*16,1,0) for i in range(80)])
        self.assertEqual(self.particle(m)[1],0x71)
        self.assertEqual(self.data(m,'frame'),0x03FF)
        self.assertEqual(self.data(m,'cap',1),255)

    def test_spawn_executes_four_real_RNG_calls_and_real_vector(self):
        m = self.machine()
        r = m.run('spawn',cap=1,frame=0,alive='none',table='zero',random_seed=1)
        self.assertEqual((r['calls']['rand'],r['calls']['vector'],r['stack_depth']),(4,1,28))
        p = self.particle(m)
        self.assertEqual(p[:7],(1,0x71,10112,346,0,0,2))
        expected = 1
        for _ in range(4):
            expected = (expected*0x015A4E35+1)&0xFFFFFFFF
        self.assertEqual(r['final_seed'],expected)

    def test_real_vector_frame_keeps_unsanitized_high_angle_BYTE(self):
        m = self.machine()
        m.run('spawn',cap=1,frame=0,alive='none',random_seed=1)
        vector, = [e for e in m.events if e[:2]==('entry','vector')]
        frame = struct.unpack('<8H',bytes.fromhex(vector[3]))
        self.assertEqual(frame,(0x2626,m.cs,86,0x7D52,DATA['flakes']+8,m.ds,DATA['flakes']+6,m.ds))

    def test_odd_particle_spawns_from_top_using_the_other_modulus(self):
        m = self.machine()
        r = m.run('spawn',cap=2,frame=8,alive='none',particle0=(1,0,0,0,0,0),table='zero')
        self.assertEqual(r['calls']['rand'],4)
        self.assertEqual(self.particle(m,1)[2:4],(346,0))
        r = m.run('spawn',cap=2,frame=7,alive='none',particle0=(1,0,0,0,0,0))
        self.assertNotIn('rand',r['calls'])

    def test_all_masked_RNG_outputs_have_real_boundary_fixture(self):
        m = self.machine()
        m.run('spawn',cap=1,frame=0,alive='none',random_seed=seed_for_first_output(32767),table='zero')
        self.assertEqual(self.particle(m)[3],32767%6272)

    def test_vector_DWORD_high_halves_survive_the_outer_WORD_loop(self):
        m = self.machine()
        r = m.run('spawn',cap=1,frame=0,alive='none',table='signed')
        angle,length = 82,86
        sine = signed(((angle*3187)^0xA55A)&65535)
        cosine = signed((((angle+64)*3187)^0xA55A)&65535)
        self.assertEqual(r['registers']['cx'],sine&0xFFFFFFFF)
        self.assertEqual(r['registers']['dx'],cosine&0xFFFFFFFF)
        self.assertEqual(r['registers']['ax'],(((length*sine)>>8)&0xFFFF0000)|1)

    def test_update_normalizes_alive_BYTE_and_preserves_padding(self):
        m = self.machine()
        m.run('update',cap=1,particle0=(255,160,320,0xFFFF,31,3))
        p = self.particle(m)
        self.assertEqual(p,(1,0x71,159,351,0xFFFF,31,3,1,2,3,4))

    def test_update_wraps_once_with_signed_WORD_comparisons(self):
        m = self.machine()
        m.run('update',cap=1,particle0=(2,(-10113)&65535,0xFFFF,0,0,0))
        self.assertEqual(self.particle(m)[2:4],(0xFFFF,0xFFFF))
        m.run('update',cap=1,particle0=(2,0x7FFF,0x7FFF,1,1,0))
        self.assertEqual(self.particle(m)[2:4],((0x8000+10112)&65535,0x8000))

    def test_capacity81_live_alias_changes_frame_and_raw_page_ports(self):
        m = self.machine()
        a = m.run('tick',cap=80,frame=0x03FF,alive='all',vsync=2)
        self.assertEqual((a['calls']['flake'],self.data(m,'frame')),(80,0x03FF))
        b = m.run('tick',cap=81,frame=0x03FF,alive='all',vsync=2)
        self.assertEqual((b['calls']['flake'],self.data(m,'frame')),(81,0x0301))
        self.assertEqual((self.data(m,'cap',1),self.data(m,'page',1),self.data(m,'slow',1),self.data(m,'adapt',1)),(50,0x12,0,0))
        self.assertEqual([(e[1],e[3]) for e in m.events if e[0]=='out'],[(0xA4,0xEF),(0xA6,0x12)])

    def test_all255_particles_are_really_visited_without_array_clamping(self):
        m = self.machine()
        r = m.run('spawn',cap=255,frame=0x7F00,alive='none',table='signed')
        self.assertEqual((r['calls']['rand'],r['calls']['vector']),(1020,255))
        self.assertEqual(self.data(m,'cap',1),255)
        self.assertEqual(self.particle(m,254)[0],1)

    def test_gate_uses_signed_frames_and_unsigned_music_measure(self):
        m = self.machine()
        self.assertEqual(m.run('gate',frame=0,frames=0x8000)['registers']['ax']&65535,1)
        self.assertEqual(m.run('gate',frame=0x8000,frames=0x7FFF)['registers']['ax']&65535,0)
        self.assertEqual(m.run('gate',active=255,frame=193,measure=0x7FFF,pmd_measure=0x8000)['registers']['ax']&65535,1)
        self.assertEqual(m.run('gate',active=255,frame=0x7FFF,measure=0x8000,pmd_measure=0x7FFF)['registers']['ax']&65535,0)

    def test_PMD_request_retains_AL_and_reload_observes_reply_memory(self):
        m = self.machine()
        r = m.run('gate',active=1,frame=0,pmd_writes=((DATA['frame'],b'\xC1\0'),))
        request, = [e for e in m.events if e[0]=='pmd']
        self.assertEqual((request[1],request[2]['ax']&65535),(0x60,0x0557))
        self.assertEqual(r['registers']['ax']&65535,1)

    def test_tick_composes_actual_owned_RNG_and_flake_on_one_UC(self):
        m = self.machine()
        r = m.run('tick',cap=2,frame=8,alive='none',table='signed')
        for kind in ('spawn','update','render'):
            self.assertEqual(r['calls'][kind],1)
        self.assertEqual((r['calls']['rand'],r['calls']['vector'],r['calls']['flake'],r['stack_depth']),(8,2,2,32))
        context = {at for s,a,n,_ in CONTEXT.values() for at in range(s*16+a,s*16+a+n)}
        self.assertEqual(len(context),187)
        self.assertTrue(context<=m.covered)

    def test_adaptation_follows_render_and_persists_into_next_entry(self):
        m = self.machine()
        a = m.run('tick',cap=4,alive='all',vsync=2)
        self.assertEqual(a['calls']['flake'],4)
        self.assertEqual((self.data(m,'cap',1),self.data(m,'adapt',1),self.data(m,'page',1)),(50,0,1))
        b = m.run('tick',persistent=True)
        self.assertEqual((b['calls']['flake'],self.data(m,'cap',1),self.data(m,'page',1)),(50,50,0))

    def test_late_clock_update_does_not_retroactively_enable_adaptation(self):
        m = self.machine()
        r = m.run('tick',cap=4,alive='all',vsync=0,ticks=(0,2),adapt=1)
        self.assertEqual(r['polls'],2)
        self.assertEqual((self.data(m,'cap',1),self.data(m,'adapt',1),self.data(m,'vsync')),(4,1,0))

    def test_readonly_zero_prefix_is_a_full_state_closed_cycle(self):
        m = self.machine()
        a = m.run('tick',cap=0,vsync=0,ticks=None,prefix=1,flags=0xED7,ss=0x8000,stack=0x80)
        first = bytes(m.u.mem_read(0,1<<20))
        b = m.run('tick',cap=0,vsync=0,ticks=None,prefix=7,flags=0xED7,ss=0x8000,stack=0x80)
        self.assertEqual((a['registers'],a['flags']),(b['registers'],b['flags']))
        self.assertEqual(bytes(m.u.mem_read(0,1<<20)),first)
        self.assertEqual((b['nonterminal_prefix'],b['polls'],b['registers']['sp']&65535),(True,7,0x7E))
        self.assertTrue(m.stopped_prefix)
        self.assertFalse(m.returned)

    def test_foreign_SS_full_ESP_and_FS_GS_are_checked(self):
        m = self.machine()
        for kind in ('spawn','render','gate','tick'):
            r = m.run(kind,cap=1,flags=0xED7,ss=0x8000,stack=0x80,table='signed')
            self.assertEqual((r['registers']['ss'],r['registers']['sp']&65535),(0x8000,0x86 if kind=='gate' else 0x82))
            self.assertEqual((r['registers']['fs'],r['registers']['gs']),(0x3456,0x4567))
            self.assertEqual(r['flags']&0x600,0x600)
            self.assertEqual(r['registers']['sp']>>16,0x1357^0x5AA5)

    def test_native_closed_cycle_proof_is_rechecked_after_opcode_change(self):
        proof = geometry_proof(self.target)
        self.assertEqual((proof['maximum_loop_iterations'],proof['maximum_rand_calls_per_spawn']),(255,1020))
        self.assertFalse(proof['budget_expiry_used'])
        raw = bytearray(self.target.program_image)
        raw[CS*16+0x2713] ^= 1
        with self.assertRaisesRegex(ValueError,'closed polling CFG'):
            geometry_proof(replace(self.target,program_image=bytes(raw)))

    @unittest.skipUnless(REPORT.is_file(),'complete snow report absent')
    def test_witness_separates_extent_procedures_prefixes_and_unowned_context(self):
        report = json.loads(REPORT.read_bytes())
        if not report['complete']:
            self.skipTest('snow full review running')
        scope = report['scope']
        witness(scope)
        for part,key,value in (('runtime','functions',1),('runtime','extents',7),('runtime','ignored_stack_bytes',32),
                ('runtime','actual_owned_RNG_and_flake',False),('runtime','vector_library_or_tables_owned',True),
                ('runtime','physical_IRQ_audio_pixels_or_timing_proved',True),('layout','mz_relocation_count',5),
                ('negative_controls','count',71)):
            bad = deepcopy(scope)
            bad[part][key] = value
            with self.assertRaises(ValueError):
                witness(bad)
