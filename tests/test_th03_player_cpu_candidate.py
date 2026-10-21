"""Offline CPU candidate contracts. Synthetic OMF exists only inside these tests."""
from th03_cpu_default_fixture import historical_default_text, historical_default_bytes
from pathlib import Path
import sys,json,tomllib,unittest,tempfile,copy,hashlib,ast
from unittest.mock import patch
ROOT=Path.cwd();SHADOW=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));import lib
lib.__path__.insert(0,str(SHADOW/'scripts/lib'))
from lib import th03_cpu_object as obj,th03_cpu_model as model,th03_cpu_gates as gates,th03_cpu_display as display,th03_player_cpu_candidate as cpu
from lib.omf import parse_omf
C=tomllib.loads((SHADOW/cpu.CANDIDATE_PATH).read_text());NEW_DEFAULT=tomllib.loads(historical_default_text());A=cpu.pre_cpu_config(NEW_DEFAULT)
WORK=ROOT/'.analysis/gpt-dots-player-cpu-only-retained-proposal-v14/run-first-v01/source'
def frame(kind,d):
 b=bytes([kind])+(len(d)+1).to_bytes(2,'little')+d;return b+bytes([-sum(b)%256])
def fixture(mutate=None):
 rows=[];added=False
 for r in parse_omf(model.CPU.read_bytes()):
  d=r.data
  if r.name=='COMENT' and d[:2]==b'\0\xe9' and len(d)>2:
   name=d[7:]
   if name==b'player_cpu.hpp':
    n=b'src/main/player/cpu.cpp';rows.append((r.record_type,d[:6]+bytes([len(n)])+n));n=b'src/main/player/cpu.hpp';d=d[:6]+bytes([len(n)])+n;added=True
  rows.append((r.record_type,d))
 assert added
 if mutate:mutate(rows)
 return b''.join(frame(k,d) for k,d in rows)
class CPU(unittest.TestCase):
 def test_binding(self):
  self.assertEqual(cpu.bind_candidate(A,C,cpu.CANDIDATE_PATH)[0],A);self.assertEqual(sum(f['size'] for f in C['functions']),1036);self.assertEqual(len(C['units'][0]['physical_objects']),1)
 def test_binding_drift(self):
  for key,val in [('object','p_cpre'),('source','bad.cpp')]:
   c=copy.deepcopy(C);c['units'][0][key]=val
   with self.assertRaises(ValueError):cpu.bind_candidate(A,c,cpu.CANDIDATE_PATH)
 def test_dependency_fixture(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'p_cpu.obj';p.write_bytes(fixture());self.assertTrue(obj.validate(p)['pass_cpu'])
 def check_bad(self,mutate):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'p_cpu.obj';p.write_bytes(fixture(mutate))
   with self.assertRaises(ValueError):obj.validate(p)
 def test_code_change(self):
  def change(rows):
   i=next(i for i,(k,d) in enumerate(rows) if k==0xa0);k,d=rows[i];rows[i]=(k,d[:-1]+bytes([d[-1]^1]))
  self.check_bad(change)
 def test_other_comment_change(self):
  def change(rows):
   i=next(i for i,(k,d) in enumerate(rows) if k==0x88 and d[:2]==b'\0\xf9');k,d=rows[i];rows[i]=(k,d[:-1]+bytes([d[-1]^1]))
  self.check_bad(change)
 def test_dependency_wrong_path(self):
  def change(rows):
   i=next(i for i,(k,d) in enumerate(rows) if b'src/main/player/cpu.hpp' in d);k,d=rows[i];rows[i]=(k,d.replace(b'cpu.hpp',b'bad.hpp'))
  self.check_bad(change)
 def test_dependency_order(self):
  def change(rows):
   i=[i for i,(k,d) in enumerate(rows) if k==0x88 and d[:2]==b'\0\xe9' and len(d)>2];rows[i[1]],rows[i[2]]=rows[i[2]],rows[i[1]]
  self.check_bad(change)
 def test_source_timestamp_bound(self):
  def change(rows):
   i=next(i for i,(k,d) in enumerate(rows) if k==0x88 and d[:2]==b'\0\xe8');k,d=rows[i];rows[i]=(k,d[:-1]+bytes([d[-1]^1]))
  self.check_bad(change)
 def test_root_prefix(self):
  raw=(model.B/'th03_main.asm').read_bytes();new=model.transform(raw);self.assertEqual(model.sha(new),cpu.ROOT_AFTER);self.assertIn(raw[raw.index(b'sub_C0D8\tproc near'):raw.index(b'sub_C370\tproc near')],new)
  with self.assertRaises(ValueError):model.transform(raw+b'\n')
 def test_actual_retained_root_and_raw(self):
  self.assertTrue(gates.root_gate(WORK/'obj/th03/main.obj')['pass_prelink_root']);self.assertTrue(gates.linked_bytes(WORK)['outside1551_equal'])
 def test_frozen_map_and_provider(self):
  result=cpu.freeze_expected(ROOT);self.assertEqual(len(result['stream']),1553);self.assertTrue(display.check_map((WORK/'obj/th03/main.map').read_bytes(),WORK)['pass_map_supplement'])
 def test_map_status_and_order(self):
  raw=(WORK/'obj/th03/main.map').read_bytes()
  for changed in [raw.replace(b'PLAYER_BOMB',b'PLAYER_BOMA',1),raw.replace(b' 096E:2C90 ',b' 096E:2C91 ',1),raw.replace(b'FONTFILE_CLOSE',b'DOS_CLOSE',1)]:
   with self.assertRaises(ValueError):display.check_map(changed,WORK)
 def test_pin_chain(self):
  for name in ('scripts/lib/th03_serial_schedule.py','scripts/replay_th03_main_serial.py'):
   ast.parse((SHADOW/name).read_text())
  spec={};tree=ast.parse((SHADOW/'scripts/replay_th03_main_serial.py').read_text())
  for n in tree.body:
   if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('SCHEDULE_SHA','ORIGINAL_REPLAY_SHA'):spec[n.targets[0].id]=ast.literal_eval(n.value)
  self.assertEqual(spec['SCHEDULE_SHA'],model.sha((SHADOW/'scripts/lib/th03_serial_schedule.py').read_bytes()));self.assertEqual(spec['ORIGINAL_REPLAY_SHA'],model.sha((SHADOW/'scripts/replay_th03_main_exact_units.py').read_bytes()))
 def test_real_replay_descriptor_and_tup_anchor(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('cpu_test_replay',SHADOW/'scripts/replay_th03_main_exact_units.py');replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
  combined=replay.add_candidate_owners(A,C);self.assertEqual(len(combined['functions']),403);self.assertEqual(len(combined['units']),77)
  replay.verify_include_carrier(C['units'][0],Path('/not-used-no-carrier'))
  tup=(ROOT/'_reference/ReC98/Tupfile.lua').read_text()
  for unit in combined['units']:
   if 'build_file' not in unit:continue
   self.assertEqual(unit['build_file'],'Tupfile.lua');self.assertEqual(tup.count(unit['build_anchor']),1);tup=tup.replace(unit['build_anchor'],unit['build_replacement'],1)
  self.assertIn('"obj/th03/p_cpu.obj",\n\t"obj/th03/warning.obj"',tup);self.assertNotIn('p_cpre',tup)
 def test_default_source_descriptor_no_acceptance(self):
  self.assertEqual(hashlib.sha256(historical_default_bytes()).hexdigest(),'001a6d04b0a7b35667b452d85e288935622597cf051c7c4646e66a5964cbf3c8')
  self.assertEqual(cpu.bind_default(NEW_DEFAULT)[0],NEW_DEFAULT)
  self.assertEqual((len(NEW_DEFAULT['units']),len(NEW_DEFAULT['functions'])),(77,403))
  self.assertEqual(cpu.pre_cpu_config(NEW_DEFAULT),A);self.assertEqual(len(A['functions']),399)
  self.assertEqual(cpu.tail.digest(A),cpu.tail.DEFAULT_CONFIG_DIGEST)
  self.assertNotIn('p_cpre',json.dumps(C))
class DefaultBinding(unittest.TestCase):
 def test_exact_inverse_and_accounting(self):
  import replay_th03_main_exact_units as replay
  before=copy.deepcopy(NEW_DEFAULT);bound,original=cpu.bind_default(NEW_DEFAULT)
  self.assertEqual(bound,before);self.assertEqual(NEW_DEFAULT,before);self.assertEqual(original,cpu.score.ORIGINAL_OWNER)
  extents=[e for u in bound['units'] for e in replay.normalized_code_extents(u,bound['segment'])]
  self.assertEqual((len(extents),len(bound['functions']),sum(e['size'] for e in extents)),(86,403,65198))
  self.assertEqual(sum(f['size'] for f in C['functions']),1036)
  self.assertEqual(sum(p['size'] for p in C['units'][0]['code_extents'][0]['producer_ranges']),41)
 def test_reject_default_drift(self):
  for mutate in [lambda c:c['units'].reverse(),lambda c:c['functions'].pop(),lambda c:c['units'].append(copy.deepcopy(c['units'][-1])),lambda c:c['units'][-1].update(object='p_cpre'),lambda c:c['functions'][-1].update(size=554),lambda c:c['units'][0].update(size=1)]:
   value=copy.deepcopy(NEW_DEFAULT);mutate(value)
   with self.assertRaises(ValueError):cpu.bind_default(value)
  with self.assertRaises(ValueError):cpu.bind_default(A)
 def test_candidate_default_mixing_rejected(self):
  with self.assertRaises(ValueError):cpu.bind_candidate(NEW_DEFAULT,C,cpu.CANDIDATE_PATH)
 def setup_only(self,candidate):
  import replay_th03_main_exact_units as replay
  tree=ast.parse((SHADOW/'scripts/replay_th03_main_exact_units.py').read_text());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='replay');prefix=[]
  for node in f.body:
   if isinstance(node,ast.If) and ast.unparse(node.test).startswith('not re.fullmatch'):break
   prefix.append(node)
  names=['config','score_original','score_proof','bomb_proof','tail_proof','cpu_proof','bomb_default','tail_default','cpu_default','charge_proof','charge_expected','charge_default']
  prefix.append(ast.Return(ast.Tuple(elts=[ast.Name(id=n,ctx=ast.Load()) for n in names],ctx=ast.Load())));f.body=prefix;env=dict(replay.__dict__);env['ROOT']=ROOT
  exec(compile(ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[])),'<CPU-setup-only>','exec'),env)
  return env['replay']('offline-no-native',[],candidate)
 def test_no_candidate_dispatch_all_proofs(self):
  from lib import th03_yumemi_charge_candidate as charge
  current_default=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
  self.assertEqual(charge.bind_default(current_default)[0],current_default)
  with patch('subprocess.Popen',side_effect=AssertionError('native forbidden')),patch.object(cpu.score,'guard_baseline',return_value={'score':1}),patch.object(cpu.bomb,'guard_baseline',return_value={'bomb':1}),patch.object(cpu.tail,'guard_baseline',return_value={'tail':1}),patch.object(cpu.tail,'freeze_expected',return_value={'tail_expected':1}),patch.object(cpu,'guard_baseline',return_value={'cpu':1}) as cg,patch.object(cpu,'freeze_expected',return_value={'cpu_expected':1}) as ce,patch.object(charge,'guard_baseline',return_value={'charge':1}) as chg,patch.object(charge,'freeze_expected',return_value={'charge_expected':1}) as che:
   row=self.setup_only(None)
  self.assertEqual(row[0],current_default);self.assertEqual(row[2:6],({'score':1},{'bomb':1},{'tail':1},{'cpu':1}));self.assertEqual(row[6:9],(True,True,True));self.assertEqual(row[9:],({'charge':1},{'charge_expected':1},True));cg.assert_called_once_with(ROOT);ce.assert_called_once_with(ROOT);chg.assert_called_once_with(ROOT);che.assert_called_once_with(ROOT)
 def test_mixed_dispatch_fails_before_proof(self):
  with patch.object(cpu,'guard_baseline') as guard:
   with self.assertRaises(ValueError):self.setup_only(ROOT/cpu.CANDIDATE_PATH)
  guard.assert_not_called()
 def test_mode_threaded_and_acceptance_not_claimed(self):
  s=(SHADOW/'scripts/replay_th03_main_exact_units.py').read_text()
  self.assertIn('cpu_candidate.precompile_and_stage(work, env, logs, execute, default=cpu_default)',s)
  self.assertIn('cpu_candidate.check_round(ROOT, work, target, cpu_proof, cpu_expected, default=cpu_default)',s)
  self.assertIn("report['cpu_default_staging'] = cpu_default",s);self.assertIn("report['cpu_candidate_exact_acceptance'] = False",s)

class Stage(unittest.TestCase):
 default_mode=False
 def setUp(self):
  from lib import th03_serial_schedule as schedule
  self.schedule=schedule;self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve();self.events=[];self.mutate=None
  self.scheduler=schedule.Schedule(self.execute,self.root,'cpu-offline',candidate=not self.default_mode)
  p=patch('subprocess.Popen',side_effect=AssertionError('native forbidden'));p.start();self.addCleanup(p.stop)
  p=patch.object(schedule.subprocess,'run',side_effect=self.build);p.start();self.addCleanup(p.stop)
 def stage(self,n=1):
  w=self.scheduler.output/('round'+str(n))/'source';w.mkdir(parents=True)
  for name in set(obj.contract()['source_pins'])|set(cpu.tail.SOURCE_PINS):
   p=w/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
  (w/'th03').mkdir(exist_ok=True);(w/'th03/p_cpu.cpp').write_text(obj.contract()['wrapper_bytes'])
  (w/'th03_main.asm').write_bytes((model.B/'th03_main.asm').read_bytes())
  (w/'build.bat').write_bytes((model.B/'build.bat').read_bytes() if self.default_mode else (model.B/'build.bat').read_bytes().replace(self.schedule.BEFORE,self.schedule.AFTER))
  for name in ('bin/tup.exe','Tupfile.ini'):
   p=w/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((model.B/name).read_bytes())
  (w/'obj/th03').mkdir(parents=True);(w/'obj/th03/unchanged.obj').write_bytes(b'offline inventory sentinel')
  return w
 def execute(self,argv,work,env,log):
  if 'tcc -c' in argv[-1]:
   self.assertIn('th03/p_cpu.cpp',argv[-1]);self.assertFalse((work/cpu.OBJECT).exists());(work/cpu.OBJECT).write_bytes(fixture());self.events.append('compile')
   if self.mutate:self.mutate(work)
  elif argv[-1]==r'bin\tup init':(work/'.tup').mkdir();(work/'.tup/db').write_bytes(b'offline');self.events.append('init')
  elif argv[-1]==r'bin\tup options':log.write_bytes(b"Parsed option file: .tup/options\nupdater.num_jobs = '1' from .tup/options\n");self.events.append('options')
  else:self.fail('unexpected fake command')
  return {'exit_code':0,'simulated_test_only':True}
 def build(self,argv,**kw):
  from types import SimpleNamespace
  self.assertEqual(argv,self.schedule.BUILD_ARGV);self.assertEqual(kw['timeout'],300);w=kw['cwd'];self.assertEqual((w/'.tup/options').read_bytes(),self.schedule.OPTIONS);self.assertEqual(model.sha((w/'th03_main.asm').read_bytes()),cpu.ROOT_AFTER);self.events.append('build');return SimpleNamespace(returncode=0,stdout=b'offline')
 def test_two_fresh_stages_real_schedule(self):
  for n in (1,2):
   w=self.stage(n);r=cpu.precompile_and_stage(w,{},w.parent,self.scheduler,default=self.default_mode);self.assertEqual(r['fresh_native_compilations'],1);self.scheduler(self.schedule.BUILD_ARGV,w,{},w.parent/'cold-build.log')
  self.assertEqual(self.events,['compile','init','options','build']*2)
 def test_stale_object_rejected(self):
  w=self.stage();(w/cpu.OBJECT).write_bytes(b'stale')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler,default=self.default_mode)
  self.assertEqual(self.events,[])
 def test_non_cpu_object_mutation_rejected(self):
  w=self.stage();self.mutate=lambda w:(w/'obj/th03/unchanged.obj').write_bytes(b'changed')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler,default=self.default_mode)
 def test_source_mutation_rejected(self):
  w=self.stage();self.mutate=lambda w:(w/'src/main/player/cpu.hpp').write_bytes(b'changed')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler,default=self.default_mode)
class DefaultStage(Stage):
 default_mode=True
 def test_candidate_carrier_not_default(self):
  w=self.stage();p=w/'build.bat';p.write_bytes(p.read_bytes().replace(self.schedule.BEFORE,self.schedule.AFTER))
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler,default=True)
  self.assertEqual(self.events,[])

if __name__=='__main__':unittest.main(verbosity=2)
