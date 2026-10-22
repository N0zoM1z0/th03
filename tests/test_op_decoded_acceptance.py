"""Portable negative controls; no target/model/native execution."""
import copy,importlib.util,json,pathlib,unittest,tempfile,tomllib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('op_acceptance_controls',ROOT/'scripts/lib/op_decoded_acceptance.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Controls(unittest.TestCase):
 def setUp(self):
  self.c=json.loads((ROOT/'config/op_decoded_acceptance/cohort.json').read_text())['owners']
  r=dict(raw_equal=True,ordered_relocations_equal=True,map_covered_bytes=1,source_lineage_verified=True,target_sha256='a'*64,candidate_sha256='a'*64)
  self.o=[dict(d,coordinate_space='decoded-load',canonical_file_offset=None,rounds=[dict(r,map_covered_bytes=d['size']),dict(r,map_covered_bytes=d['size'])]) for d in self.c]
 def reject(self,fn):
  fn()
  with self.assertRaises(m.Invalid):m.validate_inventory(self.o,self.c)
 def test_positive(self):m.validate_inventory(self.o,self.c)
 def test_duplicate_owner(self):self.reject(lambda:self.o.__setitem__(1,copy.deepcopy(self.o[0])))
 def test_missing_owner(self):self.reject(lambda:self.o.pop())
 def test_selection(self):self.reject(lambda:self.o[0].update(unit_id='th03-op-decoded-character-selection'))
 def test_physical_offset(self):self.reject(lambda:self.o[0].update(canonical_file_offset=7))
 def test_coordinate(self):self.reject(lambda:self.o[0].update(coordinate_space='canonical-file'))
 def test_wrong_source(self):self.reject(lambda:self.o[0].update(source='src/op/fake.cpp'))
 def test_extent(self):self.reject(lambda:self.o[0].update(size=self.o[0]['size']-1))
 def test_raw_failure(self):self.reject(lambda:self.o[0]['rounds'][1].update(raw_equal=False))
 def test_order_failure(self):self.reject(lambda:self.o[0]['rounds'][1].update(ordered_relocations_equal=False))
 def test_partial_map(self):self.reject(lambda:self.o[0]['rounds'][1].update(map_covered_bytes=0))
 def test_lineage(self):self.reject(lambda:self.o[0]['rounds'][1].update(source_lineage_verified=False))
 def test_digest_mismatch(self):self.reject(lambda:self.o[0]['rounds'][1].update(candidate_sha256='b'*64))
 def test_one_round(self):self.reject(lambda:self.o[0]['rounds'].pop())
 def test_pending_state(self):
  with self.assertRaises(m.Invalid):m.verify(ROOT,dict(schema='op-decoded-acceptance-v1',state='review-ready'))
 def test_no_runtime_gate(self):self.assertEqual(len(m.GATES),11);self.assertNotIn('runtime-trace',m.GATES)
 def test_historical_replay_only_in_prepare(self):
  library=(ROOT/'scripts/lib/op_decoded_acceptance.py').read_text();cli=(ROOT/'scripts/replay_th03_op_decoded_acceptance.py').read_text();self.assertNotIn('fullcold.replay(',library);self.assertEqual(cli.count('cold.replay('),1)
 def test_missing_publication_zero(self):self.assertEqual(m.load_status(ROOT)['decoded_exact_units'],0)
 def test_reject_traversal(self):
  with self.assertRaises(m.Invalid):m.regular(ROOT,'../secret')
class GateControls(unittest.TestCase):
 def setUp(self):
  self.policy=tomllib.loads((ROOT.parents[1]/'config/oracles.toml').read_text()) if (ROOT.parents[1]/'config/oracles.toml').exists() else tomllib.loads((ROOT/'config/oracles.toml').read_text())
  specs={x['id']:x for x in self.policy['oracles']}
  self.g={g:dict(result='pass',witness='proof',evidence_class=specs[g]['accepts_evidence_classes'][0]) for g in m.GATES};self.e={'proof':{}}
 def test_all_eleven(self):m.validate_gates(self.g,self.policy,self.e)
 def test_missing_gate(self):
  self.g.pop('raw-bytes')
  with self.assertRaises(m.Invalid):m.validate_gates(self.g,self.policy,self.e)
 def test_wrong_evidence_class(self):
  self.g['raw-bytes']['evidence_class']='inference'
  with self.assertRaises(m.Invalid):m.validate_gates(self.g,self.policy,self.e)
 def test_failed_gate(self):
  self.g['raw-bytes']['result']='fail'
  with self.assertRaises(m.Invalid):m.validate_gates(self.g,self.policy,self.e)
 def test_unknown_witness(self):
  with self.assertRaises(m.Invalid):m.validate_gates(self.g,self.policy,{})
 def test_runtime_not_substitute(self):
  self.g['runtime-trace']=self.g.pop('raw-bytes')
  with self.assertRaises(m.Invalid):m.validate_gates(self.g,self.policy,self.e)
 def test_pinned_input_drift(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
   p=pathlib.Path(tmp)/'source';p.write_bytes(b'first');q=m.pin(tmp,'source');p.write_bytes(b'other')
   with self.assertRaises(m.Invalid):m.checked(tmp,q)
 def test_pinned_input_missing(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
   p=pathlib.Path(tmp)/'source';p.write_bytes(b'first');q=m.pin(tmp,'source');p.unlink()
   with self.assertRaises(m.Invalid):m.checked(tmp,q)


class MetadataControls(GateControls):
 def setUp(self):
  super().setUp();repo=ROOT if (ROOT/'scripts/validate_tracking.py').exists() else ROOT.parents[1]
  spec=importlib.util.spec_from_file_location('tracking_eligibility',repo/'scripts/validate_tracking.py');self.tracking=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.tracking)
  self.o=dict(unit_id='reviewed-owner',start=32,size=8,rounds=[dict(target_sha256='a'*64,candidate_sha256='a'*64)])
  self.rows=m.owner_oracles([self.o],self.g,[dict(path='proof',sha256='b'*64,bytes=1)],self.policy,[],'python3 scripts/replay_th03_op_decoded_acceptance.py --prepare .analysis/test')['reviewed-owner']
 def accepted(self):
  p=self.policy['policy'];return self.tracking.accepted_oracle_passes(list(self.rows),self.rows,{x['id']:x for x in self.policy['oracles']},set(p['non_acceptance_evidence_classes']),artifact='th03-op',unit_id=self.o['unit_id'],extent_start=32,extent_size=8,global_evidence_oracles=set(p['global_evidence_oracles']),artifact_evidence_oracles=set(p['artifact_evidence_oracles']))
 def test_generated_metadata_eligible(self):self.assertEqual(self.accepted(),set(m.GATES));self.assertTrue(all(r['observed_utc'].endswith('Z') for r in self.rows.values()))
 def test_offset_timestamp_ineligible(self):
  for r in self.rows.values():r['observed_utc']=r['observed_utc'][:-1]+'+00:00'
  self.assertEqual(self.accepted(),set())
 def test_owner_scope_ineligible(self):
  for r in self.rows.values():
   if r['oracle']=='raw-bytes':r['unit_id']='wrong-owner'
  self.assertNotIn('raw-bytes',self.accepted())
 def test_raw_digest_ineligible(self):
  for r in self.rows.values():
   if r['oracle']=='raw-bytes':r['output_sha256']='c'*64
  self.assertNotIn('raw-bytes',self.accepted())
 def test_wrong_replay_input_binding(self):
  key,row=next((k,r) for k,r in self.rows.items() if r['oracle']!='raw-bytes');row['input_sha256']='c'*64
  with self.assertRaises(m.Invalid):m.validate_row_binding(self.o,key,row,self.g,{'proof':dict(sha256='b'*64)},m.sha(b'[]'))
 def test_wrong_claim_identity(self):
  key,row=next(iter(self.rows.items()));row['claim_id']='wrong-owner'
  with self.assertRaises(m.Invalid):m.validate_row_binding(self.o,key,row,self.g,{'proof':dict(sha256='b'*64)},m.sha(b'[]'))
 def test_wrong_row_identity(self):
  key,row=next(iter(self.rows.items()));row['id']='wrong-row'
  with self.assertRaises(m.Invalid):m.validate_row_binding(self.o,key,row,self.g,{'proof':dict(sha256='b'*64)},m.sha(b'[]'))
class ComparatorControls(unittest.TestCase):
 def setUp(self):
  from types import SimpleNamespace as N
  self.N=N;self.tmp=tempfile.TemporaryDirectory(dir=ROOT);self.root=pathlib.Path(self.tmp.name);self.work=self.root/'work';self.work.mkdir();(self.root/'src').mkdir();(self.work/'src').mkdir()
  for base in (self.root,self.work):(base/'src/x.cpp').write_bytes(b'authored')
  (self.work/'physical.cpp').write_bytes(b'wrapper');(self.work/'X.OBJ').write_bytes(b'object')
  self.d=dict(unit_id='synthetic',source='src/x.cpp',start=2,size=6)
  self.t=N(program_image=b'0123456789',relocations=[N(linear=2,segment=0,offset=2),N(linear=4,segment=0,offset=4)]);self.c=copy.deepcopy(self.t)
  self.maps=[dict(module='physical.cpp',segment=0,offset=2,size=6)];self.graph=dict(project_producers=[dict(source='physical.cpp',object='X.OBJ',maintained_owner_sources=['src/x.cpp'])]);self.manifest=dict(repeat_inputs={n:dict(sha256=m.sha((self.work/n).read_bytes())) for n in ['physical.cpp','src/x.cpp']});self.obj=dict(valid=True,dependency_paths=['physical.cpp','src/x.cpp'])
 def tearDown(self):self.tmp.cleanup()
 def audit(self):return m.audit_owner(self.d,self.t,self.c,self.maps,self.graph,self.work,self.manifest,root=self.root,object_parser=lambda raw:self.obj)
 def test_synthetic_positive(self):self.assertTrue(self.audit()['raw_equal'])
 def test_relocation_json_roundtrip(self):
  observed=self.audit();self.assertTrue(observed['relocations']);self.assertEqual(observed,json.loads(json.dumps(observed)))
 def test_byte_mutation(self):
  self.c.program_image=b'01X3456789'
  with self.assertRaises(m.Invalid):self.audit()
 def test_ordered_relocations(self):
  self.c.relocations.reverse()
  with self.assertRaises(m.Invalid):self.audit()
 def test_left_straddle(self):
  self.c.relocations.append(self.N(linear=1,segment=0,offset=1))
  with self.assertRaises(m.Invalid):self.audit()
 def test_right_straddle(self):
  self.c.relocations.append(self.N(linear=7,segment=0,offset=7))
  with self.assertRaises(m.Invalid):self.audit()
 def test_duplicate_map(self):
  self.maps*=2
  with self.assertRaises(m.Invalid):self.audit()
 def test_partial_map(self):
  self.maps[0]['size']=5
  with self.assertRaises(m.Invalid):self.audit()
 def test_missing_authored_dependency(self):
  self.obj['dependency_paths'].remove('src/x.cpp')
  with self.assertRaises(m.Invalid):self.audit()
 def test_missing_wrapper_dependency(self):
  self.obj['dependency_paths'].remove('physical.cpp')
  with self.assertRaises(m.Invalid):self.audit()
 def test_consumed_source_drift(self):
  (self.work/'src/x.cpp').write_bytes(b'drift')
  with self.assertRaises(m.Invalid):self.audit()
 def test_current_source_drift(self):
  (self.root/'src/x.cpp').write_bytes(b'drift')
  with self.assertRaises(m.Invalid):self.audit()
 def test_outside_scope_no_false_credit(self):
  self.c.program_image=b'X123456789';self.assertTrue(self.audit()['raw_equal'])


class BootstrapControls(unittest.TestCase):
 def _check_changed(self,target,rehash=False):
  import subprocess,sys,hashlib
  with tempfile.TemporaryDirectory(dir=ROOT) as d:
   root=pathlib.Path(d);(root/'scripts').mkdir();(root/'scripts/lib').mkdir();(root/'config/op_decoded_acceptance').mkdir(parents=True)
   cli='scripts/replay_th03_op_decoded_acceptance.py';(root/cli).write_bytes((ROOT/cli).read_bytes())
   names=['scripts/validate_tracking.py',cli,'scripts/lib/op_decoded_acceptance.py','scripts/lib/__init__.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/op_diet_lineage.py','scripts/lib/toolchain.py','scripts/review_th03_decoded_code.py','scripts/replay_th03_op_fullcold.py'];pins=[]
   for n in names:
    p=root/n
    if n!=cli:p.write_text('pass\n')
    raw=p.read_bytes();pins.append(dict(path=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
   (root/'config/op_decoded_acceptance/helper-bindings.json').write_text(json.dumps(dict(pins=pins)))
   args=['--prepare','.analysis/no-run']
   if rehash:
    manifest_name='config/op_decoded_acceptance/helper-bindings.json';reviewed=dict(state='review-ready',input_bindings=pins+[m.pin(root,manifest_name)]);raw_review=json.dumps(reviewed).encode();(root/'.analysis').mkdir();(root/'.analysis/review.json').write_bytes(raw_review);args=['--publish','.analysis/review.json','--review-sha256',m.sha(raw_review),'--output','config/op_decoded_acceptance/publication.json']
   marker=root/'untrusted-executed';(root/target).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("bad")\n')
   if rehash:
    pins=[m.pin(root,n) for n in names];(root/'config/op_decoded_acceptance/helper-bindings.json').write_text(json.dumps(dict(pins=pins)))
   result=subprocess.run([sys.executable,'-B',str(root/cli),*args],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0);self.assertIn('reviewed helper closure drift' if rehash else 'helper drift',result.stderr);self.assertFalse(marker.exists());self.assertFalse((root/'config/op_decoded_acceptance/publication.json').exists());self.assertFalse(list(root.rglob('__pycache__')))
 def test_changed_helper_cannot_execute(self):self._check_changed('scripts/lib/op_decoded_acceptance.py')
 def test_changed_package_initializer_cannot_execute(self):self._check_changed('scripts/lib/__init__.py')
 def test_rehashed_helper_manifest_cannot_escape_review(self):self._check_changed('scripts/lib/op_decoded_acceptance.py',rehash=True)
class PathControls(unittest.TestCase):
 def test_rejected_paths_never_prepare(self):
  import ast,argparse,sys
  from unittest.mock import patch
  tree=ast.parse((ROOT/'scripts/replay_th03_op_decoded_acceptance.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  called=[];env=dict(argparse=argparse,Path=pathlib.Path,need=m.need,ROOT=ROOT,prepare=lambda p:called.append(p))
  exec(compile(ast.Module(body=[fn],type_ignores=[]),'production main','exec'),env)
  for path in ('/tmp/out','../out','config/out'):
   with patch.object(sys,'argv',['driver','--prepare',path]):
    with self.assertRaises(m.Invalid):env['main']()
  self.assertEqual(called,[])


class DescriptorControls(unittest.TestCase):
 def test_only_complete_source_present(self):
  u=dict(id='owner',artifact='th03-op',segment='decoded:0002',offset='0',file_offset='',boundary_state='reviewed',origin='authored',source='src/x.cpp',state='source-present',size='8',compare_size='8')
  self.assertEqual(m.descriptor(u)['size'],8)
  for state in ('blocked','excluded','candidate'):
   with self.assertRaises(m.Invalid):m.descriptor(dict(u,state=state))
  with self.assertRaises(m.Invalid):m.descriptor(dict(u,compare_size='7'))
class ClosureControls(unittest.TestCase):
 def test_actual_closure_omission_and_drift(self):
  with tempfile.TemporaryDirectory(dir=ROOT) as d:
   root=pathlib.Path(d)
   def write(n,raw):
    p=root/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
   for n in ('src/current.cpp','retained.bin','archive.tar','config/th03_main_authored_functions.csv','config/evidence.csv','config/hypotheses.csv','config/knowledge.csv','config/toolchain.toml'):write(n,b'original')
   stage='scripts/stage_th03_op_fullcold.py';write(stage,('INPUT_HASHES='+repr({'src/current.cpp':m.sha(b'original')})+'\nARCHIVE="archive.tar"\nARCHIVE_SHA='+repr(m.sha(b'original'))+'\n').encode())
   write('inventory.json',json.dumps(dict(pins=[m.pin(root,'retained.bin')])).encode());write('config/op_fullcold/proof.json',json.dumps(dict(inventory=m.pin(root,'inventory.json'),stage_sha256=m.sha((root/stage).read_bytes()))).encode())
   required=m.required_closure(root);self.assertIn('src/current.cpp',required);self.assertIn('retained.bin',required);self.assertIn('config/th03_main_authored_functions.csv',required)
   provided=dict(required);provided.pop('src/current.cpp');
   with self.assertRaises(m.Invalid):m.require_bindings(provided,required)
   write('src/current.cpp',b'drift')
   with self.assertRaises(m.Invalid):m.required_closure(root)
if __name__=='__main__':unittest.main()
