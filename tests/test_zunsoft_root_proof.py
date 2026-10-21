import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('zunsoft_replay',ROOT/'scripts/replay_th03_zunsoft_root.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ZunsoftProofTests(unittest.TestCase):
 def setUp(self):self.p=json.loads((ROOT/'config/zunsoft_root/proof.json').read_text())
 def test_schema(self):module.validate_proof(self.p)
 def test_false_credits(self):
  for k in module.CREDIT_FLAGS:
   with self.subTest(key=k):
    q=copy.deepcopy(self.p);q[k]=True
    with self.assertRaises(ValueError):module.validate_proof(q)
 def test_bounded_counts(self):
  for k in ['native_phases','root_procedures','root_code_bytes','root_data_bytes','root_bss_bytes','runtime_images','runtime_calls']:
   with self.subTest(key=k):
    q=copy.deepcopy(self.p);q[k]+=1
    with self.assertRaises(ValueError):module.validate_proof(q)
 def test_unique_pins(self):
  self.p['pins'].append(self.p['pins'][0])
  with self.assertRaises(ValueError):module.validate_proof(self.p)
 def test_manifest_binding(self):
  self.p['manifest_sha256']='0'*64
  with self.assertRaises(ValueError):module.validate_proof(self.p)
 def test_verifier_binding(self):
  self.p['verifier_sha256']='0'*64
  with self.assertRaises(ValueError):module.validate_proof(self.p)
 def test_source_closure(self):
  self.p['maintained_sources'].pop(next(iter(self.p['maintained_sources'])))
  with self.assertRaises(ValueError):module.validate_proof(self.p)
if __name__=='__main__':unittest.main()
