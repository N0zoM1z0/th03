"""Additive default binding only. No native or acceptance execution."""
import copy,hashlib,tomllib,unittest
from pathlib import Path
from th03_cpu_default_fixture import historical_default_bytes
from lib import th03_yumemi_charge_candidate as charge
from replay_th03_main_exact_units import normalized_code_extents,verify_disjoint_ownership
ROOT=Path(__file__).resolve().parents[1]
class ChargeDefault(unittest.TestCase):
 def setUp(self):
  self.old=tomllib.loads(historical_default_bytes().decode());self.new=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text());self.candidate=tomllib.loads((ROOT/charge.CANDIDATE_PATH).read_text())
 def test_exact_raw_append(self):
  raw=(ROOT/charge.CANDIDATE_PATH).read_bytes();body=raw[raw.index(b'[[units]]'):]
  self.assertEqual((ROOT/'config/th03_main_exact_units.toml').read_bytes(),historical_default_bytes()+b'\n'+body)
 def test_old_owners_and_functions_unchanged(self):
  self.assertEqual(self.new,{**self.old,'units':self.old['units']+self.candidate['units'],'functions':self.old['functions']+self.candidate['functions']})
  self.assertEqual((len(self.old['units']),len(self.old['functions'])),(77,403));self.assertEqual((len(self.new['units']),len(self.new['functions'])),(78,413))
  extents={u['id']:normalized_code_extents(u,self.new['segment']) for u in self.new['units']};verify_disjoint_ownership(extents)
  flat=[e for es in extents.values() for e in es];self.assertEqual((len(flat),sum(e['size'] for e in flat)),(87,66843))
 def test_exact_charge_default_binding(self):
  before=copy.deepcopy(self.new);bound,original=charge.bind_default(self.new);self.assertEqual(bound,self.new);self.assertEqual(before,self.new)
 def test_changed_owner_rejected(self):
  bad=copy.deepcopy(self.new);bad['units'][-1]['code_extents'][0]['size']+=1
  with self.assertRaises(ValueError):charge.bind_default(bad)
 def test_changed_prior_scope_rejected(self):
  bad=copy.deepcopy(self.new);bad['units'][0]['size']+=1
  with self.assertRaises(ValueError):charge.bind_default(bad)
 def test_duplicate_charge_candidate_rejected(self):
  with self.assertRaises(ValueError):charge.bind_candidate(self.new,self.candidate,charge.CANDIDATE_PATH)
if __name__=='__main__':unittest.main()
