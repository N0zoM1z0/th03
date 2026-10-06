import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_cdg_draw as m


class SharedDrawControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images = {}
        for art in m.PROFILES:
            p = m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{art}.exe'
            if p.exists():
                cls.images[art] = parse_mz(p.read_bytes())

    def targets(self):
        if not self.images:
            self.skipTest('private decoded targets absent')
        return [(a, image, m.PROFILES[a]) for a, image in self.images.items()]

    def test_native_patch_destinations_and_width_are_owned(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['starts'][0]+32] ^= 1
                with self.assertRaisesRegex(ValueError, 'SMC writer'):
                    m.analyze(image, p)

    def test_immediate_patch_destination_must_stay_mov(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                # An arithmetic encoding has the same length as MOV DX.
                image[p['cs']*16+p['starts'][0]+94] = 0x05
                with self.assertRaisesRegex(ValueError, 'SMC destination'):
                    m.analyze(image, p)

    def test_lut_and_foreign_bindings_cannot_be_inherited(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['starts'][1]+95] ^= 1
                with self.assertRaisesRegex(ValueError, 'lookup binding'):
                    m.analyze(image, p)
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['starts'][0]+12] ^= 1
                with self.assertRaisesRegex(ValueError, 'color caller'):
                    m.analyze(image, p)

    def test_natural_even_mutation_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['starts'][2]+113] = 0
                with self.assertRaisesRegex(ValueError, 'EVEN'):
                    m.analyze(image, p)

    def test_forward_dword_crosses_offset_boundary_as_one_store(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                s = m.scenario(left=-1)
                probe = m.DrawProbe(mz, p, s)
                probe.run('alpha', s)
                first = next(e for e in probe.trace if e['kind'] == 'store')
                self.assertEqual((first['address'], first['width']), (0xb7fff, 4))
                r = m.observe(mz, p, 'alpha', s)
                self.assertEqual(r['sequence'][0]['patches'][1]['value'], 65535)

    def test_hflip_lut_is_an_explicit_fixture_and_df_is_preserved(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                s = m.scenario(lookup='identity', df=True)
                probe = m.DrawProbe(mz, p, s)
                probe.run('hflip', s)
                first = next(e for e in probe.trace if e['kind'] == 'store')
                self.assertEqual((first['address'], first['width'], first['value']), (0xa8003, 1, 23))
                self.assertTrue(probe.get('EFLAGS') & 0x400)
                self.assertEqual(probe.get('FS'), 0x7000)
                m.observe(mz, p, 'hflip', s)

    def test_zero_width_keeps_two_nonterminal_prefixes_and_empty_copy_return(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                s = m.scenario(width=0)
                for name, count, ports in [('alpha', 391, 1), ('hflip', 327, 0), ('noalpha', 0, 0)]:
                    r = m.observe(mz, p, name, s, sequence=[(name, s)], prefix=name != 'noalpha')
                    row = r['sequence'][0]
                    self.assertEqual((row['graph_stores'], len(row['ports'])), (count, ports))
                    self.assertEqual(row['terminal'], name == 'noalpha')

    def test_mixed_reentry_preserves_hflip_fs_and_updated_df(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                first = m.scenario(df=True, width=3, bottom=160)
                later = m.scenario(df=False, width=2, bottom=80)
                r = m.observe(mz, p, 'hflip', first,
                              sequence=[('hflip', first), ('alpha', first), ('noalpha', later), ('hflip', later)])
                self.assertEqual([c['fs'] for c in r['sequence']], [0x7000]*4)
                self.assertTrue(all(c['terminal'] for c in r['sequence']))

    def test_wrong_smc_immediate_value_rejected(self):
        original = m.DrawSpec.store
        def changed(spec, at, width, value, code=False):
            original(spec, at, width, value+1 if code else value, code)
        for art, mz, p in self.targets():
            with self.subTest(artifact=art), patch.object(m.DrawSpec, 'store', changed):
                with self.assertRaisesRegex(ValueError, 'ordered scalar'):
                    m.observe(mz, p, 'alpha', m.scenario())

    def test_complete_memory_guard_rejects_extra_physical_byte(self):
        original = m.DrawSpec.invoke
        def changed(spec, *args, **kw):
            original(spec, *args, **kw)
            spec.memory[0x8fff0] ^= 1
        for art, mz, p in self.targets():
            with self.subTest(artifact=art), patch.object(m.DrawSpec, 'invoke', changed):
                with self.assertRaisesRegex(ValueError, 'physical'):
                    m.observe(mz, p, 'noalpha', m.scenario())

    def test_stack_segment_alias_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                probe = m.DrawProbe(mz, p, m.scenario())
                original = probe.get
                probe.get = lambda r: 0x4001 if r == 'SS' else original(r)
                with self.assertRaisesRegex(ValueError, 'SS alias'):
                    probe.run('alpha', m.scenario())


if __name__ == '__main__':
    unittest.main()
