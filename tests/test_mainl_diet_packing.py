import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mainl_diet_packing_replay',ROOT/'scripts/replay_th03_mainl_diet_packing.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class DietPackingProofTests(unittest.TestCase):
 def setUp(self):self.proof=module.load_json(ROOT/'config/mainl_diet_packing/proof.json')
 def test_diagnostic_schema(self):module.validate_proof(self.proof)
 def test_reject_source_credit(self):
  self.proof['source_acceptance']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_reject_exact_credit(self):
  self.proof['exact_acceptance']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_reject_role_conflation(self):
  self.proof['runs'][1]['label']='target_control'
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_reject_duplicate_pin(self):
  self.proof['pins'].append(copy.deepcopy(self.proof['pins'][0]))
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_negative_canonical_result_is_bound(self):
  self.assertEqual([r['label'] for r in self.proof['runs']],['target_control','source_product','complete_source_product'])
  self.assertTrue(all(r['result']['path'] in {p['path'] for p in self.proof['pins']} for r in self.proof['runs']))
if __name__=='__main__':unittest.main()
