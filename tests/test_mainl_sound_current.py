"""Sound/file ABI and state boundaries, without claiming physical devices."""
from copy import deepcopy
from pathlib import Path
import json,sys,unittest
from unicorn import UC_HOOK_CODE
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.decoded_mainl_sound_layout import verify
from lib.decoded_mainl_sound_runtime import Machine,F,negative_controls
from review_th03_mainl_sound_work import images,witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03ML'

@unittest.skipUnless((WORK/'bin/th03/mainl.exe').is_file(),'private current MAINL absent')
class Sound(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,_,_,cls.graph,cls.files=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def watch(self,m,addresses):
        rows=[]
        def capture(uc,a,s,u):
            rva=a-m.base
            if rva in addresses:rows.append((rva,m.registers(),m.r('sp')))
        h=m.uc.hook_add(UC_HOOK_CODE,capture);self.addCleanup(lambda:m.uc.hook_del(h));return rows
    def test_complete_five_objects_and_six_natural_procedures(self):
        r=verify(self.work,self.target,self.candidate,self.graph,self.files)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['native_objects'])),(6,332,5))
        self.assertEqual(sum(len(o['fields']) for o in r['native_objects']),33)
        self.assertEqual(r['normal_tlink_relaxed_calls'],1);self.assertEqual(r['ordered_relocations'],[])
        self.assertEqual((r['private_data_bytes'],r['private_bss_bytes'],r['reviewed_initialized_dependency_bytes']),(0,0,69))
        self.assertFalse(r['adjacent_explicit_padding_accepted']);self.assertFalse(r['whole_product_accepted'])
    def test_load_copies_thirteen_bytes_even_after_filename_NUL(self):
        m=self.machine();name=b'A\0'+b'b'*11;m.run('load',filename=name,filename_offset=0xFFFF)
        self.assertEqual(m.uc.mem_read(m.data+F['load_fn'],13),name)
    def test_MIDI_suffix_scan_skips_first_NUL_and_preserves_overflow(self):
        m=self.machine();name=b'\0'+b'Q'*12;m.run('load',filename=name,midi=2,suffix_end=16)
        self.assertEqual(m.uc.mem_read(m.data+F['load_fn'],13),name)
        self.assertEqual(m.uc.mem_read(m.data+F['load_fn']+16,3),b'md\0')
        m.run('load',filename=b'X'*13,midi=2,suffix_end=32)
        self.assertEqual(m.uc.mem_read(m.data+F['load_fn']+32,3),b'md\0')
    def test_file_errors_still_query_read_and_close_with_original_DS(self):
        m=self.machine();rows=self.watch(m,{0xC8C7,0xC8DA,0xC8DE,0xC8E6,0xC8EB})
        r=m.run('load',midi=2,open_result=5,open_failure=True,read_failure=True,read_result=6,close_failure=True)
        self.assertEqual([a for a,_,_ in rows],[0xC8C7,0xC8DA,0xC8E6,0xC8EB])
        self.assertEqual((rows[1][1]['bx'],rows[2][1]['bx'],rows[2][1]['cx']),(5,5,0x5000))
        self.assertEqual((rows[2][1]['ds'],rows[3][1]['ds'],rows[3][1]['ax']),(0x6000,m.ds,0x3E06))
        self.assertEqual((r['registers']['ds'],m.r('sp')),(m.ds,0xF804))
    def test_idle_first_SE_keeps_frame_but_equal_priority_restarts(self):
        m=self.machine();r=m.run('play',playing=255,frame=7,argument=3)
        self.assertEqual((r['playing'],r['frame']),(3,7))
        r=m.run('play',playing=3,frame=7,argument=3);self.assertEqual((r['playing'],r['frame']),(3,0))
    def test_priority_index_keeps_the_full_WORD_before_DL_storage(self):
        r=self.machine().run('play',playing=0,argument=0x100,frame=7)
        self.assertEqual((r['registers']['bx'],r['registers']['dx'],r['playing'],r['frame']),(0x100,0x100,0,0))
    def test_priority_comparison_remains_unsigned_for_mutable_BYTE_tables(self):
        m=self.machine();r=m.run('play',playing=0,argument=1,frame=7,priority_patch=((0,128),(1,127)))
        self.assertEqual((r['playing'],r['frame']),(0,7))
        r=m.run('play',playing=0,argument=1,frame=7,priority_patch=((0,255),(1,255)))
        self.assertEqual((r['playing'],r['frame']),(1,0))
    def test_SE_duration_uses_postincrement_and_BYTE_wrap(self):
        m=self.machine()
        self.assertEqual(m.run('update',playing=1,frame=3,duration_patch=((1,4),))['playing'],1)
        r=m.run('update',playing=1,frame=4,duration_patch=((1,4),));self.assertEqual((r['playing'],r['frame']),(255,0))
        r=m.run('update',playing=1,frame=255);self.assertEqual((r['playing'],r['frame'],r['driver_calls']),(1,0,0))
    def test_first_SE_frame_calls_PMD_before_expiring_a_zero_duration(self):
        m=self.machine();rows=self.watch(m,{0xCEA0,0xCED6,0xCEDA})
        r=m.run('update',playing=1,frame=0,duration_patch=((1,0),),midi=1)
        self.assertEqual([(a,regs['ax']) for a,regs,_ in rows],[(0xCEA0,0xC01)])
        self.assertEqual((r['playing'],r['frame']),(255,0))
    def test_inactive_KAJA_returns_incoming_AX_without_loading_argument(self):
        r=self.machine().run('kaja',active=0,argument=0xFFFF)
        self.assertEqual((r['registers']['ax'],r['driver_calls']),(0x1357,0))
    def test_KAJA_and_measure_route_MIDI_only_when_exactly_one(self):
        m=self.machine();rows=self.watch(m,{0xCED6,0xCEDA,0xD41B,0xD422})
        m.run('kaja',midi=2);m.run('kaja',midi=1)
        m.run('measure',midi=2,measure=0,measures=(0xFFFF,));m.run('measure',midi=1,measure=0,measures=(0xFFFF,))
        self.assertEqual([a for a,_,_ in rows],[0xCED6,0xCEDA,0xD41B,0xD422])
        self.assertEqual(rows[-1][1]['dx'],192)
    def test_no_BGM_measure_executes_actual_far_frame_delay(self):
        m=self.machine();rows=self.watch(m,{0xCB52})
        r=m.run('measure',active=0,frames=0xFFFF,ticks=(0xFFFE,0xFFFF),measure=7)
        self.assertEqual(len(rows),1);self.assertEqual(rows[0][2],0xF7F8)
        self.assertEqual((r['counter_updates'],r['registers']['ax'],m.maximum_stack),(2,0xFFFF,10))
    def test_counter_and_measure_limits_are_unsigned_and_query_zero_once(self):
        m=self.machine();r=m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0x402)
        self.assertEqual((r['counter_updates'],r['registers']['ax'],r['flags']&0x600),(2,0x8000,0x400))
        r=m.run('measure',measure=0,measures=(0xFFFF,));self.assertEqual(r['driver_calls'],1)
        r=m.run('measure',measure=0xFFFF,measures=(0x7FFF,0xFFFE,0xFFFF));self.assertEqual(r['driver_calls'],3)
    def test_all_thirty_three_instruction_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],33)
    @unittest.skipUnless((ROOT/'.analysis/work/mainl-sound-build.json').is_file(),'full current sound witness absent')
    def test_partial_state_domains_or_adjacent_padding_cannot_inherit_acceptance(self):
        s=json.loads((ROOT/'.analysis/work/mainl-sound-build.json').read_bytes())['scope']
        for key,value in (('exhaustive_byte_states',255),('file_read_request_bytes',0x4000)):
            wrong=deepcopy(s);wrong['runtime'][key]=value
            with self.assertRaisesRegex(ValueError,'runtime dimensions'):witness(wrong)
        wrong=deepcopy(s);wrong['layout']['adjacent_explicit_padding_accepted']=True
        with self.assertRaisesRegex(ValueError,'source classification'):witness(wrong)
