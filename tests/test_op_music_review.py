import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_op_music as m
from probe_th03_unicorn_far_return import probe


class MusicControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=m.ROOT/m.DECODED;cls.mz=parse_mz(p.read_bytes()) if p.exists() else None
    def setUp(self):
        if self.mz is None:self.skipTest('private decoded target absent')
    def test_comment_seek_wraps_before_long_promotion(self):
        r=m.observe(self.mz,'load',m.scenario(read=41),[40])
        e=next(x for x in r['events'] if x['name']=='seek')
        self.assertEqual(e['args'],[0,33600,65535]);self.assertEqual(e['signed_offset'],-31936)
    def test_short_read_keeps_stale_bytes_but_adds_all_terminators(self):
        r=m.observe(self.mz,'load',m.scenario(read=0),[65535])
        self.assertEqual(r['stores'],20);self.assertEqual(r['external_inputs'],[])
        self.assertEqual(next(x for x in r['events'] if x['name']=='seek')['signed_offset'],-840)
    def test_copy_direction_remains_sensitive_to_df(self):
        a=m.observe(self.mz,'put',m.scenario(df=False));b=m.observe(self.mz,'put',m.scenario(df=True))
        self.assertEqual((a['stores'],b['stores']),(16000,16000))
        self.assertNotEqual(a['stores_sha256'],b['stores_sha256'])
        self.assertNotEqual(a['reads_sha256'],b['reads_sha256'])
    def test_nonpositive_point_count_duplicates_existing_first_point(self):
        for n in (0,65535):
            r=m.observe(self.mz,'build',m.scenario(),[255,n,0,0,0,0x1f70])
            self.assertEqual(r['stores'],2);self.assertNotIn('polar',r['native_entries'])
    def test_repeat_polygons_retains_initialization(self):
        r=m.observe(self.mz,'polygons',m.scenario(),sequence=[('polygons',[]),('polygons',[])])
        self.assertEqual(r['native_entries']['irand'],96);self.assertEqual(r['native_entries']['build'],32)
    def test_song_then_cancel_finishes_load_before_exit(self):
        r=m.observe(self.mz,'music',m.scenario(initialized=1,inputs=[0,0x3020,0]))
        self.assertEqual([x['args'] for x in r['events'] if x['name']=='kaja'],[[256],[0]])
        self.assertEqual(len([x for x in r['events'] if x['name']=='snd-load']),1)
        self.assertEqual(r['native_entries']['comment'],4)
        self.assertEqual([x['args'][0] for x in r['events'] if x['name']=='hfree'],[0x5000,0x6000,0x6400,0x6800,0x6c00])
    def test_quit_selection_does_not_load_a_song(self):
        r=m.observe(self.mz,'music',m.scenario(track=20,initialized=1,inputs=[0,0x20,0]))
        self.assertFalse(any(x['name']=='kaja' for x in r['events']))
    def test_native_foreign_operand_change_rejected(self):
        image=bytearray(self.mz.program_image);image[m.CS*16+0x1474]^=1
        with self.assertRaisesRegex(ValueError,'caller|callee'):m.analyze(image)
    def test_branch_into_operand_rejected(self):
        image=bytearray(self.mz.program_image);image[m.CS*16+0xc97]=2
        with self.assertRaisesRegex(ValueError,'operand|neighbor'):m.analyze(image)
    def test_wrong_physical_store_is_rejected(self):
        original=m.MusicSpec.load
        def changed(s,args):original(s,args);s.store(0xefff0,1,0xff)
        with patch.object(m.MusicSpec,'load',changed):
            with self.assertRaisesRegex(ValueError,'scalar|physical'):m.observe(self.mz,'load',m.scenario(read=0),[0])
    def test_far_frame_stack_segment_alias_rejected(self):
        p=m.MusicProbe(self.mz,m.scenario());original=p.get
        p.get=lambda name:0x4001 if name=='SS' else original(name)
        with self.assertRaisesRegex(ValueError,'stack segment'):p.run('music')
    def test_read_hook_far_return_control_records_tool_behavior(self):
        r=probe();self.assertTrue(r['observations'][0]['terminal'])
        if r['unicorn']=='1.0.2rc4':self.assertTrue(r['read_hook_changes_terminal'])


if __name__=='__main__':unittest.main()
