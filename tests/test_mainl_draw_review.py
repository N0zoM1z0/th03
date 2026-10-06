"""Complete drawing scopes, shared return tails, native GDC frames and explicit devices."""
from contextlib import redirect_stderr
from importlib.util import find_spec
import io
from pathlib import Path
import struct
import sys
from types import SimpleNamespace
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_th03_mainl_draw import (OWN_RANGES, CONTEXT, ALIGNMENT, INTERIOR, NEAR, TABLE,
                                   table_entry, analyze, DrawProbe, Scalar)


def fixture():
    data = bytearray(0xe3f0 + 0x700)
    for _, start, size, cleanup in OWN_RANGES + CONTEXT:
        data[start:start + size] = b'\x90' * size
        tail = b'\xc3' if cleanup == 'near' else b'\xca' + struct.pack('<H', cleanup) if cleanup else b'\xcb'
        data[start + size - len(tail):start + size] = tail
    for address, value in (ALIGNMENT | INTERIOR).items():
        data[address] = value
    for address, target in NEAR.items():
        data[address:address + 3] = b'\xe8' + struct.pack('<h', target - address - 3)
    data[TABLE:TABLE + 1024] = b''.join(table_entry(value) for value in range(256))
    return data


def jump(address, target):
    return b'\xe9' + struct.pack('<h', target - address - 3)


class DrawBoundaryTests(unittest.TestCase):
    def test_complete_bodies_shared_tails_and_cleanup(self):
        observed = analyze(fixture())
        self.assertEqual(observed['new_extent_bytes'], 1680)
        self.assertEqual(observed['prior_context_bytes'], 11)
        with self.assertRaisesRegex(ValueError, 'complete body'):
            analyze(fixture()[:0x2d31])
        for address in (0xfe8, 0x162f, 0x16fd, 0x1755, 0x175c, 0x2c6b, 0x2d2f, 0xc70):
            data = fixture()
            data[address] = 0x90
            with self.assertRaisesRegex(ValueError, 'terminal cleanup'):
                analyze(data)
        data = fixture()
        data[0xf58] = 0xc3
        with self.assertRaisesRegex(ValueError, 'interior cleanup'):
            analyze(data)

    def test_native_edges_exclude_operands_table_and_neighbors(self):
        for code, message in ((b'\xe8\x00\x00', 'unknown native call'), (b'\xff\xd0', 'unknown indirect'),
                              (b'\x9a\x00\x00\x00\x00', 'unknown far'),
                              (jump(0xf58, 0xf59), 'branch enters'), (jump(0xf58, TABLE), 'branch enters')):
            data = fixture()
            data[0xf58:0xf58 + len(code)] = code
            with self.assertRaisesRegex(ValueError, message):
                analyze(data)
        data = fixture()
        data[0x1642:0x1644] = b'\x77\xe8'  # Complete caller can branch into its shared RETF10 tail.
        analyze(data)

    def test_device_sites_producers_and_all_table_entries(self):
        for code, address, message in ((b'\xcd\x21', 0x175a, 'BIOS site'), (b'\xcd\x18', 0xf58, 'BIOS site'),
                                       (b'\xe7\x7c', 0xf74, 'port/site/width'), (b'\xe6\xa9', 0xfbe, 'port/site/width'),
                                       (b'\xe4\xa0', 0xf58, 'port/site/width')):
            data = fixture()
            data[address:address + len(code)] = code
            with self.assertRaisesRegex(ValueError, message):
                analyze(data)
        for address in (0xfeb, 0x1683, 0x175d, 0x2cb5):
            data = fixture()
            data[address] = 0
            with self.assertRaisesRegex(ValueError, 'producer alignment'):
                analyze(data)
        for value in range(256):
            data = fixture()
            data[TABLE + value * 4] ^= 1
            with self.assertRaisesRegex(ValueError, 'packed-pixel table'):
                analyze(data)


@unittest.skipUnless(find_spec('unicorn'), 'optional Unicorn unavailable')
class DrawRuntimeTests(unittest.TestCase):
    def probe(self, code=b'', address=0xf58, patches=(), scenario=None):
        __import__('unicorn')
        data = fixture()
        meta = analyze(data)
        data[address:address + len(code)] = code
        for address, code in patches:
            data[address:address + len(code)] = code
        return DrawProbe(SimpleNamespace(program_image=data, relocations=[]), scenario or {}, meta)

    def test_four_real_near_frames_and_bare_helper_rejection(self):
        p = self.probe(jump(0x1700, 0x173a), 0x1700)
        p.run('scroll', [17])
        self.assertEqual(dict(p.native), dict(scroll=1, gdc=4))
        for name in ('gdc', 'clipout', 'noclipout'):
            with self.assertRaisesRegex(ValueError, 'complete public caller'):
                p.run(name)
        with self.assertRaisesRegex(ValueError, 'native entry frame'):
            self.probe(jump(0xf58, 0xc66)).run('gaiji', [15, 0, 0, 0])
        with self.assertRaisesRegex(ValueError, 'native return frame'):
            self.probe(b'\x83\xc4\x02' + jump(0xf5b, 0xfe8)).run('gaiji', [15, 0, 0, 0])

    def test_unknown_services_ports_font_latches_and_whole_store_spans(self):
        for code, message in ((b'\xcd\x18', 'BIOS request/site'), (b'\xe6\x7c', 'output port/site/width'),
                              (b'\xe4\xa9', 'input port/site/width'),
                              (b'\xc7\x06\x28\x05\x01\x00', 'outside declared'),
                              (b'\xb8\x00\x90\x8e\xc0\x26\xc7\x06\x00\x00\x34\x12', 'outside declared')):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaisesRegex(ValueError, message):
                    self.probe(code).run('gaiji', [15, 0, 0, 0])
            self.assertEqual(stderr.getvalue(), '')
        with self.assertRaisesRegex(ValueError, 'font latch/mode'):
            self.probe(jump(0xf58, 0xfbe), patches=[(0xfbe, b'\xe4\xa9')]).run('gaiji', [15, 0, 0, 0])
        with self.assertRaisesRegex(ValueError, 'GRCG mode'):
            self.probe(jump(0xf58, 0xf74), patches=[(0xf74, b'\xe6\x7c')]).run('gaiji', [15, 0, 0, 0])
        p = self.probe(b'\xb4\x40', 0x1758, [(0x175a, b'\xcd\x18')])
        p.run('show')
        self.assertEqual(p.events[0]['ax_request'], 0x4011)

    def test_budget_stale_completion_and_segment_aliases(self):
        p = self.probe(jump(0xf58, 0xfe8))
        p.run('gaiji', [15, 0, 0, 0])
        p.uc.mem_write(p.code + 0xf58, b'\xeb\x00\xeb\xfe')
        with self.assertRaisesRegex(ValueError, 'terminal/budget'):
            p.run('gaiji', [15, 0, 0, 0], budget=50)
        with self.assertRaisesRegex(ValueError, 'terminal segment alias'):
            self.probe(b'\xea\x10\xff\xff\x1f').run('gaiji', [15, 0, 0, 0])
        with self.assertRaisesRegex(ValueError, 'CODE/stack segment alias'):
            self.probe(b'\xea\x68\x0f\xff\x1f').run('gaiji', [15, 0, 0, 0])
        with self.assertRaisesRegex(ValueError, 'instruction boundaries'):
            self.probe(jump(0xf58, TABLE)).run('gaiji', [15, 0, 0, 0])
        p = self.probe(address=0x1700, patches=[(0x1720, b'\xeb\x00\xe4\xa0\x84\xc1\x74\xf8')], scenario=dict(gdc_status=[0]))
        with self.assertRaisesRegex(ValueError, 'terminal/budget'):
            p.run('scroll', [17], budget=1000)
        self.assertEqual((p.status_index, p.get('IP'), len(p.frames)), (242, 0x1720, 1))
        self.assertFalse(p.stop)
        self.assertFalse(p.writes)
        self.assertTrue(all(event['direction'] == 'in' for event in p.ports))

    def test_scalar_cld_negative_source_adjustment_and_carry_direction(self):
        p = self.probe(scenario=dict(df=True, flags=0x203, source_values=[[0x5000, 0xfffc, [0xf0] * 4], [0x5000, 4, [0x0f] * 4]]))
        model = Scalar(p)
        model.run('pack', [8, 0, 0x5000, 400, 0])
        self.assertTrue(model.flags & 1024)
        model.run('pack', [16, 0, 0x5000, 0, 0xfff8])
        self.assertFalse(model.flags & 1024)
        self.assertEqual([value for _, _, value in model.writes], [0xaa] * 4)
        model = Scalar(p)
        model.run('gaiji', [15, 0, 0, 0])
        self.assertEqual(model.low, 1)
        self.assertFalse(model.ports[0]['live_if'])
        self.assertTrue(model.ports[1]['live_if'])
        self.assertEqual(model.writes[1][0], 0xa8000 + 0xfffe)
        self.assertEqual(model.writes[2][0], 0xa8000 + 76)

    def test_scalar_scroll_split_and_real_ready_condition(self):
        p = self.probe(scenario=dict(gdc_status=[0x80, 0, 4], zoom=0x4000))
        model = Scalar(p)
        model.run('scroll', [400])
        self.assertEqual(model.status_index, 3)
        self.assertEqual(dict(model.native), dict(scroll=1, gdc=4))
        self.assertEqual([event['value'] for event in model.ports if event['direction'] == 'out'],
                         [0x70, 0x80, 0x3e, 0, 0x40, 0, 0, 0, 0x59])


if __name__ == '__main__':
    unittest.main()
