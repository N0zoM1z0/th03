import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_op_entry as e


class EntryControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=e.ROOT/e.menu.DECODED;cls.mz=parse_mz(p.read_bytes()) if p.exists() else None
    def setUp(self):
        if self.mz is None:self.skipTest('private decoded target absent')
    def test_reentry_after_failed_exec_retains_dirty_seen(self):
        r=e.reentry_failure(self.mz)
        self.assertTrue(r['first_terminal']);self.assertFalse(r['second_terminal']);self.assertGreater(r['second_native']['irand'],10)
    def test_story_palette_and_skill_bytes(self):
        r=e.observe(self.mz,'story',e.scenario(selected_char=15,rank=255,seed=0xffffffff,offset=0x31))
        self.assertEqual(r['result'],0);self.assertEqual(r['native_entries']['cfg_save'],1)
        self.assertEqual([x['name'] for x in r['events'][-6:]],['write','close','restore','kaja','game-exit','execl'])
    def test_demo_255_wrap_retains_out_of_bounds_index_attempt(self):
        r=e.observe(self.mz,'demo',e.scenario(demo=255))
        self.assertEqual(r['native_entries']['demo'],1)
        self.assertEqual(r['files'][0]['args'][0],4)
    def test_wait_threshold_exec_returns_then_continues(self):
        r=e.observe(self.mz,'wait',e.scenario(inputs=[0]*521+[0x20]))
        self.assertEqual(r['native_entries']['demo'],2)
        self.assertEqual(len([x for x in r['events'] if x['name']=='execl']),2)
    def test_vs_cancel_does_not_leave_menu(self):
        r=e.observe(self.mz,'vs',e.scenario(inputs=[0x1000,0,0x20],selection_reply=1))
        self.assertEqual(len([x for x in r['events'] if x['name']=='input']),3)
        self.assertEqual(r['result'],1)
    def test_startup_held_input_is_processed_after_initial_unlock(self):
        r=e.observe(self.mz,'entry',e.scenario(maininit=0,sel=5,inputs=[0x20,0x20]))
        self.assertEqual(r['native_entries']['main'],2)
        self.assertEqual(r['native_entries']['scopy'],1)
    def test_full_physical_store_change_rejected(self):
        orig=e.EntrySpec.reset_scores
        def changed(s):orig(s);s.put(s.resident+0x28,1,0xff)
        with patch.object(e.EntrySpec,'reset_scores',changed):
            with self.assertRaisesRegex(ValueError,'scalar|physical'):e.observe(self.mz,'score',e.scenario())
    def test_foreign_call_operand_mutation_rejected(self):
        image=bytearray(self.mz.program_image);image[e.CS*16+0x14e]^=1
        with self.assertRaisesRegex(ValueError,'caller|callee'):e.analyze(image)
    def test_far_startup_return_frame_is_checked(self):
        p=e.EntryProbe(self.mz,e.scenario(zoom=1))
        orig=p.get
        def changed(name):return 0x4001 if name=='SS' else orig(name)
        p.get=changed
        with self.assertRaisesRegex(ValueError,'stack segment'):p.run('entry')
    def test_uninitialized_save_byte_is_retained_in_native_file_trace(self):
        r=e.observe(self.mz,'cfg_save',e.scenario())
        self.assertTrue(r['files'][0]['bytes'].endswith('a5'))
        self.assertEqual(len(next(x['defined_bytes'] for x in r['events'] if x['name']=='write')),6)


if __name__=='__main__':unittest.main()
