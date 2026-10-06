import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_op_menu as m


class MenuControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=m.ROOT/m.DECODED
        cls.mz=parse_mz(p.read_bytes()) if p.exists() else None
    def setUp(self):
        if self.mz is None:self.skipTest('private decoded target absent')
    def test_simultaneous_music_directions_toggle_twice(self):
        r=m.observe(self.mz,'option',m.scenario(sel=1,put=0x657,input=12,bgm=0))
        self.assertEqual([e['name'] for e in r['events'] if e['name'] in ('kaja','determine')],['kaja','determine','kaja','kaja'])
        self.assertEqual(r['native_entries']['option_choice'],4)
    def test_release_gate_and_repeated_held_key(self):
        seq=[('option',[],8),('option',[],0),('option',[],8),('option',[],8)]
        r=m.observe(self.mz,'option',m.scenario(put=0x657,optlock=0),sequence=seq)
        self.assertEqual(r['native_entries']['option_choice'],1)
    def test_tables_cannot_enter_operands(self):
        image=bytearray(self.mz.program_image);image[m.CS*16+0x799]=0xa3
        with self.assertRaisesRegex(ValueError,'table/pad'):m.analyze(image)
    def test_unknown_callback_is_rejected(self):
        p=m.MenuProbe(self.mz,m.scenario(put=0x5de))
        with self.assertRaisesRegex(ValueError,'escape/operand|caller|callback'):p.run('move',[1,5])
    def test_complete_store_change_rejected(self):
        original=m.MenuSpec.put
        def changed(spec,a,z,v,external=False):
            original(spec,a,z,v,external)
            if a==spec.data+m.MAINLOCK and not external:original(spec,spec.data+0x200,1,0x7e)
        with patch.object(m.MenuSpec,'put',changed):
            with self.assertRaisesRegex(ValueError,'scalar|physical'):m.observe(self.mz,'main',m.scenario(input=0))
    def test_budget_failure_retained(self):
        p=m.MenuProbe(self.mz,m.scenario())
        with self.assertRaisesRegex(ValueError,'budget'):p.run('main',budget=1)
    def test_foreign_pushed_cs_frame(self):
        r=m.observe(self.mz,'main',m.scenario(sel=2,input=0x20))
        self.assertEqual([e['name'] for e in r['events']],['music','fade','wait','cdg2'])
    def test_cancel_after_other_screen_is_not_reached(self):
        r=m.observe(self.mz,'main',m.scenario(sel=0,input=0x1020))
        self.assertEqual(r['stores'],3)


if __name__=='__main__':unittest.main()
