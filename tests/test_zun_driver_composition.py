"""Actual maintained -2/-4 input composition; no native or payload execution."""

# This integration suite needs an optional archived native run.
from pathlib import Path as _ArchivePath
import unittest as _archive_unittest
if not (_ArchivePath(__file__).resolve().parents[1] / '.analysis/th03-zun-launcher/sol-zun-launcher-cached-final-20261006/receipt.json').is_file():
    raise _archive_unittest.SkipTest("archived native fixtures unavailable")

import sys,unittest
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1]
ROOT=HERE if (HERE/'config/targets.toml').exists() else next(p for p in HERE.parents if (p/'config/targets.toml').exists())
sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(HERE/'scripts'))
import compose_th03_zun_driver as composition
spec=spec_from_file_location('driver_wrapper_route',HERE/'scripts/replay_th03_zun_launcher.py')
route=module_from_spec(spec);spec.loader.exec_module(route)
class DriverComposition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rounds,cls.inputs=composition.prepare_pair(ROOT)
        cls.init_rounds,_=composition.init.prepare_pair(ROOT)
        p=ROOT/composition.init.WRAPPER_RUN/'round1'
        cls.modules={n:(p/(n+'.com')).read_bytes() for n in ('launcher','transfer_call','transfer_helper')}
        cls.driver=(ROOT/composition.DRIVER_WORKS[0]/'driver.com').read_bytes()
    def test_actual_two_produced_inputs_and_outside_preservation(self):
        self.assertEqual(self.rounds[0][0],self.rounds[1][0])
        for i,(data,row) in enumerate(self.rounds):
            base,old=self.init_rounds[i]
            self.assertEqual(row['maintained_driver_input'],composition.DRIVER_WORKS[i]+'/driver.com')
            self.assertEqual(row['maintained_init_input'],old['maintained_init_input'])
            self.assertIn(row['maintained_driver_input'],self.inputs)
            self.assertEqual(data[:0x32a2],base[:0x32a2]);self.assertEqual(data[0x4322:],base[0x4322:])
            self.assertEqual(data[0x32a2:0x4322],self.driver)
            self.assertEqual(row['other_payloads_unchanged'],4);self.assertEqual(row['retained_payloads'],3)
            self.assertEqual(row['different_target_offsets'],composition.init.DIFFERENCES)
    def test_no_retained_driver_source_dependency(self):
        self.assertFalse(any('libs/sprite16' in n or 'master.lib/macros.inc' in n for n in self.inputs))
        for n in ('driver.asm','driver_data.inl','driver_hardware.inc'):self.assertIn('src/zun/'+n,self.inputs)
    def test_wrong_driver_size_or_bytes_rejected(self):
        for bad in (self.driver[:-1],self.driver+b'\0',bytes([self.driver[0]^1])+self.driver[1:]):
            with self.assertRaises(ValueError):composition.compose_driver(self.modules,self.init_rounds[0][0],bad)
    def test_wrapper_mutation_rejected(self):
        for name in self.modules:
            modules=dict(self.modules);raw=bytearray(modules[name]);raw[0]^=1;modules[name]=bytes(raw)
            with self.assertRaises(ValueError):composition.compose_driver(modules,self.init_rounds[0][0],self.driver)
    def test_either_missing_driver_has_no_fallback(self):
        read=composition.read_plain
        for work in composition.DRIVER_WORKS:
            def missing(path):
                if str(path).endswith(work+'/driver.com'):raise FileNotFoundError('missing produced driver')
                return read(path)
            with patch.object(composition,'read_plain',side_effect=missing):
                with self.assertRaises(FileNotFoundError):composition.prepare_pair(ROOT)
    def test_changed_receipt_or_source_rejected(self):
        read=composition.read_plain
        for suffix in (composition.DRIVER_RUNS[1]+'/completion.json','src/zun/driver_data.inl'):
            def changed(path):
                raw=read(path)
                return raw+b' ' if str(path).endswith(suffix) else raw
            with patch.object(composition,'read_plain',side_effect=changed):
                with self.assertRaisesRegex(ValueError,'input identity'):composition.prepare_pair(ROOT)
    def test_explicit_retained_wrapper_and_safe_name_required(self):
        for run,cached in (('bad id','sol-zun-launcher-20261006-final'),('unused',None),('unused','other')):
            with self.assertRaises(ValueError):composition.replay(ROOT,run,cached)
    def test_opt_in_hook_preserves_old_default_and_init_mode(self):
        with patch.object(composition,'replay',return_value={'driver':True}) as selected:
            with self.assertRaisesRegex(ValueError,'unsafe run ID'):route.replay('invalid run id')
            selected.assert_not_called()
            self.assertEqual(route.replay('candidate','sol-zun-launcher-20261006-final',False,True),{'driver':True})
            selected.assert_called_once_with(route.ROOT,'candidate','sol-zun-launcher-20261006-final')
            with self.assertRaisesRegex(ValueError,'choose one'):route.replay('unused',None,True,True)
        with patch.object(composition.init,'replay',return_value={'init':True}) as old:
            self.assertEqual(route.replay('candidate','sol-zun-launcher-20261006-final',True),{'init':True})
            old.assert_called_once()
if __name__=='__main__':unittest.main(verbosity=2)
