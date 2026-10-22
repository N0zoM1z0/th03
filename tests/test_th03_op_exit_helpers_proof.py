"""Portable proof/receipt and pre-import source-closure negative controls."""
from pathlib import Path
import copy,importlib.util,inspect,json,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('op_exit_proof',ROOT/'scripts/replay_th03_op_exit_helpers.py');replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
class ProofTests(unittest.TestCase):
 def setUp(self):
  self.p=json.loads((ROOT/'config/op_exit_helpers/proof.json').read_text())
 def test_real_compact_proof(self):replay.validate_proof(self.p)
 def test_every_credit_flag_rejected(self):
  for name in replay.FLAGS:
   p=copy.deepcopy(self.p);p[name]=True
   with self.subTest(name=name),self.assertRaisesRegex(ValueError,'credit inflation'):replay.validate_proof(p)
 def test_scope_inflation(self):
  for name in ('native_phases','fresh_owner_objects','new_owner_bytes','retained_context_objects','preserved_prior_owners','preserved_prior_bytes'):
   p=copy.deepcopy(self.p);p[name]+=1
   with self.subTest(name=name),self.assertRaisesRegex(ValueError,'bounded scope'):replay.validate_proof(p)
 def test_false_manifest(self):
  self.p['manifest_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'recipe identity'):replay.validate_proof(self.p)
 def test_false_verifier(self):
  self.p['verifier_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'recipe identity'):replay.validate_proof(self.p)
 def test_missing_current_source(self):
  self.p['maintained_closure'].pop('src/op/core/exit.cpp')
  with self.assertRaisesRegex(ValueError,'current source/helper closure'):replay.validate_proof(self.p)
 def test_missing_import_helper(self):
  self.p['helper_closure'].pop('scripts/inventory_rec98_th03.py')
  with self.assertRaisesRegex(ValueError,'current source/helper closure'):replay.validate_proof(self.p)
 def test_unrelated_historical_guard_forbidden(self):
  self.p['helper_closure']['docs/unrelated.md']={'sha256':'0'*64,'bytes':0}
  with self.assertRaisesRegex(ValueError,'current source/helper closure'):replay.validate_proof(self.p)
 def fixture(self,root):
  p={'helper_closure':{},'maintained_closure':{}};m={'sources':{}}
  for section,names in (('helper_closure',replay.HELPER_CLOSURE),('maintained_closure',replay.SOURCE_CLOSURE)):
   for name in names:
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True);body=('safe fixture '+name).encode();path.write_bytes(body);q={'sha256':replay.sha(body),'bytes':len(body)};p[section][name]=q
    if section=='helper_closure':m['sources'][name]=dict(q,mode=420)
  return p,m
 def test_complete_current_closure_guard(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p,m=self.fixture(root);replay.guard_current(root,p,root,m)
 def test_current_body_mutation_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p,m=self.fixture(root);(root/'src/op/core/exit.cpp').write_bytes(b'changed')
   with self.assertRaisesRegex(ValueError,'current maintained'):replay.guard_current(root,p,root,m)
 def test_stager_mutation_rejected_before_import(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p,m=self.fixture(root);(root/'scripts/stage_th03_op_exit_helpers.py').write_bytes(b'raise RuntimeError("must not execute")')
   with self.assertRaisesRegex(ValueError,'current maintained'):replay.guard_current(root,p,root,m)
 def test_import_helper_mutation_rejected_before_import(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p,m=self.fixture(root);(root/'scripts/lib/pc98.py').write_bytes(b'raise RuntimeError("must not execute")')
   with self.assertRaisesRegex(ValueError,'current helper before import'):replay.guard_current(root,p,root,m)
 def test_false_native_helper_binding_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p,m=self.fixture(root);m['sources']['scripts/lib/omf.py']['sha256']='0'*64
   with self.assertRaisesRegex(ValueError,'current helper before import'):replay.guard_current(root,p,root,m)
 def test_guards_precede_all_dynamic_imports(self):
  s=inspect.getsource(replay.replay);self.assertLess(s.index('guard_current(root,p,source_root,m)'),s.index("stage=load("));self.assertLess(s.index('guard_current(root,p,source_root,m)'),s.index("policy=load("));self.assertLess(s.index('guard_current(root,p,source_root,m)'),s.index("verifier=load("))
 def phase(self):
  env={'environment':{'DISPLAY':'','WAYLAND_DISPLAY':'','TZ':'UTC'},'cpu':[0],'nice':10};m={'work':'work','native_argv':{'compile_exit':['tcc','th03/exit.cpp']}};a={'argv':m['native_argv']['compile_exit'],'cwd':'/repo/work','environment':env['environment'],'wait_seconds':90,'cleanup_seconds':15};z={'exit_code':0,'timeout':False,'cleanup_uncertain':False,'poison':False,'initial_inventory_complete':True,'inventory_complete':True,'survivors':[],'errors':[]};return a,z,m,env
 def test_positive_bounded_phase(self):replay.validate_phase('compile_exit',*self.phase())
 def test_wrong_native_command(self):
  a,z,m,e=self.phase();a['argv']=['tasm']
  with self.assertRaisesRegex(ValueError,'argv'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_wrong_native_workdir(self):
  a,z,m,e=self.phase();a['cwd']='/other'
  with self.assertRaisesRegex(ValueError,'cwd'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_wrong_native_budget(self):
  for k in ('wait_seconds','cleanup_seconds'):
   a,z,m,e=self.phase();a[k]+=1
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'phase bounds'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_cpu_and_nice_rejected(self):
  for k,v in (('cpu',[0,1]),('nice',0)):
   a,z,m,e=self.phase();e[k]=v
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'resource bounds'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_uncertain_cleanup_rejected(self):
  for k in ('timeout','cleanup_uncertain','poison'):
   a,z,m,e=self.phase();z[k]=True
   with self.subTest(k=k),self.assertRaisesRegex(ValueError,'unsafe cleanup'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_survivors_rejected(self):
  a,z,m,e=self.phase();z['survivors']=[123]
  with self.assertRaisesRegex(ValueError,'owned cleanup inventory'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_incomplete_inventory_rejected(self):
  a,z,m,e=self.phase();z['inventory_complete']=False
  with self.assertRaisesRegex(ValueError,'owned cleanup inventory'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_nonzero_exit_rejected(self):
  a,z,m,e=self.phase();z['exit_code']=1
  with self.assertRaisesRegex(ValueError,'phase exit'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_boolean_exit_rejected(self):
  a,z,m,e=self.phase();z['exit_code']=False
  with self.assertRaisesRegex(ValueError,'phase exit'):replay.validate_phase('compile_exit',a,z,m,e)
 def test_traversal_rejected(self):
  with self.assertRaisesRegex(ValueError,'unsafe'):replay.regular(ROOT,'../outside')
 def test_symlink_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'body').write_bytes(b'body');(root/'link').symlink_to(root/'body')
   with self.assertRaisesRegex(ValueError,'regular input'):replay.regular(root,'link')
if __name__=='__main__':unittest.main()
