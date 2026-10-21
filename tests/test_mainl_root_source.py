"""Read-only symbolic ownership checks; no native compiler invocation."""
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lib import mainl_root_source as root
from lib.mainl_staff_source import statements


def checked(row):
    raw = (ROOT / row['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise ValueError('source identity differs: ' + row['path'])
    return raw


class RootSourceTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / 'config/th03_mainl_root_source.json').read_text())
        self.previous = checked(self.c['previous_generated_root'])
        self.free = checked(self.c['free_all_provider'])
        self.source = checked(self.c['source'])
        checked(self.c['composer'])

    def test_full_source_expansion_identity(self):
        out = root.compose(self.previous, self.free, self.source)
        marker = ('include ' + root.SOURCE).encode()
        self.assertEqual(out['th03_mainl.asm'].count(marker), 1)
        expanded = out['th03_mainl.asm'].replace(marker, out[root.SOURCE])
        original = self.previous.replace(root.BEGIN, self.free)
        self.assertEqual(statements(expanded), statements(original))
        self.assertIn(b'@CUTSCENE_SCRIPT_LOAD$QNXC procdesc pascal near', out['th03_mainl.asm'])
        self.assertNotIn(root.BEGIN, out['th03_mainl.asm'])

    def test_complete_procedure_and_table_partition(self):
        starts = re.findall(rb'(?m)^(\S+)\s+proc\s+(near|far)', self.source)
        self.assertEqual(len(starts), 9)
        self.assertEqual([n for n,k in starts if k == b'far'], [b'_main'])
        self.assertEqual(len(re.findall(rb'(?m)^\S+\s+endp', self.source)), 9)
        targets = re.findall(rb'\bdw offset (loc_\w+)', self.source)
        self.assertEqual(targets, [b'loc_9B97', b'loc_9B97', b'loc_9B9F', b'loc_9BA7', b'loc_9B9F', b'loc_9BA7', b'loc_9B97', b'loc_9BAF', b'loc_9BB7'])
        self.assertEqual(self.c['procedure_bytes'] + 2 * len(targets), 2488)
        self.assertFalse(self.c['exact_acceptance'])
        self.assertFalse(self.c['source_progress_changed'])

    def test_abi_and_observed_quirks(self):
        rows = statements(self.source)
        for row in [(b'retf',), (b'retn', b'6'), (b'retn', b'2'),
                    (b'mov', b'byte', b'ptr', b'es:[bx+2],', b"'e'"),
                    (b'mov', b'byte', b'ptr', b'es:[bx+3],', b"'x'"),
                    (b'jbe', b'short', b'loc_9C42'),
                    (b'dec', b'es:[bx+resident_t.story_stage]'),
                    (b'jmp', b'cs:off_9C9F[bx]')]:
            self.assertIn(row, rows)

    def test_changed_instruction_rejected(self):
        altered = self.source.replace(b'xor\tsi, si', b'sub\tsi, si', 1)
        self.assertNotEqual(altered, self.source)
        with self.assertRaises(ValueError): root.compose(self.previous, self.free, altered)

    def test_changed_table_rejected(self):
        altered = self.source.replace(b'dw offset loc_9B97', b'dw offset loc_9B9F', 1)
        with self.assertRaises(ValueError): root.compose(self.previous, self.free, altered)

    def test_padding_or_missing_body_rejected(self):
        with self.assertRaises(ValueError): root.compose(self.previous, self.free, self.source + b'\ndb 90h\n')
        with self.assertRaises(ValueError): root.compose(self.previous, self.free, self.source.replace(b'sub_9F8D\tendp', b''))

    def test_source_boundary_rejected(self):
        with self.assertRaises(ValueError): root.compose(self.previous + root.END, self.free, self.source)
        with self.assertRaises(ValueError): root.compose(self.previous.replace(root.BEGIN, b''), self.free, self.source)

if __name__ == '__main__': unittest.main()
