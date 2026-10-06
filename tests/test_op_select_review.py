import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_op_select as m


class SelectionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=m.ROOT/m.DECODED;cls.mz=parse_mz(p.read_bytes()) if p.exists() else None
    def setUp(self):
        if self.mz is None:self.skipTest('private decoded target absent')
    def test_two_confirm_bits_execute_in_order_even_after_confirmation(self):
        r=m.observe(self.mz,'update',m.scenario(confirmed=[0,1],paletted=[1,1]),[0,0x30])
        events=[e for e in r['nonpoint_events'] if e['name']=='cdg-load']
        self.assertEqual([e['args'][0] for e in events],[1,1])
        self.assertEqual(r['state']['paletted'],[2,1]);self.assertEqual(r['state']['fade'],0)
        self.assertEqual(r['state']['confirmed'],[1,1])
    def test_bomb_collision_decrements_paletted_byte(self):
        r=m.observe(self.mz,'update',m.scenario(confirmed=[1,0],paletted=[2,1],sel=[0,0]),[1,0x10])
        self.assertEqual(r['state']['paletted'],[2,1]);self.assertEqual(r['nonpoint_events'][-1]['args'][0],0)
    def test_lock_requires_release_and_release_does_not_process_input(self):
        r=m.observe(self.mz,'update',m.scenario(locked=[255,0]),
                    sequence=[('update',[0,0x20]),('update',[0,0]),('update',[0,2])])
        self.assertEqual(r['state']['sel'],[1,1]);self.assertEqual(r['state']['confirmed'],[0,0])
        self.assertEqual(r['state']['locked'],[1,0]);self.assertEqual(r['events'],0)
    def test_confirmed_player_preserves_lock_on_release(self):
        r=m.observe(self.mz,'update',m.scenario(confirmed=[1,0],locked=[255,0]),[0,0])
        self.assertEqual(r['stores'],0);self.assertEqual(r['state']['locked'][0],255)
    def test_later_missing_rank_overrides_earlier_unlocked_rank(self):
        ranks=[m.rank_fixture(99),m.rank_fixture(exists=0),m.rank_fixture(),m.rank_fixture()]
        r=m.observe(self.mz,'unlock',m.scenario(ranks=ranks))
        self.assertEqual(r['replies'],[7]);self.assertEqual(r['native_entries']['load'],2)
        self.assertEqual(r['native_entries']['irand'],12);self.assertEqual(r['native_entries']['recreate'],1)
    def test_init_preserves_locks_and_cycle(self):
        r=m.observe(self.mz,'init',m.scenario(locked=[255,1],cycle=254,confirmed=[1,1]))
        self.assertEqual(r['state']['locked'],[255,1]);self.assertEqual(r['state']['cycle'],254)
        self.assertEqual(r['state']['confirmed'],[1,1]);self.assertEqual(r['state']['trail'],8)
    def test_first_wait_keeps_init_vsync_and_decrements_trail(self):
        r=m.observe(self.mz,'story',m.scenario(game_mode=1,inputs=[[0,0,0],[0,0,0x1000]]))
        self.assertEqual(r['state']['trail'],7);self.assertEqual(r['replies'],[1])
        self.assertEqual(r['state']['fade'],1)
    def test_cancel_runs_after_confirmation_and_frees_twenty_two_slots(self):
        r=m.observe(self.mz,'story',m.scenario(game_mode=1,inputs=[[0,0,0x1030]]))
        self.assertEqual(r['state']['confirmed'],[1,1]);self.assertEqual(r['replies'],[1])
        self.assertEqual([e['args'][0] for e in r['nonpoint_events'] if e['name']=='cdg-free'],list(range(22)))
        self.assertEqual([e['args'] for e in r['nonpoint_events'] if e['name']=='kaja'],[[256],[0],[256]])
    def test_native_indirect_pointer_operand_change_rejected(self):
        image=bytearray(self.mz.program_image);image[m.CS*16+0x2242]^=1
        with self.assertRaisesRegex(ValueError,'indirect'):m.analyze(image)
    def test_foreign_destination_change_rejected(self):
        image=bytearray(self.mz.program_image);image[m.CS*16+0x20db]^=1
        with self.assertRaisesRegex(ValueError,'caller'):m.analyze(image)
    def test_wrong_physical_store_rejected(self):
        original=m.SelectSpec.update
        def changed(s,args):original(s,args);s.store(0xefff0,1,0xff)
        with patch.object(m.SelectSpec,'update',changed):
            with self.assertRaisesRegex(ValueError,'scalar|physical'):m.observe(self.mz,'update',m.scenario(),[0,0])
    def test_far_frame_stack_segment_alias_rejected(self):
        p=m.SelectProbe(self.mz,m.scenario());original=p.get
        p.get=lambda name:0x4001 if name=='SS' else original(name)
        with self.assertRaisesRegex(ValueError,'stack segment'):p.run('story')
    def test_floor_division_mutation_rejected_for_negative_curve_products(self):
        with patch.object(m,'trunc',lambda n,d:n//d):
            with self.assertRaisesRegex(ValueError,'scalar events'):
                m.observe(self.mz,'curve',m.scenario(),[257,257,220,0,0])


if __name__=='__main__':unittest.main()
