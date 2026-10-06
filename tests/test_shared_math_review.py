import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_math as m


class SharedMathControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={a:parse_mz(p.read_bytes()) for a in m.PROFILES if (p:=m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{a}.exe').exists()}
    def targets(self):
        if not self.images:self.skipTest('private decoded targets absent')
        return [(a,mz,m.PROFILES[a]) for a,mz in self.images.items()]
    def mainl(self):
        if 'mainl' not in self.images:self.skipTest('private MAINL absent')
        return self.images['mainl'],m.PROFILES['mainl']
    def test_lut_binding_and_far_cleanup(self):
        for a,mz,p in self.targets():
            for at,message in [(p['lut']+4,'LUT actual binding'),(p['lut']+29,'cleanup')]:
                with self.subTest(artifact=a,offset=at):
                    image=bytearray(mz.program_image);image[p['cs']*16+at]^=1
                    with self.assertRaisesRegex(ValueError,message):m.analyze(image,p)
    def test_vector_tables_call_and_alignment(self):
        mz,p=self.mainl()
        for at,message in [(p['vector']+0x1e,'sine/cosine'),(p['between']+0x16,'caller'),(p['vector']+69,'producer byte')]:
            with self.subTest(offset=at):
                image=bytearray(mz.program_image);image[p['cs']*16+at]^=1
                with self.assertRaisesRegex(ValueError,message):m.analyze(image,p)
    def test_atan_alignment_is_decoded_but_unreachable(self):
        mz,p=self.mainl();meta=m.analyze(mz.program_image,p)
        self.assertEqual(meta['bodies'][-1]['unreachable_positions'],[0x3b])
        image=bytearray(mz.program_image);image[p['atan']+0x24]=0x16
        with self.assertRaisesRegex(ValueError,'unreachable atan alignment'):m.analyze(image,p)
    def test_all_lut_bytes_and_flags_are_native(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                probe=m.MathProbe(mz,p);row=probe.run('lut',dict(df=1,**{'if':0}))
                self.assertEqual(row['stores'],[[probe.data+p['table']+i,1,m.reverse(i)] for i in range(256)])
                self.assertEqual(row['if_df'],0x400)
    def test_real_divide_stop_cannot_resume_same_instance(self):
        mz,p=self.mainl();probe=m.MathProbe(mz,p);row=probe.run('atan',dict(x=0,y=-32768))
        self.assertFalse(row['terminal']);self.assertEqual(row['fault']['vector'],0);self.assertEqual(row['stores'],[])
        with self.assertRaisesRegex(ValueError,'post-trap'):probe.run('lut',{})
    def test_far_word_crosses_boundary_and_alias_order_is_preserved(self):
        mz,p=self.mainl();probe=m.MathProbe(mz,p)
        row=probe.run('vector',dict(length=-1,angle=1,xp=[0x5000,0xffff],yp=[0x6000,0]))
        self.assertEqual(row['stores'],[[0x5ffff,2,0xffff],[0x60000,2,0xffff]])
    def test_changed_table_is_used_by_later_calls(self):
        mz,p=self.mainl();probe=m.MathProbe(mz,p)
        first=probe.run('vector',dict(angle=1,length=-32768,xp=[p['ds']+0x2000,p['sine']+2],yp=[p['ds']+0x2000,p['sine']+130]),True)
        later=probe.run('vector',dict(angle=1,length=257),True)
        self.assertNotEqual([r[2] for r in later['stores']],[m.u16(257*v//256) for v in (m.sine_words()[65],m.sine_words()[1])])
        self.assertEqual([r[2] for r in first['stores']],[0x8000,0xfd00])
        self.assertEqual([r[2] for r in later['stores']],[0xfcfd,0x7f80])
    def test_ordered_store_model_rejects_swapped_outputs(self):
        mz,p=self.mainl();original=m.MathSpec.invoke
        def changed(spec,*args):original(spec,*args);spec.stores.reverse()
        with patch.object(m.MathSpec,'invoke',changed),self.assertRaisesRegex(ValueError,'ordered scalar'):m.MathProbe(mz,p).run('vector',dict(length=257,angle=32))
    def test_full_physical_memory_guard_rejects_extra_byte(self):
        original=m.MathSpec.invoke
        def changed(spec,*args):original(spec,*args);spec.memory[0x8fff0]^=1
        for a,mz,p in self.targets():
            with self.subTest(artifact=a),patch.object(m.MathSpec,'invoke',changed):
                with self.assertRaisesRegex(ValueError,'physical memory'):m.MathProbe(mz,p).run('lut',{})
    def test_native_atan_stack_alias_rejected(self):
        mz,p=self.mainl();probe=m.MathProbe(mz,p);original=probe.get
        probe.get=lambda r:0x4001 if r=='SS' else original(r)
        with self.assertRaisesRegex(ValueError,'native atan far frame'):probe.run('between',dict(points=[0,0,256,1],plus=1,length=257))


if __name__=='__main__':unittest.main()
