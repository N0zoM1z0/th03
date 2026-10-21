import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('snow_replay',ROOT/'scripts/replay_th03_mainl_staff_prefix_backend.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class StaffPrefixProofTests(unittest.TestCase):
 def setUp(self):self.proof=json.loads((ROOT/'config/mainl_staff_prefix_backend/proof.json').read_text())
 def test_schema(self):module.validate_proof(self.proof)
 def test_no_acceptance_inflation(self):
  for key in ['source_acceptance','exact_acceptance','source_progress_changed','full_cold_build','runtime_rerun','fresh_product_repeat']:
   with self.subTest(key=key):
    p=copy.deepcopy(self.proof);p[key]=True
    with self.assertRaises(ValueError):module.validate_proof(p)
 def test_phase_count(self):
  self.proof['native_phase_count']=2
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_duplicate_pin(self):
  self.proof['pins'].append(self.proof['pins'][0])
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
if __name__=='__main__':unittest.main()
