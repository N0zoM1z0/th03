from pathlib import Path
import copy,importlib.util,unittest
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'scripts/replay_th03_op_fullcold.py'
if not FILE.exists():FILE=Path(__file__).with_name('replay_th03_op_fullcold.py')
spec=importlib.util.spec_from_file_location('fullcold_replay',FILE);r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def proof():return dict(schema='th03-op-fullcold-proof-v1',rounds=2,native_phases=56,project_objects_per_round=27,source_owners=34,source_bytes=12436,cohort_bytes=9530,**{k:False for k in r.FLAGS})
def report():
 owners=[dict(id='owner'+str(i),size=1,ordered_relocations_equal=True) for i in range(33)];owners[0]['size']=9498;owners.append(dict(id='op-character-selection',size=2906,ordered_relocations_equal=False))
 return dict(diagnostic_checks_pass=True,source_integrity_checked=True,all_owners_raw_pass=True,all_owners_ordered_pass=False,candidate_cohort_raw_and_ordered_pass=True,candidate_cohort_units=33,candidate_cohort_bytes=9530,owners=owners,whole_file_equal=False,whole_program=dict(different_bytes=6),whole_ordered_relocations=dict(equal=False,different_positions=313),raw_repeat_pairs=[{}]*29,two_round_raw_repeat_equal=True,**{k:False for k in r.FLAGS})
class EvidenceTests(unittest.TestCase):
 def test_valid_scope(self):r.validate_proof(proof());r.validate_report(report(),2)
 def test_no_credit(self):
  for key in r.FLAGS:
   p=proof();p[key]=True
   with self.assertRaises(ValueError):r.validate_proof(p)
 def test_wrong_scope(self):
  for key in ('rounds','native_phases','project_objects_per_round','source_owners','source_bytes','cohort_bytes'):
   p=proof();p[key]+=1
   with self.assertRaises(ValueError):r.validate_proof(p)
 def test_selection_negative_preserved(self):
  x=report();x['owners'][-1]['ordered_relocations_equal']=True
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_raw_failure(self):
  x=report();x['all_owners_raw_pass']=False
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_cohort_failure(self):
  x=report();x['candidate_cohort_raw_and_ordered_pass']=False
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_whole_raw_negative(self):
  x=report();x['whole_program']['different_bytes']=0
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_order_negative(self):
  x=report();x['whole_ordered_relocations']['equal']=True
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_missing_repeat(self):
  x=report();x['raw_repeat_pairs'].pop()
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_no_runtime_claim(self):
  x=report();x['runtime_rerun']=True
  with self.assertRaises(ValueError):r.validate_report(x,2)
 def test_path_traversal(self):
  with self.assertRaises(ValueError):r.regular(Path.cwd(),'../x')
if __name__=='__main__':unittest.main()
