"""Pure retained-input composition checks; no native or payload execution."""
import hashlib,json,sys,unittest
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE if (HERE/'config/targets.toml').exists() else next(p for p in HERE.parents if (p/'config/targets.toml').exists())
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(HERE/'scripts'))
import compose_th03_zun_init as composition
spec=spec_from_file_location('candidate_wrapper_route',HERE/'scripts/replay_th03_zun_launcher.py')
route=module_from_spec(spec);spec.loader.exec_module(route)
class InitComposition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rounds,cls.inputs=composition.prepare_pair(ROOT)
        p=ROOT/composition.WRAPPER_RUN/'round1'
        cls.modules={n:(p/(n+'.com')).read_bytes() for n in ('launcher','transfer_call','transfer_helper')}
        cls.scaffold=(p/'zun.com').read_bytes()
        cls.init=(ROOT/composition.INIT_WORKS[0]/'init.com').read_bytes()
    def test_actual_two_inputs_four_payloads_scaffold_and_known_differences(self):
        self.assertEqual(self.rounds[0][0],self.rounds[1][0]);self.assertEqual(self.rounds[0][0],self.scaffold)
        for n,(data,row) in enumerate(self.rounds):
            self.assertEqual(row['maintained_init_input'],composition.INIT_WORKS[n]+'/init.com')
            self.assertIn(row['maintained_init_input'],self.inputs)
            self.assertEqual(row['other_payloads_unchanged'],4);self.assertTrue(row['outside_init_raw_equal'])
            self.assertEqual(row['different_target_offsets'],composition.DIFFERENCES)
            self.assertEqual(data[0x5c4:0xb32],self.init)
    def test_parent_composition_receipt(self):
        root=ROOT/'.analysis/zun-init-wrapper-composition/zun-init-wrapper-minus2-20261021-v01'
        raw=(root/'receipt.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'39490223a696083e6729e01c7855da1b4f84ba5a3ecb380e33f0aa2da760f924')
        receipt=json.loads(raw)
        self.assertEqual(receipt['native_invocations'],0);self.assertFalse(receipt['new_wrapper_cold_build'])
        self.assertFalse(receipt['exact_acceptance']);self.assertEqual(receipt['different_bytes'],10)
        self.assertEqual([len(row) for row in receipt['runtime']],[7,7]);self.assertTrue(receipt['wrong_transfer_address_rejected'])
        self.assertEqual((root/'round1.com').read_bytes(),self.rounds[0][0])
        self.assertEqual((root/'round2.com').read_bytes(),self.rounds[1][0])
    def test_no_reference_init_dependency(self):
        self.assertFalse(any('bin/th02/zuninit.com' in n for n in self.inputs))
        self.assertIn('src/zun/init.asm',self.inputs)
    def test_reject_wrong_init_size_or_bytes(self):
        for bad in (self.init+b'\0',self.init[:-1],bytes([self.init[0]^1])+self.init[1:]):
            with self.assertRaises(ValueError):composition.compose_init(self.modules,self.scaffold,bad)
    def test_reject_other_wrapper_mutation(self):
        for name in self.modules:
            modules=dict(self.modules);raw=bytearray(modules[name]);raw[0]^=1;modules[name]=bytes(raw)
            with self.assertRaises(ValueError):composition.compose_init(modules,self.scaffold,self.init)
    def test_missing_produced_input_has_no_fallback(self):
        read=composition.read_plain
        def missing(path):
            if str(path).endswith('ZC9467D4/init.com'):raise FileNotFoundError('missing produced init')
            return read(path)
        with patch.object(composition,'read_plain',side_effect=missing):
            with self.assertRaises(FileNotFoundError):composition.prepare_pair(ROOT)
    def test_changed_retained_scaffold_rejected(self):
        read=composition.read_plain
        def changed(path):
            raw=read(path)
            if str(path).endswith('round1/zun.com'):return raw[:-1]+bytes([raw[-1]^1])
            return raw
        with patch.object(composition,'read_plain',side_effect=changed):
            with self.assertRaisesRegex(ValueError,'input identity'):composition.prepare_pair(ROOT)
    def test_opt_in_requires_explicit_retained_wrapper(self):
        for value in (None,'unreviewed'):
            with self.assertRaisesRegex(ValueError,'explicit reviewed'):composition.replay(ROOT,'unused-source-test',value)
    def test_existing_route_defaults_unchanged_and_opt_in_forwarded(self):
        with patch.object(composition,'replay',return_value={'mock':True}) as selected:
            with self.assertRaisesRegex(ValueError,'unsafe run ID'):route.replay('invalid run id')
            selected.assert_not_called()
            self.assertEqual(route.replay('candidate','sol-zun-launcher-20261006-final',True),{'mock':True})
            selected.assert_called_once_with(route.ROOT,'candidate','sol-zun-launcher-20261006-final')
if __name__=='__main__':unittest.main(verbosity=2)
