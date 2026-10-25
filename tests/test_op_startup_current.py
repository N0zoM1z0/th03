"""Startup boundaries, real descendant state and full cold-graph refusal."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_startup_layout import START,SIZE,verify as layout
from lib.op_startup_cold import verify as cold_graph
from lib.op_startup_runtime import Machine,OPTION_PATH,stream
from review_th03_op_cfg_work import images
import review_th03_op_startup_work as review


@unittest.skipUnless((ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP/bin/th03/op.target.exe').is_file(),
                     'current private OP proof absent')
class OpStartupCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work,cls.target,cls.candidate,cls.cold,_=images(ROOT)

    def machine(self):
        machine=Machine(self.target,0x3000)
        self.addCleanup(machine.close)
        return machine

    def test_equal_mutants_and_reordered_MZ_sites_cannot_inherit_native_ownership(self):
        raw=bytearray(self.target.program_image)
        raw[START+SIZE-1]^=8
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'entire independently resolved native'):
            layout(ROOT,self.work,bad,bad)
        relocations=list(self.target.relocations)
        sites=[i for i,r in enumerate(relocations) if START<=r.linear<START+SIZE]
        relocations[sites[0]],relocations[sites[1]]=relocations[sites[1]],relocations[sites[0]]
        bad=replace(self.target,relocations=tuple(relocations))
        with self.assertRaisesRegex(ValueError,'literal ordered MZ vector'):
            layout(ROOT,self.work,bad,bad)

    def test_raw_dispatch_fixture_really_changes_live_BYTE_and_wraps_rand(self):
        machine=self.machine()
        result=machine.run(raw_dispatch=128,loop_prefix=3,samples=stream(0,0,0),random=0xFFFFFFFE)
        self.assertEqual(bytes(machine.uc.mem_read(machine.data+0x118C,1)),b'\x80')
        # Attract increments to FFFFFFFF; the first root INC then wraps the DWORD.
        self.assertEqual(int.from_bytes(machine.uc.mem_read(0x50010,4),'little'),2)
        self.assertEqual([row['name'] for row in result['borrowed']],['wait','main'])
        self.assertTrue(result['loop_prefix'])
        self.assertFalse(result['returned'])

    def test_actual_option_path_returns_through_native_exit_and_cfg_copy(self):
        machine=self.machine()
        self.assertTrue(all(child.uc is machine.uc for child in machine.children.values()))
        result=machine.run(samples=OPTION_PATH,flags=0xED7,stack=0x100)
        self.assertEqual((result['returned'],result['iterations']),(True,9))
        self.assertIn('option',[row['name'] for row in result['borrowed']])
        self.assertEqual(bytes(machine.uc.mem_read(0x70100,4)),b'\xFF\xFF\x00\x30')
        self.assertEqual(result['flags']&0x400,0)  # Real CRT CLD survives root exit.

    def test_short_cfg_stops_before_arbitrary_resident_use_and_is_not_a_return(self):
        result=self.machine().run(read_bytes=0,cfg_boundary=True)
        self.assertTrue(result['cfg_boundary'])
        self.assertFalse(result['returned'])
        self.assertFalse(result['held'])
        self.assertEqual((result['borrowed'],result['inherited_private_stack_bytes']),([],0))

    def test_held_story_propagates_live_SP_through_the_intermediate_main_frame(self):
        machine=self.machine()
        result=machine.run(samples=stream(0x20,0,0x20),selection_ax=0,selected_char=17)
        self.assertTrue(result['held'])
        self.assertFalse(result['returned'])
        self.assertEqual(result['registers']['sp']&65535,0xF800-18)
        self.assertEqual(machine.r('sp'),0xF800-18)
        self.assertEqual(bytes(machine.uc.mem_read(0x7F800,4)),b'\xFF\xFF\x00\x30')

    def test_stale_unrelated_native_object_fails_the_entire_cold_graph(self):
        report=deepcopy(self.cold)
        name=next(n for n in report['rounds'][0]['outputs'] if n.endswith('.obj') and n!='obj/th03/op_01.obj')
        for round_ in report['rounds']:
            round_['outputs'][name]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'complete current output'):
            cold_graph(ROOT,self.work,self.target,self.candidate,report)

    def test_witness_cannot_turn_prefixes_into_returns_or_hide_private_windows(self):
        scope=json.loads(review.REPORT.read_bytes())['scope']
        review.witness(scope)
        for path,value in ((('runtime','observations',0,'ordinary_returns'),1482),
                           (('runtime','synthetic_owned_callee_returns'),True),
                           (('runtime','borrowed_private_stack_bytes','main'),0)):
            bad=deepcopy(scope)
            at=bad
            for key in path[:-1]:at=at[key]
            at[path[-1]]=value
            with self.assertRaises(ValueError):review.witness(bad)


if __name__=='__main__':unittest.main()
