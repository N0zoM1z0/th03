#!/usr/bin/env python3
"""Portable source-only positive and negative checks; invokes no native tool."""
from pathlib import Path
import argparse
import copy
import importlib.util
import json
import shutil
import tempfile
import unittest

P = argparse.ArgumentParser()
P.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
P.add_argument('--reference', type=Path)
ARGS, REST = P.parse_known_args()
ROOT = ARGS.root.resolve()
SPEC = importlib.util.spec_from_file_location('op_exit_stage', ROOT / 'scripts/stage_th03_op_exit_helpers.py')
STAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAGE)
CONFIG, INPUTS = STAGE.read_inputs(ROOT)

class SourceChecks(unittest.TestCase):
    def setUp(self):
        scratch = Path.cwd() / '.analysis'
        scratch.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='op-exit-source-test-', dir=scratch)
        self.base = Path(self.temp.name)
        self.root = self.base / 'root'
        for name in [STAGE.CONFIG, *INPUTS]:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, p)

    def tearDown(self):
        self.temp.cleanup()

    def reject_config(self, mutation):
        config = copy.deepcopy(CONFIG)
        mutation(config)
        with self.assertRaises(ValueError):
            STAGE.validate_config(config)

    def test_01_original_bodies(self):
        for unit in CONFIG['units']:
            self.assertEqual(STAGE.sha(INPUTS[unit['source']].replace(b'compat/rec98/', b'')), unit['original_body_sha256'])

    def test_02_three_distinct_physical_producers(self):
        self.assertEqual([u['physical_game_macro'] for u in CONFIG['units']], [2, 1, 3])
        self.assertEqual(len({u['object'] for u in CONFIG['units']}), 3)

    def test_03_literal_forwarding(self):
        data = STAGE.payload(ROOT)
        for unit in CONFIG['units']:
            self.assertEqual(data[unit['original_body']], ('#include "' + unit['source'] + '"\n').encode())
        self.assertEqual(len(data), 13)

    def test_04_source_stage_repeat(self):
        a = STAGE.stage(ROOT, self.base / 'round1')
        b = STAGE.stage(ROOT, self.base / 'round2')
        self.assertEqual(a, b)
        self.assertEqual((a['code_bytes'], a['compiler_invocations']), (133, 0))
        self.assertFalse(a['source_acceptance'] or a['exact_acceptance'])

    def test_05_fresh_output_only(self):
        out = self.base / 'out'
        out.mkdir()
        with self.assertRaisesRegex(ValueError, 'fresh output'):
            STAGE.stage(ROOT, out)

    def test_06_wrong_game(self):
        self.reject_config(lambda c: c['units'][1].update(physical_game_macro=3))

    def test_07_wrong_compiler(self):
        self.reject_config(lambda c: c['units'][1].update(compiler='tasm32'))

    def test_08_wrong_command_flags(self):
        self.reject_config(lambda c: c['units'][0].update(original_command=c['units'][0]['original_command'].replace('-ml', '-ms')))

    def test_09_overlapping_extent(self):
        self.reject_config(lambda c: c['units'][2].update(offset=33))

    def test_10_duplicate_owner(self):
        self.reject_config(lambda c: c['units'].append(c['units'][0]))

    def test_11_false_exact_credit(self):
        self.reject_config(lambda c: c.update(exact_acceptance=True))

    def test_12_false_source_credit(self):
        self.reject_config(lambda c: c.update(source_acceptance=True))

    def test_13_extra_padding_credit(self):
        self.reject_config(lambda c: c['units'][0].update(size=26, compare_size=26))

    def test_14_missing_support_declaration(self):
        self.reject_config(lambda c: c['support_files'].pop(next(iter(c['support_files']))))

    def test_15_body_mutation(self):
        p = self.root / CONFIG['units'][2]['source']
        p.write_bytes(p.read_bytes().replace(b'\tpfend();', b'\t/* omitted */'))
        with self.assertRaisesRegex(ValueError, 'maintained source differs'):
            STAGE.read_inputs(self.root)

    def test_16_missing_source(self):
        (self.root / CONFIG['units'][0]['source']).unlink()
        with self.assertRaisesRegex(ValueError, 'missing input'):
            STAGE.read_inputs(self.root)

    def test_17_fake_compat_stub(self):
        p = self.root / 'compat/rec98/th02/core/initexit.h'
        p.write_text('void game_exit(void) {}\n')
        with self.assertRaisesRegex(ValueError, 'compat source differs'):
            STAGE.read_inputs(self.root)

    def test_18_symlink_input(self):
        p = self.root / CONFIG['units'][0]['source']
        p.unlink()
        p.symlink_to(ROOT / CONFIG['units'][0]['source'])
        with self.assertRaisesRegex(ValueError, 'symlink input'):
            STAGE.read_inputs(self.root)

    def test_19_symlink_output(self):
        out = self.base / 'out'
        out.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink output'):
            STAGE.stage(ROOT, out)

    def test_20_config_mutation(self):
        p = self.root / STAGE.CONFIG
        p.write_bytes(p.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'candidate config differs'):
            STAGE.read_inputs(self.root)

    def test_21_source_only_payload(self):
        for p in STAGE.payload(ROOT):
            self.assertNotIn(Path(p).suffix.lower(), ('.obj', '.exe', '.com', '.map', '.lib'))

    @unittest.skipUnless(ARGS.reference, 'optional reference root not supplied')
    def test_22_original_reference_inputs(self):
        STAGE.verify_reference(ARGS.reference, CONFIG)

    def test_23_wrong_object(self):
        self.reject_config(lambda c: c['units'][0].update(object='obj/th03/exit.obj'))

    def test_24_unsafe_owner_path(self):
        self.reject_config(lambda c: c['units'][0].update(source='../escape.cpp'))

if __name__ == '__main__':
    unittest.main(argv=[__file__, *REST])
