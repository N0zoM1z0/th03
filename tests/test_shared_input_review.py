from dataclasses import replace
from pathlib import Path
import struct
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_th03_shared_input as m


class SharedInputControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={a:m.parse_mz(path.read_bytes()) for a in m.PROFILES if (path:=m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{a}.exe').exists()}
    def targets(self):
        if not self.images:self.skipTest('private decoded targets absent')
        return [(a,mz,m.PROFILES[a]) for a,mz in self.images.items()]
    def run_probe(self,mz,p,name,s,terminal=True):
        probe=m.InputProbe(mz,p,s);probe.word(p['present'],s.get('present',0));probe.word(p['clock'],0xbeef)
        probe.uc.mem_write(probe.data+p['sound'],bytes([s.get('sound',0)]));probe.uc.mem_write(probe.data+p['midi'],bytes([s.get('midi_active',0)]))
        probe.run(name,s,terminal=terminal,budget=400000 if terminal else 14000);return probe
    def test_independent_data_and_joystick_bindings(self):
        for a,mz,p in self.targets():
            entries={n:o for n,o,_,_ in p['ranges']}
            for at in (entries['frame_delay']+5,entries['interface']+0x10):
                image=bytearray(mz.program_image);image[p['cs']*16+at]^=1
                with self.assertRaises(ValueError):m.analyze(image,p)
    def test_operand_branch_entry_and_far_cleanup_rejected(self):
        for a,mz,p in self.targets():
            entry=next(o for n,o,_,_ in p['ranges'] if n=='frame_delay')
            for at in (entry+16,entry+19):
                image=bytearray(mz.program_image);image[p['cs']*16+at]^=1
                with self.assertRaises(ValueError):m.analyze(image,p)
    def test_second_sample_retains_held_key_and_delay_count(self):
        for a,mz,p in self.targets():
            s=dict(samples=[[[0]*10,m.samples(5,2)[0]]]);probe=self.run_probe(mz,p,'sense',s)
            self.assertEqual([probe.word(p[k]) for k in ('p1','p2','sp')],[32,0,32]);self.assertEqual(probe.outs,1024)
            self.assertEqual(probe.writes[:4],[[p[k],2,0] for k in ('p1','p2','sp','joy')])
    def test_shortened_sampling_loop_fails_scalar_matrix(self):
        for a,mz,p in self.targets():
            entry=next(o for n,o,_,_ in p['ranges'] if n=='sense');image=bytearray(mz.program_image)
            self.assertEqual(image[p['cs']*16+entry+17],2);image[p['cs']*16+entry+17]=1
            with self.assertRaisesRegex(ValueError,'scalar result|port count'):m.matrix(replace(mz,program_image=bytes(image)),p)
    def test_modes_overwrite_or_merge_joystick_as_specified(self):
        for a,mz,p in self.targets():
            for name,expected in [('joy_key',[0x8104,32,32]),('key_joy',[32,0x8104,32]),('one_cpu',[0x8124,0,32]),('cpu_one',[0,0x8124,32]),('attract',[0,0,0x8124])]:
                probe=self.run_probe(mz,p,name,dict(samples=[m.samples(5,2)],present=1,joy=0x8104));self.assertEqual([probe.word(p[k]) for k in ('p1','p2','sp')],expected)
    def test_release_must_finish_before_negative_timeout(self):
        for a,mz,p in self.targets():
            probe=self.run_probe(mz,p,'change',dict(frames=-1,samples=[m.samples(0,1),m.samples()]))
            self.assertEqual((probe.senses,probe.delays),(2,1))
    def test_zero_and_9999_change_timeouts_are_prefixes(self):
        for a,mz,p in self.targets():
            for frames in (0,9999):self.assertFalse(self.run_probe(mz,p,'change',dict(frames=frames),False).stop)
    def test_stalled_clock_does_not_claim_return(self):
        for a,mz,p in self.targets():
            self.assertFalse(self.run_probe(mz,p,'frame_delay',dict(frames=1,direct_delay=True,stalled_delay=True),False).stop)
    def test_frame_wait_uses_unsigned_high_bit_argument(self):
        for a,mz,p in self.targets():
            probe=self.run_probe(mz,p,'frame_delay',dict(frames=0x8000,direct_delay=True,delay_tick=0x4000))
            self.assertEqual(probe.delay_ticks,2);self.assertEqual(probe.word(p['clock']),0x8000)
    def test_measure_result_is_clobbered_by_keyboard_ax(self):
        if 'mainl' not in self.images:self.skipTest('private MAINL absent')
        p=m.PROFILES['mainl'];probe=self.run_probe(self.images['mainl'],p,'measure_wait',dict(sound=1,measure_value=65535,measure=3,samples=[m.samples(4,1)]))
        self.assertEqual(probe.measure_comparisons,[[4,3]]);self.assertEqual(probe.get('AX'),0)
    def test_extra_physical_byte_is_rejected(self):
        original=m.InputProbe.run
        def changed(probe,*args,**kwargs):
            result=original(probe,*args,**kwargs);probe.uc.mem_write(0x8fff0,b'\x7f');return result
        for a,mz,p in self.targets():
            with patch.object(m.InputProbe,'run',changed),self.assertRaisesRegex(ValueError,'complete physical memory'):m.matrix(mz,p)
    def test_complete_keyboard_modes_wait_and_frame_positions(self):
        for a,mz,p in self.targets():
            result=m.coverage(m.analyze(mz.program_image,p),m.matrix(mz,p));self.assertTrue(result['complete']);self.assertGreater(result['prefixes'],0)


if __name__=='__main__':unittest.main()
