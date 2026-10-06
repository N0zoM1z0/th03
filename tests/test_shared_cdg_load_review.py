import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from lib.pc98 import parse_mz
import review_th03_shared_cdg_load as m


class SharedCDGControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.images = {}
        for art in m.PROFILES:
            path = m.ROOT/f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{art}.exe'
            if path.exists():
                cls.images[art] = parse_mz(path.read_bytes())

    def targets(self):
        if not self.__class__.images:
            self.skipTest('private decoded targets absent')
        return [(art, mz, m.PROFILES[art]) for art, mz in self.__class__.images.items()]

    def test_single_frees_before_open_and_all_opens_before_free(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                single = m.observe(mz, p, 'single', m.scenario(), follow=False)
                all_images = m.observe(mz, p, 'all', m.scenario(), follow=False)
                self.assertEqual([e['name'] for e in single['events'][:3]], ['free', 'free', 'open'])
                self.assertEqual([e['name'] for e in all_images['events'][:3]], ['open', 'free', 'free'])

    def test_word_multiplication_wraps_before_signed_dword_seek(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                r = m.observe(mz, p, 'single', m.scenario(n=-32768, header=m.header(13108).hex()))
                self.assertEqual([e['args'] for e in r['events'] if e['name'] == 'seek'], [[1, 0, 65534]])
                self.assertEqual([e['args'] for e in r['events'] if e['name'] == 'alloc'], [[13108], [52432]])

    def test_equal_segment_handles_are_freed_twice(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                r = m.observe(mz, p, 'free', m.scenario(old=[0x8000, 0x8000]))
                self.assertEqual(r['events'], [dict(name='free', args=[0x8000])]*2)
                self.assertEqual(len(r['stores']), 2)

    def test_all_noalpha_clears_previous_nonzero_flag(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                r = m.observe(mz, p, 'all_noalpha', m.scenario(flag=255))
                self.assertEqual(r['final_flag'], 0)
                self.assertEqual([e['args'] for e in r['events'] if e['name'] == 'alloc'], [[16]])
                self.assertEqual(r['native_entries']['all'], 1)

    def test_empty_header_count_retains_unchecked_segment_words_until_followup(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                s = m.scenario(count=0, header=m.header(count=0, alpha=0xabcd, colors=0xdead).hex())
                r = m.observe(mz, p, 'all', s)
                self.assertFalse(any(e['name'] == 'alloc' for e in r['events']))
                self.assertEqual(r['events'][-2:], [dict(name='free', args=[0xabcd]), dict(name='free', args=[0xdead])])

    def test_failure_replies_and_null_allocations_do_not_abort(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                r = m.observe(mz, p, 'single', m.scenario(status=65535, carry=True, allocations=[0, 0], payload='a17e36c4'))
                reads = [e for e in r['events'] if e['name'] == 'read']
                self.assertEqual([e['args'][2] for e in reads[1:]], [0, 0])
                self.assertEqual(r['events'][-1]['name'], 'close')
                self.assertTrue(any(a == 0 for a, _, _ in r['external_inputs']))

    def test_segment_alias_writes_are_checked_as_physical_inputs(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                r = m.observe(mz, p, 'single', m.scenario(allocations=[p['ds']+0x2000, 0x7000], payload='a17e36c4'))
                self.assertIn(((p['ds']+0x2000)*16, 1, 0xa1), r['external_inputs'])

    def test_push_cs_bridge_mutation_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['start']+11] = 0x90
                with self.assertRaisesRegex(ValueError, 'PUSH CS'):
                    m.analyze(image, p)

    def test_foreign_destination_mutation_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['start']+30] ^= 1
                with self.assertRaisesRegex(ValueError, 'caller'):
                    m.analyze(image, p)

    def test_far_cleanup_mutation_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                image = bytearray(mz.program_image)
                image[p['cs']*16+p['start']+591] ^= 2
                with self.assertRaisesRegex(ValueError, 'cleanup'):
                    m.analyze(image, p)

    def test_stack_segment_alias_rejected(self):
        for art, mz, p in self.targets():
            with self.subTest(artifact=art):
                probe = m.CDGProbe(mz, p, m.scenario())
                original = probe.get
                probe.get = lambda r: 0x4001 if r == 'SS' else original(r)
                with self.assertRaisesRegex(ValueError, 'stack segment'):
                    probe.run('single')

    def test_unexpected_physical_byte_mutation_rejected(self):
        original = m.CDGSpec.invoke
        def changed(spec, name):
            original(spec, name)
            spec.memory[0xefff0] ^= 1
        for art, mz, p in self.targets():
            with self.subTest(artifact=art), patch.object(m.CDGSpec, 'invoke', changed):
                with self.assertRaisesRegex(ValueError, 'physical'):
                    m.observe(mz, p, 'free', m.scenario(), follow=False)

    def test_native_store_order_mutation_rejected(self):
        original = m.CDGSpec.invoke
        def changed(spec, name):
            original(spec, name)
            if name == 'free':
                spec.writes.reverse()
        for art, mz, p in self.targets():
            with self.subTest(artifact=art), patch.object(m.CDGSpec, 'invoke', changed):
                with self.assertRaisesRegex(ValueError, 'writes'):
                    m.observe(mz, p, 'free', m.scenario(), follow=False)


if __name__ == '__main__':
    unittest.main()
