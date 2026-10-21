"""Source-only aggregate contracts; no native execution or exactness credit."""
import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = Path(os.environ.get('TH03_MAINL_COLD_PAYLOAD', ROOT))
CONTEXT = PAYLOAD / 'config/mainl_cold_context'

class MainlColdSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = PAYLOAD / 'scripts/stage_th03_mainl_cold.py'
        spec = importlib.util.spec_from_file_location('mainl_cold_stage', path)
        cls.stage = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.stage)
        cls.files, cls.owners, cls.stages, cls.graph, cls.archive = cls.stage.compose_all(CONTEXT)

    def test_no_retained_project_binaries(self):
        forbidden = {'.obj', '.exe', '.map', '.lib', '.dll', '.com'}
        self.assertFalse(any(Path(n).suffix.lower() in forbidden for n in self.files))
        self.assertEqual(len(self.files), 1881)

    def test_original_order_and_first_use_flags(self):
        self.assertEqual(self.graph, json.loads((CONTEXT / 'object_graph.json').read_text()))
        self.assertEqual(len(self.graph), 35)
        self.assertEqual(sum(r['kind'] == 'tcc' for r in self.graph), 30)
        self.assertEqual(sum(r['kind'] == 'tasm' for r in self.graph), 5)
        scoredat = next(r for r in self.graph if r['output'].endswith('/scoredat.obj'))
        self.assertEqual((scoredat['game'], scoredat['binary']), (3, 'O'))
        self.assertEqual(self.graph[14]['output'], 'obj/th03/vector_far.obj')

    def test_heap_and_current_composers_are_not_replaced_by_carrier(self):
        names = [r['name'] for r in self.stages]
        for name in ('maintained heap', 'maintained graphics and staff split',
                     'maintained root', 'maintained PI decoder', 'maintained resources',
                     'maintained archive_io', 'maintained display_hardware',
                     'maintained root_tail', 'maintained linked game'):
            self.assertIn(name, names)
        self.assertLess(names.index('maintained heap'), names.index('maintained linked game'))
        text = (PAYLOAD / 'scripts/stage_th03_mainl_cold.py').read_text()
        self.assertNotIn('MLG12', text)

    def test_generated_sprite_context_is_explicit(self):
        data = (CONTEXT / 'flake.asp').read_bytes()
        self.assertEqual(len(data), 1239)
        self.assertNotIn(b'\r', data)
        self.assertEqual(len(data.replace(b'\r\n', b'\n')), 1239)
        self.assertEqual(self.files['th03/sprites/flake.asp'], self.stage.crlf(data))
        self.assertEqual(len(self.files['th03/sprites/flake.asp']), 1281)

    def test_original_codestring_remains_context(self):
        self.assertIn(b'#pragma codestring "\\x90"', self.files['src/mainl/linked_game/input_sense.cpp'])

    def test_fixed_source_date_and_reference(self):
        self.assertEqual(self.stage.REV, 'b6ba5b0a529edbb31efdf8c0e939263804f8ee47')
        self.assertEqual(self.archive, '9f7a4eb17f24ae2d99adaba4320f6c46f4fc8d659f9b784f6d8e5f3af99bf705')
        self.assertEqual(self.stage.STAMP, 1792540800000000000)

if __name__ == '__main__':
    unittest.main()
