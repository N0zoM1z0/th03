"""Story policy, actual static reentry and native ownership boundaries."""
from copy import deepcopy
from pathlib import Path
from dataclasses import replace
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from review_th03_op_cfg_work import images
from lib.op_story_layout import verify
from lib.op_story_runtime import Machine,negative_controls
from review_th03_op_story_work import witness
WORK=ROOT/'.analysis/toolchain/wineprefix/drive_c/TH03OP'

@unittest.skipUnless((WORK/'bin/th03/op.exe').is_file(),'current OP native pair absent')
class StoryCurrent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.work,cls.target,cls.candidate,_,_=images(ROOT)
    def machine(self):
        m=Machine(self.target,0x3000);self.addCleanup(m.close);return m
    def test_complete_code_fields_and_closed_candidate_CFG(self):
        r=verify(self.work,self.target,self.candidate)
        self.assertEqual((r['functions'],r['code_bytes'],len(r['ordered_native_fields']),len(r['ordered_relocations'])),(1,390,22,5))
        self.assertEqual(len(r['blocked_candidate_CFG']),11);self.assertFalse(r['whole_product_accepted'])
        self.assertFalse(r['library_random_source_credit_added']);self.assertEqual(r['owners'][0]['unit_id'],'th03-op-decoded-entry-screens')
    def test_two_equal_mutated_images_cannot_hide_native_producer_drift(self):
        raw=bytearray(self.target.program_image);raw[0x9A42]^=1
        bad=replace(self.target,program_image=bytes(raw))
        with self.assertRaisesRegex(ValueError,'complete source producer'):verify(self.work,bad,bad)
    def test_only_AL_cancels_and_AH_survives_the_boolean_return(self):
        m=self.machine();r=m.run(selection_ax=0xA580)
        self.assertTrue(r['cancelled']);self.assertEqual(r['registers']['ax'],0xA501);self.assertEqual(r['random_calls'],0)
        self.assertFalse(m.run(selection_ax=0xA500)['cancelled'])
    def test_actual_static_seen_memory_makes_reentry_nonterminal(self):
        m=self.machine();first=m.run(selected_char=1);second=m.run(selected_char=1,reenter=True)
        self.assertFalse(first['nonterminal']);self.assertEqual(sum(first['seen']),6)
        self.assertTrue(second['nonterminal']);self.assertEqual(second['random_calls'],8);self.assertEqual(second['seen'],first['seen'])
        self.assertTrue(m.run(reenter=True,selection_ax=1)['cancelled'])
    def test_unchecked_character_retry_is_followed_by_a_closed_loop(self):
        r=self.machine().run(selected_char=21)
        self.assertTrue(r['nonterminal']);self.assertEqual(r['retries'],1);self.assertEqual(r['registers']['si'],1)
        self.assertEqual(r['seen'],[1]*7)
    def test_seen_slot_for_excluded_opponent_does_not_reduce_availability(self):
        m=self.machine();r=m.run(selected_char=1,seen=[0,0xFF,0,0,0,0,0])
        self.assertFalse(r['nonterminal']);self.assertEqual(r['seen'],[1,0xFF,1,1,1,1,1])
        self.assertTrue(m.run(seen=[0x80]*7)['nonterminal'])
    def test_rank_BYTE_wrap_real_cfg_transaction_and_caller_words(self):
        m=self.machine();r=m.run(rank=255,options=(0x12,0x34),random_seed=0xFFFFFFFF,stack=0x80,resoff=0xFF80,flags=0xED7)
        self.assertEqual(r['file_hex'][:8],'1234ffd3')
        self.assertEqual(bytes(m.uc.mem_read(0x60000+0xFF80+0x38,1)),bytes(((70+255*25)&255,)))
        self.assertEqual(bytes(m.uc.mem_read(0x70080,4)),b'\xFF\xFF\x5A\xA5')
    def test_actual_instruction_controls_cover_caller_random_and_owned_helpers(self):
        r=negative_controls(self.target);self.assertEqual(r['count'],40)
        self.assertFalse(r['source_or_payload_patched']);self.assertFalse(r['character_selection_code_mutated'])
    @unittest.skipUnless((ROOT/'.analysis/work/op-story-build.json').is_file(),'complete story report absent')
    def test_report_cannot_claim_all_seeds_termination_or_selection_ownership(self):
        r=json.loads((ROOT/'.analysis/work/op-story-build.json').read_bytes())
        if not r['complete']:self.skipTest('story review still running')
        witness(r['scope'])
        for part,key,value in (('runtime','all_32bit_seeds_termination_proved',True),
                               ('runtime','executed_owner_bytes',389),('layout','character_selection_procedure_owned',True),
                               ('layout','library_random_source_credit_added',True)):
            bad=deepcopy(r['scope']);bad[part][key]=value
            with self.assertRaises(ValueError):witness(bad)
