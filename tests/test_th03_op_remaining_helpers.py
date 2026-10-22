#!/usr/bin/env python3
"""Source-only validation and negative controls. No native tool or model execution."""
from pathlib import Path
import argparse
import copy
import importlib.util
import shutil
import tempfile
import unittest

P = argparse.ArgumentParser()
P.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
P.add_argument('--reference', type=Path)
P.add_argument('--scratch', type=Path, default=Path.cwd()/'.analysis'/'op-remaining-source-tests')
ARGS, REST = P.parse_known_args()
ROOT = ARGS.root.resolve()
SPEC = importlib.util.spec_from_file_location('op_remaining_stage', ROOT / 'scripts/stage_th03_op_remaining_helpers.py')
STAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STAGE)
CONFIG, INPUTS = STAGE.read_inputs(ROOT)

class SourceChecks(unittest.TestCase):
    def setUp(self):
        ARGS.scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='source-test-', dir=ARGS.scratch)
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

    def test_02_five_distinct_physical_producers(self):
        self.assertEqual([u['physical_game_macro'] for u in CONFIG['units']], [2,2,3,3,3])
        self.assertEqual([u['language'] for u in CONFIG['units']], ['c','c','cpp','cpp','cpp'])
        self.assertEqual(len({u['object'] for u in CONFIG['units']}), 5)

    def test_03_literal_forwarding(self):
        data = STAGE.payload(ROOT)
        for u in CONFIG['units']:
            self.assertEqual(data[u['wrapper']], ('#include "'+u['original_body']+'"\n').encode())
            self.assertEqual(data[u['original_body']], ('#include "'+u['source']+'"\n').encode())
        self.assertEqual(len(data), len(INPUTS)+10)

    def test_04_source_stage_repeat(self):
        a = STAGE.stage(ROOT, self.base/'round1')
        b = STAGE.stage(ROOT, self.base/'round2')
        self.assertEqual(a,b)
        self.assertEqual((a['code_bytes'],a['original_producer_context_bytes'],a['compiler_invocations']),(247,2,0))
        self.assertFalse(a['source_acceptance'] or a['exact_acceptance'])

    def test_05_fresh_output_only(self):
        out = self.base/'out';out.mkdir()
        with self.assertRaisesRegex(ValueError,'fresh output'):
            STAGE.stage(ROOT,out)

    def test_06_wrong_game(self):
        self.reject_config(lambda c:c['units'][0].update(physical_game_macro=3))
    def test_07_c_not_cpp(self):
        self.reject_config(lambda c:c['units'][0].update(language='cpp'))
    def test_08_wrong_compiler(self):
        self.reject_config(lambda c:c['units'][0].update(compiler='bcc'))
    def test_09_changed_flags(self):
        self.reject_config(lambda c:c['units'][0].update(original_command=c['units'][0]['original_command'].replace('-ml','-ms')))
    def test_10_wrong_extent(self):
        self.reject_config(lambda c:c['units'][1].update(offset=0x67))
    def test_11_duplicate_owner(self):
        self.reject_config(lambda c:c['units'].append(c['units'][0]))
    def test_12_false_exact_credit(self):
        self.reject_config(lambda c:c.update(exact_acceptance=True))
    def test_13_false_source_credit(self):
        self.reject_config(lambda c:c.update(source_acceptance=True))
    def test_14_mode_nop_not_code(self):
        self.reject_config(lambda c:c['units'][0].update(size=30,compare_size=30))
    def test_15_pmd_nop_not_code(self):
        self.reject_config(lambda c:c['units'][1].update(size=58,compare_size=58))
    def test_16_polar_alignment_not_code(self):
        self.reject_config(lambda c:c['units'][2].update(size=27,compare_size=27))
    def test_17_tail_context_cannot_disappear(self):
        self.reject_config(lambda c:c['units'][0].update(original_producer_context=[]))
    def test_18_tail_context_cannot_claim_code(self):
        self.reject_config(lambda c:c['units'][0]['original_producer_context'][0].update(function_code_credit=True))
    def test_19_missing_support_declaration(self):
        self.reject_config(lambda c:c['support_files'].pop(next(iter(c['support_files']))))
    def test_20_body_mutation(self):
        p=self.root/CONFIG['units'][4]['source'];p.write_bytes(p.read_bytes().replace(b'\tgraph_start();',b'\t/* omitted */'))
        with self.assertRaisesRegex(ValueError,'maintained source differs'): STAGE.read_inputs(self.root)
    def test_21_missing_source(self):
        (self.root/CONFIG['units'][0]['source']).unlink()
        with self.assertRaisesRegex(ValueError,'missing input'): STAGE.read_inputs(self.root)
    def test_22_fake_compat_stub(self):
        p=self.root/'compat/rec98/th02/snd/snd.h';p.write_text('void fake(void) {}\n')
        with self.assertRaisesRegex(ValueError,'compat source differs'): STAGE.read_inputs(self.root)
    def test_23_symlink_input(self):
        p=self.root/CONFIG['units'][0]['source'];p.unlink();p.symlink_to(ROOT/CONFIG['units'][0]['source'])
        with self.assertRaisesRegex(ValueError,'symlink input'): STAGE.read_inputs(self.root)
    def test_24_symlink_output(self):
        out=self.base/'out';out.symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink output'): STAGE.stage(ROOT,out)
    def test_25_config_mutation(self):
        p=self.root/STAGE.CONFIG;p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaisesRegex(ValueError,'candidate config differs'): STAGE.read_inputs(self.root)
    def test_26_source_only_payload(self):
        for p in STAGE.payload(ROOT): self.assertNotIn(Path(p).suffix.lower(),('.obj','.exe','.com','.map','.lib'))
    @unittest.skipUnless(ARGS.reference,'optional reference root not supplied')
    def test_27_original_reference_inputs(self):
        STAGE.verify_reference(ARGS.reference,CONFIG)
    def test_28_wrong_object(self):
        self.reject_config(lambda c:c['units'][0].update(object='obj/th03/snd_kaja.obj'))
    def test_29_unsafe_source_path(self):
        self.reject_config(lambda c:c['units'][0].update(source='../escape.c'))
    def test_30_pascal_kaja(self):
        self.reject_config(lambda c:c['units'][3].update(calling_convention='far cdecl, RETF'))
    def test_31_original_nop_cannot_be_removed(self):
        p=self.root/CONFIG['units'][0]['source'];p.write_bytes(p.read_bytes().replace(b'#pragma codestring "\\x90"\n',b''))
        with self.assertRaisesRegex(ValueError,'maintained source differs'): STAGE.read_inputs(self.root)
    def test_32_original_pragmas_cannot_change(self):
        p=self.root/CONFIG['units'][0]['source'];p.write_bytes(p.read_bytes().replace(b'-WX ',b''))
        with self.assertRaisesRegex(ValueError,'maintained source differs'): STAGE.read_inputs(self.root)
    def test_33_polar_original_signed_arithmetic(self):
        self.assertIn(b'(static_cast<long>(radius) * ratio) >> 8',INPUTS[CONFIG['units'][2]['source']])
    def test_34_all_text_ascii_utf8_without_transcoding(self):
        for raw in INPUTS.values(): self.assertEqual(raw.decode('ascii').encode('utf-8'),raw)
    def test_35_target_calling_convention(self):
        self.reject_config(lambda c:c['units'][2].update(calling_convention='far pascal, RETF 2'))
    def test_36_alignment_context_cannot_claim_code(self):
        self.reject_config(lambda c:c['units'][2]['excluded_linker_alignment'][0].update(function_code_credit=True))

if __name__ == '__main__':
    unittest.main(argv=[__file__,*REST])
