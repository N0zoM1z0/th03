"""Source-only proof and retained-record mutations; no native tools or models."""
import ast,copy,hashlib,importlib.util,json,unittest,tempfile
from unittest.mock import patch
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=Path.cwd()
spec=importlib.util.spec_from_file_location('zunsoft_repeat_tests',BASE/'scripts/replay_th03_zunsoft_repeat.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ZunsoftRepeatProofTests(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((BASE/'config/zunsoft_repeat/proof.json').read_text());self.inv=json.loads((ROOT/self.p['inventory']['path']).read_text());self.pair=json.loads((ROOT/m.OUTPUT/'raw-repeat-verification.json').read_text())
 def test_schema_inventory_and_retained_pair(self):m.validate_proof(self.p);m.validate_inventory(self.inv,self.p);m.validate_pair(self.pair)
 def test_credit_flags(self):
  for k in m.FLAGS:
   q=copy.deepcopy(self.p);q[k]=True
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_proof(q)
 def test_counts_do_not_invent_third_modeled_image(self):
  for k in ['root_procedures','root_code_bytes','root_data_bytes','root_bss_bytes','native_phases','runtime_images','retained_runtime_calls','modeled_candidates']:
   q=copy.deepcopy(self.p);q[k]+=1
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_proof(q)
 def test_two_frozen_builds(self):
  for k,v in [('two_cold_builds',False),('manifest_sha256s',list(reversed(m.MANIFESTS)))]:
   q=copy.deepcopy(self.p);q[k]=v
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_proof(q)
 def test_fixed_history(self):
  for k in ['original_proof_sha256','repeat_verifier_sha256','raw_repeat_sha256','structural_sha256']:
   q=copy.deepcopy(self.p);q[k]='0'*64
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_proof(q)
 def test_source_helper_closure(self):
  for k in ['helper_closure','maintained_sources']:
   q=copy.deepcopy(self.p);q[k].pop(next(iter(q[k])))
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_proof(q)
 def test_retention_dictionary(self):
  q=copy.deepcopy(self.inv);q['inputs'].pop(next(iter(q['inputs'])))
  with self.assertRaises(ValueError):m.validate_inventory(q,self.p)
 def test_inventory_metadata_and_duplicates(self):
  q=copy.deepcopy(self.inv);q['metadata']['root_code_bytes']=10096
  with self.assertRaises(ValueError):m.validate_inventory(q,self.p)
  q=copy.deepcopy(self.inv);q['pins'].append(q['pins'][0])
  with self.assertRaises(ValueError):m.validate_inventory(q,self.p)
 def test_raw_output_mutations(self):
  for k,v in [('raw_equal',False),('bytes',10097),('sha256','0'*64)]:
   q=copy.deepcopy(self.pair);q['raw_products']['bin/th01/zunsoft.com'][k]=v
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_pair(q)
 def test_pair_runtime_and_reuse_mutations(self):
  for k,v in [('retained_runtime_calls',3900),('runtime_rerun',True),('project_objects_reused',1),('independent_cold_builds',1),('source_bytes_modes_mtimes_identical',False)]:
   q=copy.deepcopy(self.pair);q[k]=v
   with self.subTest(key=k),self.assertRaises(ValueError):m.validate_pair(q)
 def test_original_one_build_proof_unchanged(self):
  b=(ROOT/m.ORIGINAL_PROOF).read_bytes();p=json.loads(b);self.assertEqual(hashlib.sha256(b).hexdigest(),self.p['original_proof_sha256']);self.assertFalse(p['two_cold_builds']);self.assertEqual((p['native_phases'],p['runtime_calls']),(2,2600))
 def test_source_only_entrypoint(self):
  t=ast.parse((BASE/'scripts/replay_th03_zunsoft_repeat.py').read_text());self.assertFalse(any(isinstance(n,ast.Import) and any(a.name=='subprocess' for a in n.names) for n in ast.walk(t)))
 def test_inventory_cleanup_retention(self):
  spec=importlib.util.spec_from_file_location('zunsoft_repeat_cleanup_test',ROOT/'scripts/clean_generated.py');clean=importlib.util.module_from_spec(spec);spec.loader.exec_module(clean)
  with tempfile.TemporaryDirectory(prefix='zunsoft-retention-test-',dir=ROOT/'.analysis') as d:
   root=Path(d);analysis=root/'.analysis';analysis.mkdir();inventory=analysis/'inventory.json';inventory.write_text(json.dumps(self.inv))
   with patch.multiple(clean,ROOT=root,ANALYSIS=analysis,PRESERVED_ANALYSIS_ROOTS=set(),PRESERVED_ANALYSIS_FILES=set()),patch.object(clean,'ledger_preserved_paths',return_value=set()),patch.object(clean,'documented_analysis_paths',return_value=set()),patch.object(clean,'ledger_text_query_paths',return_value=set()),patch.object(clean,'proof_preserved_paths',return_value=(set(),set())):
    retained=clean.referenced_analysis_closure({inventory})
   expected={root/name for name in self.inv['inputs'] if name.startswith('.analysis/')}
   self.assertTrue(expected.issubset(retained));self.assertGreater(len(expected),250)
if __name__=='__main__':unittest.main()
