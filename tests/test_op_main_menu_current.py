"""Complete main caller, inline switch ownership and actual nested state flow."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.op_main_menu_layout import verify
from lib.op_main_menu_runtime import Machine,negative_controls,QUIT,INIT,LOCK,INMAIN,SEL
from review_th03_op_cfg_work import images
from review_th03_op_main_menu_work import witness,legacy_invariance
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'
@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'private current OP absent')
class MainMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,*_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def byte(self,m,off):return bytes(m.uc.mem_read(m.data+off,1))[0]
    def test_complete_native_caller_and_symbolic_far_relaxation(self):
        r=verify(ROOT,self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],r['instruction_bytes'],r['inline_non_instruction_bytes']),(1,291,278,13))
        self.assertEqual((len(r['ordered_native_fields']),len(r['ordered_relocations'])),(42,1))
        self.assertEqual(r['natural_music_call']['native_field'],[2221,4,0xCC,0x16,1,14])
        self.assertFalse(r['whole_product_accepted'])
    def test_equal_target_candidate_cannot_hide_unexecuted_separator(self):
        raw=bytearray(self.target.program_image);raw[0xA1F6]=1;bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'all 291 resolved native bytes'):verify(ROOT,self.work,bad,bad)
    def test_missing_single_scoped_MZ_pair_rejects(self):
        bad=replace(self.target,relocations=tuple(r for r in self.target.relocations if r.linear!=0xA0EE))
        with self.assertRaisesRegex(ValueError,'ordered MZ vector'):verify(ROOT,self.work,bad,bad)
    def test_all_owned_callees_share_the_original_physical_UC(self):
        m=self.machine();self.assertTrue(all(child.uc is m.uc for child in m.children.values()))
        for selection,expected in ((0,['story','wait']),(1,['vs','wait']),(2,['wait']),(3,['score'])):
            r=m.run(selection=selection,input=0x20)
            self.assertEqual([c['name'] for c in r['nested']],expected);self.assertTrue(r['returned'])
    def test_screen_return_is_early_even_when_cancel_was_initially_set(self):
        m=self.machine();r=m.run(input=0x3020,selection=0)
        self.assertEqual((self.byte(m,QUIT),self.byte(m,INIT),self.byte(m,LOCK),self.byte(m,INMAIN)),(0,0,0,1))
        self.assertEqual([c['name'] for c in r['nested']],['story','wait'])
        self.assertEqual(bytes(m.uc.mem_read(m.data+0x1AA6,2)),b'\1\0')
    def test_story_AL_only_cancellation_flows_through_actual_instructions(self):
        m=self.machine();r=m.run(input=0x20,selection_ax=0x100,selected_char=17)
        self.assertFalse(r['nested'][0]['observation']['cancelled'])
        self.assertGreater(r['nested'][0]['observation']['random_calls'],0)
        r=m.run(input=0x20,selection_ax=0xA580)
        self.assertTrue(r['nested'][0]['observation']['cancelled'])
    def test_actual_main_reentry_reinitializes_and_preserves_story_seen(self):
        m=self.machine();self.assertTrue(m.run(input=0x20,selection_ax=0,selected_char=17)['returned'])
        seen=bytes(m.uc.mem_read(m.data+0x99,7));self.assertEqual(sum(bool(v) for v in seen),6)
        m.run(input=0,reenter=True)
        self.assertEqual((self.byte(m,INIT),self.byte(m,LOCK)),(1,1))
        r=m.run(input=0x20,reenter=True,selection_ax=0,selected_char=17)
        self.assertTrue(r['held']);self.assertFalse(r['returned'])
        self.assertEqual(bytes(m.uc.mem_read(m.data+0x99,7)),seen)
    def test_both_arrows_then_confirm_select_the_option_in_source_order(self):
        m=self.machine();m.run(input=0x23,selection=4)
        self.assertEqual((self.byte(m,SEL),self.byte(m,INIT),self.byte(m,0x118C)),(0,0,1))
    def test_fresh_cold_logs_can_change_but_whole_artifacts_cannot(self):
        cold=json.loads((ROOT/'.analysis/work/op-build.json').read_bytes())
        cold['native_phases'][0]['log_sha256']='1'*64
        result=legacy_invariance(ROOT,json.dumps(cold).encode())
        self.assertTrue(result['all_equal']);self.assertFalse(result['cold_report_identity_required'])
        cold['rounds'][0]['outputs']['bin/th03/op.exe']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'complete decoded/stored artifacts'):legacy_invariance(ROOT,json.dumps(cold).encode())
    def test_instruction_and_consumed_table_controls_are_separate(self):
        c=negative_controls(self.target)
        self.assertEqual((c['actual_instruction_mutations'],len(c['rejected']),c['consumed_table_WORD_mutations']),(36,36,6))
        self.assertFalse(c['separator_executed'])
    @unittest.skipUnless((ROOT/'.analysis/work/op-main-menu-build.json').is_file(),'complete current main review absent')
    def test_witness_rejects_fake_callee_return_missing_coverage_and_legacy_drift(self):
        r=json.loads((ROOT/'.analysis/work/op-main-menu-build.json').read_bytes())
        if not r['complete']:self.skipTest('main review running')
        for path,value in ((('runtime','synthetic_owned_callee_returns'),True),(('runtime','observations',0,'executed_callee_bytes','story'),389),(('legacy_invariance','all_equal'),False)):
            s=deepcopy(r['scope']);at=s
            for key in path[:-1]:at=at[key]
            at[path[-1]]=value
            with self.assertRaises(ValueError):witness(s)
