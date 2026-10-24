"""Whole-entry wait cases and explicitly separate signed-loop continuations."""
from copy import deepcopy
from pathlib import Path
import json,sys,unittest
from unicorn import UC_HOOK_CODE
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_attract_layout import verify
from lib.op_attract_runtime import Machine,negative_controls
from review_th03_op_cfg_work import images
from review_th03_op_attract_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'

@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class Attract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):_,cls.target,*_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_complete_native_body_and_external_near_field(self):
        w,t,c,*_=images(ROOT);r=verify(w,t,c)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields'])),(1,105,9))
        self.assertEqual(len(r['ordered_relocations']),5)
        self.assertEqual([f['offset'] for f in r['ordered_native_fields'] if not f['locat']&0x40],[1366])
        self.assertIsNone(r['owners'][0]['canonical_file_offset']);self.assertFalse(r['containing_producer_accepted'])
    def test_initial_nonzero_input_is_cleared_and_first_poll_still_updates_random(self):
        m=self.machine();r=m.run(random=0xFFFFFFFF)
        self.assertEqual((r['polls'],r['demo_calls'],r['random']),(1,0,0))
        base=0x60000+0x31
        self.assertEqual((m.uc.mem_read(base+0xF,1),m.uc.mem_read(base+0x14,1)),(b'\xA5',b'\xA5'))
    def test_full_entry_520_and_521_poll_cases_keep_late_input_demo(self):
        m=self.machine()
        self.assertEqual(m.run(polls=520)['demo_calls'],0)
        r=m.run(polls=521);self.assertEqual((r['demo_calls'],r['random']),(1,600))
    def test_returning_demo_repeats_on_each_later_poll(self):
        r=self.machine().run(polls=523)
        self.assertEqual((r['demo_calls'],r['random']),(3,3200))
    def test_actual_delay_runs_for_each_poll_and_animation_column(self):
        m=self.machine();r=m.run(polls=523)
        self.assertEqual((r['actual_delay_calls'],r['counter_updates'],r['registers']['ax']),(537,1074,1))
        from lib.op_attract_runtime import DELAY
        self.assertTrue(set(range(DELAY,DELAY+21)) <= m.nested_covered)
    def test_signed_WORD_continuations_do_not_claim_elapsed_frames(self):
        m=self.machine()
        for frame,count in ((520,1),(0x7FFE,1),(0x7FFF,0),(0x8000,0),(0xFFFF,0)):
            r=m.run(continuation=frame)
            self.assertEqual((r['polls'],r['continuation'],r['demo_calls']),(1,frame,count))
    def test_player2_and_absent_joystick_do_not_end_the_wait(self):
        m=self.machine();rows=[(0,0,0xFFFF,0x8000),(0,1,0,0)]
        self.assertEqual(m.run(samples=rows,present=0)['polls'],2)
        self.assertEqual(m.run(samples=[rows[0]],present=0x8000)['polls'],1)
    def test_actual_demo_255_wrap_keeps_adjacent_seed_and_stack_byte(self):
        r=self.machine().run(continuation=520,demo=255)
        self.assertEqual(r['random'],0x05090B07);self.assertEqual(r['file_hex'],'a5a5a5d3570050a7')
    def test_actual_call_sites_visit_fourteen_columns_and_keep_tile_arguments(self):
        m=self.machine();columns=[];left=[]
        h=m.uc.hook_add(UC_HOOK_CODE,lambda uc,a,s,u:columns.append(m.r('si')),begin=m.base+0x9E5D,end=m.base+0x9E5D)
        h2=m.uc.hook_add(UC_HOOK_CODE,lambda uc,a,s,u:left.append(bytes(uc.mem_read(0x70000+m.r('sp'),6))),begin=m.base+0x9E52,end=m.base+0x9E52)
        try:m.run()
        finally:m.uc.hook_del(h);m.uc.hook_del(h2)
        self.assertEqual(columns,list(range(176,288,8)));self.assertEqual(left,[b'\0\0\0\x01\xA0\0'])
    def test_near_return_restores_SI_BP_and_inherits_IF_DF(self):
        m=self.machine()
        for flags in (2,0x202,0x402,0xED7):
            r=m.run(flags=flags,status=0x8000,continuation=520,midi=1)
            self.assertEqual((r['registers']['si'],r['registers']['bp']),(0x1C1B,0x207D))
            self.assertEqual(r['flags']&0x600,flags&0x600)
    def test_all_twenty_four_real_mutations_fail(self):
        self.assertEqual(negative_controls(self.target)['count'],24)
    @unittest.skipUnless((ROOT/'.analysis/work/op-attract-build.json').is_file(),'full attract witness absent')
    def test_continuations_cannot_be_reclassified_as_ordinary_entry_coverage(self):
        scope=json.loads((ROOT/'.analysis/work/op-attract-build.json').read_bytes())['scope']
        for key,value in (('ordinary_entry_cases',615),('executed_nested_bytes',0)):
            s=deepcopy(scope);s['runtime']['observations'][0][key]=value
            with self.assertRaisesRegex(ValueError,'ordinary/continuation'):witness(s)
