"""Resident source proof negatives; offline only, no compiler/Wine/model invocation."""
import copy,importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path.cwd().resolve()
SOURCE=Path(os.environ.get('TH03_RESIDENT_SOURCE_ROOT',str(ROOT))).resolve()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
r=module('resident_replay_tests',SOURCE/'scripts/replay_th03_zun_resident.py')
s=module('resident_stage_tests',SOURCE/'scripts/stage_th03_zun_resident.py')
PROOF=json.loads((SOURCE/'config/zun_resident/proof.json').read_text())
RUNTIME=json.loads((ROOT/'.analysis/zun-resident-native-proposal-v02/runtime.json').read_text())
class ResidentProofTests(unittest.TestCase):
 def test_valid_compact_scope(self):r.validate_proof(PROOF)
 def test_no_credit_inflation(self):
  for key in r.CREDIT_FLAGS:
   q=copy.deepcopy(PROOF);q[key]=True
   with self.subTest(key=key),self.assertRaises(ValueError):r.validate_proof(q)
 def test_bounded_counts(self):
  for key,value in [('native_phases',2),('root_procedures',3),('root_code_bytes',629),('root_data_bytes',0),('runtime_calls',60),('runtime_images',3),('two_cold_builds',False)]:
   q=copy.deepcopy(PROOF);q[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):r.validate_proof(q)
 def test_recipe_drift(self):
  q=copy.deepcopy(PROOF);q['manifest_sha256s'][1]='0'*64
  with self.assertRaises(ValueError):r.validate_proof(q)
 def test_duplicate_pin(self):
  q=copy.deepcopy(PROOF);q['pins']*=2
  with self.assertRaises(ValueError):r.validate_proof(q)
 def test_helper_closure_missing(self):
  q=copy.deepcopy(PROOF);q['helper_closure'].pop('scripts/lib/pc98.py')
  with self.assertRaises(ValueError):r.validate_proof(q)
 def test_runtime_scope(self):r.validate_runtime(RUNTIME)
 def test_runtime_bad_abi(self):
  q=copy.deepcopy(RUNTIME);q['runtime']['current'][0]['preserved']['BP']=0xbeef;q['runtime']['target'][0]['preserved']['BP']=0xbeef
  with self.assertRaises(ValueError):r.validate_runtime(q)
 def test_runtime_no_extra_second_run(self):
  q=copy.deepcopy(RUNTIME);q['runtime_total_calls']=60
  with self.assertRaises(ValueError):r.validate_runtime(q)
 def test_runtime_semantic_drift(self):
  q=copy.deepcopy(RUNTIME);q['runtime']['current'][0]['debug']=1
  with self.assertRaises(ValueError):r.validate_runtime(q)
 def test_import_helper_rejected_before_loading(self):
  original=Path.read_bytes
  def read(p):
   b=original(p);return b+b'\n# drift\n' if p==ROOT/'scripts/lib/omf.py' else b
  with patch.object(Path,'read_bytes',read),patch('builtins.exec') as loaded,self.assertRaisesRegex(ValueError,'input drift'):
   r.replay(ROOT,PROOF,SOURCE)
  loaded.assert_not_called()
 def test_replay_ignores_unrelated_tracked_docs_and_never_runs_native_or_model(self):
  original=Path.read_bytes
  def read(p):
   if p.is_relative_to(ROOT/'docs') or p in [ROOT/'config/units.csv',ROOT/'config/evidence.csv']:raise AssertionError('unrelated tracked snapshot access')
   return original(p)
  with patch.dict(sys.modules),patch.object(Path,'read_bytes',read),patch('subprocess.Popen',side_effect=AssertionError('native forbidden')),patch('unicorn.Uc',side_effect=AssertionError('model forbidden')):
   result=r.replay(ROOT,PROOF,SOURCE)
  self.assertEqual((result['root_code_bytes'],result['retained_runtime_calls'],result['native_phases_replayed']),(322,40,4));self.assertFalse(result['exact_acceptance'])
class ResidentStageTests(unittest.TestCase):
 def test_source_encoding_and_provenance(self):
  plan,data=s.read_inputs(SOURCE,SOURCE/'config/zun_resident/source.json');self.assertEqual(len(data),10)
  for b in data.values():b.decode('cp932');self.assertNotIn(b'\r',b)
  self.assertIn(b'int main(int argc, const unsigned char **argv)',data['src/zun/res_init.inl'])
 def test_fresh_stage_only_sources(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.analysis') as t:
   out=Path(t)/'overlay';report=s.stage(SOURCE,SOURCE/'config/zun_resident/source.json',out)
   self.assertEqual(len(report['files']),11);self.assertFalse(report['compiled']);self.assertEqual((out/'th03/res_yume.cpp').read_bytes(),b'#include "src/zun/res_yume.cpp"\n')
   self.assertFalse(any(p.suffix.lower() in ['.obj','.lib','.com','.exe'] for p in out.rglob('*') if p.is_file()))
   with self.assertRaises(ValueError):s.stage(SOURCE,SOURCE/'config/zun_resident/source.json',out)
 def test_reject_modified_owner(self):
  original=Path.read_bytes
  def read(p):return original(p)+(b'\n' if p==SOURCE/'src/zun/res_init.inl' else b'')
  with patch.object(Path,'read_bytes',read),self.assertRaises(ValueError):s.read_inputs(SOURCE,SOURCE/'config/zun_resident/source.json')
 def test_reject_modified_manifest(self):
  with tempfile.TemporaryDirectory(dir=ROOT/'.analysis') as t:
   p=Path(t)/'manifest.json';p.write_bytes((SOURCE/'config/zun_resident/source.json').read_bytes()+b'\n')
   with self.assertRaises(ValueError):s.read_inputs(SOURCE,p)
if __name__=='__main__':unittest.main()
