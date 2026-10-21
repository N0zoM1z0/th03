import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cold_replay',ROOT/'scripts/replay_th03_mainl_fullcold_current.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ColdProofTests(unittest.TestCase):
 def setUp(self):self.proof=json.loads((ROOT/'config/mainl_fullcold_current/proof.json').read_text())
 def test_schema(self):module.validate_proof(self.proof)
 def test_false_credits(self):
  for key in module.CREDIT_FLAGS:
   with self.subTest(key=key):
    p=copy.deepcopy(self.proof);p[key]=True
    with self.assertRaises(ValueError):module.validate_proof(p)
 def test_full_counts(self):
  for key in ['rounds','groups','native_phases']:
   with self.subTest(key=key):
    p=copy.deepcopy(self.proof);p[key]-=1
    with self.assertRaises(ValueError):module.validate_proof(p)
 def test_unique_pins(self):
  self.proof['pins'].append(self.proof['pins'][0])
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_fixed_helpers(self):
  self.assertEqual(len(module.FINAL_MANIFESTS),2);self.assertEqual(len(module.VERIFIER_SHA),64);self.assertEqual(len(module.STAGE_SHA),64)
if __name__=='__main__':unittest.main()
