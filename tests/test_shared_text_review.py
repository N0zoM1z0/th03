import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_text as m


class SharedTextControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images={a:parse_mz(p.read_bytes()) for a in m.PROFILES
                    if (p:=m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{a}.exe').exists()}

    def targets(self):
        if not self.images: self.skipTest('private decoded targets absent')
        return [(a,mz,m.PROFILES[a]) for a,mz in self.images.items()]

    def test_classifier_and_caller_bindings_are_independent(self):
        for a,mz,p in self.targets():
            for offset,message in [(0x67,'classifier'),(0x9a,'classifier'),(0xb7,'classifier'),(0x2c,'caller'),(0x80,'caller'),(0x25b,'caller')]:
                with self.subTest(artifact=a,offset=offset):
                    image=bytearray(mz.program_image); image[p['cs']*16+p['start']+offset]^=1
                    with self.assertRaisesRegex(ValueError,message): m.analyze(image,p)

    def test_branch_and_far_cleanup_controls(self):
        for a,mz,p in self.targets():
            for offset,value,message in [(0x6b,0x21,'operand/neighbor'),(0x263,8,'cleanup')]:
                with self.subTest(artifact=a,offset=offset):
                    image=bytearray(mz.program_image); image[p['cs']*16+p['start']+offset]=value
                    with self.assertRaisesRegex(ValueError,message): m.analyze(image,p)

    def test_negative_division_and_nul_trail_are_preserved(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                probe=m.TextProbe(mz,p); row=probe.run(dict(left=-1,string=[0x81,0,90,0],offset=0xffff,jis=0,fx=0x3f))
                self.assertEqual(row['string_offset'],2)
                self.assertEqual(row['conversions'],1)
                self.assertEqual(next(e for e in probe.trace if e[0]=='convert')[1:], [0x8100,0])
                self.assertEqual(next(e for e in probe.trace if e[0]=='store')[1],0)

    def test_persistent_vram_across_changed_reentry(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                probe=m.TextProbe(mz,p)
                s=dict(left=7,top=400,fx=0x3f,string=[65,0x81,0x40,0],df=1)
                first=probe.run(s); empty=probe.run(dict(string=[0],df=0)); last=probe.run(s)
                self.assertEqual(empty['stores'],0)
                self.assertEqual(first['memory_after_sha256'],last['memory_after_sha256'])
                self.assertEqual(first['trace_sha256'],last['trace_sha256'])

    def test_budget_prefix_is_checked_by_scalar_events(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                row=m.TextProbe(mz,p).run(dict(left=-32768,unterminated=True,df=1),False)
                self.assertFalse(row['terminal']); self.assertGreater(row['stores'],0)

    def test_unified_trace_rejects_changed_port_order(self):
        original=m.TextSpec.events
        def changed(spec):
            events=list(original(spec)); events[1],events[2]=events[2],events[1]
            yield from events
        for a,mz,p in self.targets():
            with self.subTest(artifact=a),patch.object(m.TextSpec,'events',changed):
                with self.assertRaisesRegex(ValueError,'unified scalar trace'): m.TextProbe(mz,p).run(dict(string=[65,0],fx=5))

    def test_physical_memory_guard_rejects_untracked_byte(self):
        original=m.TextSpec.events
        def changed(spec):
            yield from original(spec)
            spec.memory[0x8fff0]^=1
        for a,mz,p in self.targets():
            with self.subTest(artifact=a),patch.object(m.TextSpec,'events',changed):
                with self.assertRaisesRegex(ValueError,'physical memory'): m.TextProbe(mz,p).run(dict(string=[65,0]))

    def test_vram_alias_keeps_an_independently_checked_prefix(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                row=m.TextProbe(mz,p).run(dict(segment=0xa800,offset=0xffff,string=[0x81,0x40,0],left=1,fx=0x35),False)
                self.assertFalse(row['terminal']); self.assertGreater(row['stores'],0)

    def test_native_grcg_stack_alias_rejected(self):
        for a,mz,p in self.targets():
            with self.subTest(artifact=a):
                probe=m.TextProbe(mz,p); original=probe.get
                probe.get=lambda r: 0x4001 if r=='SS' else original(r)
                with self.assertRaisesRegex(ValueError,'GRCG frame'): probe.run(dict(string=[0x81,0x40,0]))


if __name__=='__main__': unittest.main()
