import copy,importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('alignment_replay',ROOT/'scripts/replay_th03_mainl_vsync_alignment.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class AlignmentProofTests(unittest.TestCase):
 def setUp(self):self.proof=module.load_json(ROOT/'config/mainl_vsync_alignment/proof.json')
 def test_schema(self):module.validate_proof(self.proof)
 def test_exact_credit_rejected(self):
  self.proof['exact_acceptance']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_source_credit_rejected(self):
  self.proof['source_progress_changed']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_cold_credit_rejected(self):
  self.proof['full_cold_build']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_runtime_credit_rejected(self):
  self.proof['runtime_rerun']=True
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_duplicate_pin_rejected(self):
  self.proof['pins'].append(copy.deepcopy(self.proof['pins'][0]))
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_wrong_native_count_rejected(self):
  self.proof['native_phase_count']=9
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_stage_conflation_rejected(self):
  self.proof['runs'][1]['label']='alignment'
  with self.assertRaises(ValueError):module.validate_proof(self.proof)
 def test_current_sources_bound(self):
  self.assertEqual({r['path'] for r in self.proof['source_bindings']},{'scripts/lib/mainl_vsync_alignment_source.py','src/mainl/display_hardware/vsync_data.asm','src/mainl/display_hardware/cdg_data.asm'})
if __name__=='__main__':unittest.main()
