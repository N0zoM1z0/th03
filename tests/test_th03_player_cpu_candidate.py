"""Offline CPU candidate contracts. Synthetic OMF exists only inside these tests."""
from pathlib import Path
import sys,json,tomllib,unittest,tempfile,copy,hashlib,ast
from unittest.mock import patch
ROOT=Path.cwd();SHADOW=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'));import lib
lib.__path__.insert(0,str(SHADOW/'scripts/lib'))
from lib import th03_cpu_object as obj,th03_cpu_model as model,th03_cpu_gates as gates,th03_cpu_display as display,th03_player_cpu_candidate as cpu
from lib.omf import parse_omf
C=tomllib.loads((SHADOW/cpu.CANDIDATE_PATH).read_text());A=tomllib.loads((ROOT/'config/th03_main_exact_units.toml').read_text())
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
 def test_default_not_promoted(self):
  default=ROOT/'config/th03_main_exact_units.toml'
  self.assertEqual(hashlib.sha256(default.read_bytes()).hexdigest(),'b125066ad367a0b04e6f4be69bc62ee45fd20abd3eb47bf2dbb9518d208fed90')
  if SHADOW.resolve()!=ROOT.resolve():self.assertFalse((SHADOW/'config/th03_main_exact_units.toml').exists())
  self.assertNotIn('th03-main-player-cpu',{u['id'] for u in A['units']})
  self.assertNotIn('p_cpu',{u['object'] for u in A['units']})
  self.assertNotIn('p_cpu',{f['object'] for f in A['functions']})
  self.assertNotIn('p_cpre',json.dumps(C));self.assertEqual(len(A['functions']),399)
class Stage(unittest.TestCase):
 def setUp(self):
  from lib import th03_serial_schedule as schedule
  self.schedule=schedule;self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve();self.events=[];self.mutate=None
  self.scheduler=schedule.Schedule(self.execute,self.root,'cpu-offline',candidate=True)
  p=patch('subprocess.Popen',side_effect=AssertionError('native forbidden'));p.start();self.addCleanup(p.stop)
  p=patch.object(schedule.subprocess,'run',side_effect=self.build);p.start();self.addCleanup(p.stop)
 def stage(self,n=1):
  w=self.scheduler.output/('round'+str(n))/'source';w.mkdir(parents=True)
  for name in set(obj.contract()['source_pins'])|set(cpu.tail.SOURCE_PINS):
   p=w/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
  (w/'th03').mkdir(exist_ok=True);(w/'th03/p_cpu.cpp').write_text(obj.contract()['wrapper_bytes'])
  (w/'th03_main.asm').write_bytes((model.B/'th03_main.asm').read_bytes())
  (w/'build.bat').write_bytes((model.B/'build.bat').read_bytes().replace(self.schedule.BEFORE,self.schedule.AFTER))
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
   w=self.stage(n);r=cpu.precompile_and_stage(w,{},w.parent,self.scheduler);self.assertEqual(r['fresh_native_compilations'],1);self.scheduler(self.schedule.BUILD_ARGV,w,{},w.parent/'cold-build.log')
  self.assertEqual(self.events,['compile','init','options','build']*2)
 def test_stale_object_rejected(self):
  w=self.stage();(w/cpu.OBJECT).write_bytes(b'stale')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler)
  self.assertEqual(self.events,[])
 def test_non_cpu_object_mutation_rejected(self):
  w=self.stage();self.mutate=lambda w:(w/'obj/th03/unchanged.obj').write_bytes(b'changed')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler)
 def test_source_mutation_rejected(self):
  w=self.stage();self.mutate=lambda w:(w/'src/main/player/cpu.hpp').write_bytes(b'changed')
  with self.assertRaises(ValueError):cpu.precompile_and_stage(w,{},w.parent,self.scheduler)
if __name__=='__main__':unittest.main(verbosity=2)
