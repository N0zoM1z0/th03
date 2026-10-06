from dataclasses import replace
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_pi as m


class SharedPiControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={a:parse_mz(p.read_bytes()) for a in m.PROFILES if (p:=m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{a}.exe').exists()}
    def targets(self):
        if not self.images:self.skipTest('private decoded targets absent')
        return [(a,mz,m.PROFILES[a]) for a,mz in self.images.items()]
    def test_independent_data_and_call_bindings(self):
        for a,mz,p in self.targets():
            for key,at in [('palette',0xd),('palette',0x15),('put',0x13),('load',0xf)]:
                image=bytearray(mz.program_image);image[p['cs']*16+p[key]+at]^=1
                with self.assertRaises(ValueError):m.analyze(image,p)
    def test_far_cleanup_and_operand_branch_entry_rejected(self):
        for a,mz,p in self.targets():
            for at in [p['put']+0x87,p['put']+0x25]:
                image=bytearray(mz.program_image);image[p['cs']*16+at]^=1
                with self.assertRaises(ValueError):m.analyze(image,p)
    def test_palette_native_memcpy_clears_df_and_word_order(self):
        for a,mz,p in self.targets():
            probe=m.PiProbe(mz,p);r=probe.run('palette',dict(df=1,**{'if':0}));stores=[e for e in r['events'] if e[0]=='store']
            self.assertEqual([e[1:3] for e in stores],[[probe.data+p['palettes']+i*2,2] for i in range(24)]);self.assertEqual(probe.get('EFLAGS')&0x600,0)
    def test_actual_palette_overlap_propagates_prior_word_writes(self):
        for a,mz,p in self.targets():
            probe=m.PiProbe(mz,p);r=probe.run('palette',dict(slot=2691));values=[e[3] for e in r['events'] if e[0]=='store']
            self.assertEqual(values[:4]*6,values)
    def test_pointer_normalization_discards_word_addition_carry(self):
        for a,mz,p in self.targets():
            r=m.PiProbe(mz,p).run('put',dict(width=8,height=2,pointer=(0xffff,0xffff)))
            calls=[e[2] for e in r['events'] if e[0]=='call'];self.assertEqual([c[1:3] for c in calls],[[0xffff,0xffff],[3,0xffff]])
    def test_callbacks_change_live_stride_and_height(self):
        for a,mz,p in self.targets():
            ds=(p['ds']+0x2000)*16;r=m.PiProbe(mz,p).run('put',dict(height=20,pointer=(0,0x5000),callback_writes=[['packed_put',1,ds+p['headers']+20,'03000300']]))
            calls=[e[2] for e in r['events'] if e[0]=='call'];self.assertEqual([c[0] for c in calls],[640,3,3]);self.assertEqual(calls[1][1:3],[1,0x5000])
    def test_odd_interlace_counter_boundary_is_a_prefix(self):
        for a,mz,p in self.targets():
            if 'interlace' not in p:continue
            r=m.PiProbe(mz,p).run('interlace',dict(height=65535,prefix=True,budget=2000));self.assertFalse(r['terminal']);self.assertTrue(r['events'])
    def test_every_quarter_branch_uses_fixed_two_hundred_rows(self):
        for a,mz,p in self.targets():
            if 'quarter' not in p:continue
            for q in (0,1,2,3,0xffff):
                r=m.PiProbe(mz,p).run('quarter',dict(quarter=q,height=0,pointer=(0,0x5000)))
                calls=[e[2] for e in r['events'] if e[0]=='call'];self.assertEqual(len(calls),200);self.assertEqual(calls[0][0],320)
    def test_failed_free_still_clears_header_and_keeps_buffer_pointer(self):
        for a,mz,p in self.targets():
            probe=m.PiProbe(mz,p);r=probe.run('load',dict(carry=1,status=0xffff,pointer=(4,0x5000)))
            self.assertEqual([e[2] for e in r['events'] if e[:2]==['call','heap_free']],[[0x8000],[0x9000],[0x5000]])
            self.assertEqual(bytes(probe.uc.mem_read(probe.data+p['buffers'],4)),b'\x04\0\0\x50');self.assertEqual(r['status'],0xffff)
    def test_repeated_load_frees_retained_buffer_again(self):
        for a,mz,p in self.targets():
            probe=m.PiProbe(mz,p);probe.run('load',dict(pointer=(4,0x5000)));r=probe.run('load',{},True)
            self.assertEqual([e[2] for e in r['events'] if e[:2]==['call','heap_free']],[[0x5000]])
    def test_free_reads_machine_segment_after_first_callback(self):
        for a,mz,p in self.targets():
            ds=(p['ds']+0x2000)*16;r=m.PiProbe(mz,p).run('load',dict(callback_writes=[['heap_free',1,ds+p['headers']+18,'0000']]))
            self.assertEqual([e[2] for e in r['events'] if e[:2]==['call','heap_free']],[[0x8000],[0x5000]])
    def test_native_memcpy_direction_mutation_is_rejected(self):
        for a,mz,p in self.targets():
            image=bytearray(mz.program_image);image[p['memcpy']+0x12]=0xfd
            with self.assertRaisesRegex(ValueError,'ordered scalar'):m.PiProbe(replace(mz,program_image=bytes(image)),p).run('palette',{})
    def test_complete_physical_guard_rejects_extra_byte(self):
        original=m.PiSpec.events
        def changed(spec,name):yield from original(spec,name);spec.memory[0x8fff0]^=1
        for a,mz,p in self.targets():
            with patch.object(m.PiSpec,'events',changed),self.assertRaisesRegex(ValueError,'full physical memory'):m.PiProbe(mz,p).run('load',{})
    def test_coverage_includes_native_helper_odd_copy_and_free_alignments(self):
        for a,mz,p in self.targets():
            rows=m.matrix(mz,p,True);cov=m.coverage(m.analyze(mz.program_image,p),rows)
            self.assertEqual(cov['positions'],144 if a=='op' else 250)


if __name__=='__main__':unittest.main()
