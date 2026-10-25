"""Boundary, signed BYTE, simultaneous-key and native ABI regression checks."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import csv,json,struct,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_option_layout import verify
from lib.op_option_runtime import Machine,negative_controls,SEL,PUT,INIT,LOCK,INOPT
from review_th03_op_cfg_work import images
from review_th03_op_option_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'
@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private source-bound OP absent')
class Option(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def byte(self,m,off):return bytes(m.uc.mem_read(m.data+off,1))[0]
    def test_complete_disjoint_native_owners_and_ordered_vectors(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],r['instruction_bytes'],len(r['ordered_native_fields']),len(r['ordered_relocations'])),(2,595,595,65,9))
        self.assertEqual([(o['offset'],o['size'],o['callee_pop_bytes']) for o in r['owners']],[(0x7A1,63,4),(0x903,532,0)])
        self.assertFalse(r['main_caller_accepted']);self.assertFalse(r['containing_producer_accepted'])
    def test_high_parameter_bytes_are_live_but_only_low_BYTE_is_signed(self):
        m=self.machine();r=m.run('move',selection=127,maximum=0xA503,direction=0x5A01,stack=0x80)
        self.assertEqual(self.byte(m,SEL),3);self.assertEqual(r['registers']['sp'],0x86)
        self.assertEqual(bytes(m.uc.mem_read(0x70082,4)),struct.pack('<2H',0x5A01,0xA503))
        m.run('move',selection=128,maximum=0xA580,direction=0)
        self.assertEqual(self.byte(m,SEL),128)
    def test_both_arrows_execute_in_source_order(self):
        m=self.machine();m.run('option',input=3,selection=0)
        self.assertEqual(self.byte(m,SEL),0)
        m.run('option',input=12,rank=3,key=2)
        self.assertEqual(bytes(m.uc.mem_read(0x60031+0xB,1)),b'\3')
    def test_held_input_stays_locked_until_a_zero_sample(self):
        m=self.machine();m.run('option',input=2,selection=1,allowed=0)
        self.assertEqual((self.byte(m,SEL),self.byte(m,LOCK)),(1,0))
        m.run('option',input=0,selection=1,allowed=0)
        self.assertEqual(self.byte(m,LOCK),1)
    def test_initialization_sets_option_callback_and_blocks_held_input(self):
        m=self.machine();m.run('option',initialized=0,input=2,selection=3)
        self.assertEqual((self.byte(m,SEL),self.byte(m,INIT),self.byte(m,LOCK)),(3,1,0))
        self.assertEqual(bytes(m.uc.mem_read(m.data+PUT,2)),struct.pack('<H',0x657))
    def test_cancel_and_confirm_have_independent_exit_stores(self):
        m=self.machine();r=m.run('option',selection=3,input=0x3020)
        self.assertEqual((self.byte(m,SEL),self.byte(m,INIT),self.byte(m,INOPT),self.byte(m,LOCK)),(4,0,0,0))
        stores=[e for e in m.expected.events if e['kind']=='store']
        self.assertEqual(sum(e['address']==m.data+INIT and e['value']==0 for e in stores),2)
    def test_disabled_sound_redraws_without_changing_requested_BGM(self):
        m=self.machine();m.run('option',selection=1,input=12,bgm=255,disabled=255)
        self.assertEqual(bytes(m.uc.mem_read(0x60031+0x15,1)),b'\xff')
        self.assertFalse(any(e['kind']=='interrupt' for e in m.expected.events))
        self.assertEqual(sum(e['kind']=='entry' and e['address']==0x9F57 for e in m.expected.events),2)
    def test_real_mode_detection_keeps_midi_BYTE_fallback_and_fm_flag(self):
        m=self.machine();m.run('option',selection=1,input=8,driver_ax=0x12FF,midi=2,fm=0)
        self.assertEqual((self.byte(m,0x5DC),self.byte(m,0x1A0A)),(2,0))
        self.assertEqual([e['vector'] for e in m.expected.events if e['kind']=='interrupt'],[0x60,0x60,0x60])
    def test_equal_candidate_target_cannot_hide_code_or_relocation_changes(self):
        raw=bytearray(self.target.program_image);raw[0xA403]^=1
        changed=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'complete resolved native function bytes'):verify(self.work,changed,changed)
        changed=replace(self.target,relocations=tuple(reversed(self.target.relocations)))
        with self.assertRaisesRegex(ValueError,'ordered'):verify(self.work,changed,changed)
    def test_all_35_actual_instruction_controls_fail(self):self.assertEqual(negative_controls(self.target)['count'],35)
    @unittest.skipUnless((ROOT/'.analysis/work/op-option-build.json').is_file(),'complete option report absent')
    def test_witness_rejects_missing_helper_coverage_or_broadened_ownership(self):
        r=json.loads((ROOT/'.analysis/work/op-option-build.json').read_bytes())
        if not r['complete']:self.skipTest('option review running')
        for path,value in ((('runtime','observations',0,'executed_nested_bytes'),566),(('layout','main_caller_accepted'),True)):
            bad=deepcopy(r['scope']);at=bad
            for key in path[:-1]:at=at[key]
            at[path[-1]]=value
            with self.assertRaises(ValueError):witness(bad)
