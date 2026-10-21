"""Source-only CRT contracts; these tests do not award linked/runtime credit."""
import hashlib
import os
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('TH03_MAINL_CRT_SOURCE', ROOT / 'src/mainl/crt'))

class MainlCrtSourceTests(unittest.TestCase):
    def test_error_mapping_is_named_semantic_data(self):
        constants = dict((k, int(v)) for k, v in re.findall(
            r'^(\w+) equ (\d+)$', (SOURCE / 'crt_errno.inc').read_text(), re.M))
        rows = re.findall(r'^\s*db (\w+) ; DOS (\d+)$',
                          (SOURCE / 'dos_error_map.inc').read_text(), re.M)
        self.assertEqual([int(i) for _, i in rows], list(range(89)))
        data = b'\0\0' + bytes(constants[name] for name, _ in rows)
        self.assertEqual(len(data), 91)
        self.assertEqual(hashlib.sha256(data).hexdigest(),
            '8e70a05d6747dfa521aa7692b5843ef6a6ae1f002553c28fb2267bc8a1630e9c')

    def test_external_errno_words_belong_to_data(self):
        # Regression for the first actual TASM probe: CODE-scoped EXTRNs
        # produced erroneous CS overrides and wrong segment-frame fixups.
        segment = None
        owners = {}
        for line in (SOURCE / 'ioerror.asm').read_text().splitlines():
            line = line.split(';', 1)[0].strip()
            m = re.match(r'(\w+) segment\b', line, re.I)
            if m:
                segment = m.group(1)
            if re.match(r'\w+ ends$', line, re.I):
                segment = None
            if line.lower().startswith('extrn '):
                for name in re.findall(r'(\w+):word', line):
                    owners[name] = segment
        self.assertEqual(owners, {'_errno': '_DATA', '__sys_nerr': '_DATA'})

    def test_executable_segments_have_no_encoded_data_or_padding(self):
        for name in ('h_llsh', 'h_padd', 'n_pcmp', 'ioerror', 'setblock'):
            in_code = False
            for line in (SOURCE / (name + '.asm')).read_text().splitlines():
                line = line.split(';', 1)[0].strip()
                if re.match(r'_TEXT segment\b', line, re.I):
                    in_code = True
                if re.match(r'_TEXT ends$', line, re.I):
                    in_code = False
                if in_code:
                    self.assertFalse(re.search(r'\b(db|dw|dd|org|even|align)\b', line, re.I),
                                     (name, line))

    def test_explicit_function_distance_and_cleanup_contracts(self):
        text = (SOURCE / 'fbrk.c').read_text()
        for declaration in ('int near pascal grow_break', 'int near cdecl _brk',
                            'heap_pointer near cdecl _sbrk', 'int far cdecl setblock'):
            self.assertIn(declaration, text)
        self.assertIn('typedef char huge *heap_pointer;', text)
        self.assertEqual((SOURCE / 'ioerror.asm').read_text().count('    ret 2'), 2)
        self.assertIn('_setblock proc far', (SOURCE / 'setblock.asm').read_text())

    def test_pointer_helpers_keep_all_public_aliases(self):
        for filename, names in {
            'h_llsh.asm': ('N_LXLSH@', 'F_LXLSH@', 'LXLSH@'),
            'h_padd.asm': ('N_PADD@', 'F_PADD@', 'PADD@', 'N_PSUB@', 'F_PSUB@', 'PSUB@'),
            'n_pcmp.asm': ('N_PCMP@',),
        }.items():
            public = set()
            for line in (SOURCE / filename).read_text().splitlines():
                if line.startswith('public '):
                    public.update(x.strip() for x in line[7:].split(','))
            self.assertEqual(public, set(names))

if __name__ == '__main__':
    unittest.main()
