"""Offline real-stage/real-Schedule contracts. Processes simulated, never native."""
from pathlib import Path
import copy,importlib.util,json,os,subprocess,sys,tempfile,tomllib,unittest
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
PRIVATE=Path(os.environ.get('TH03_TAIL_PRIVATE_ROOT',Path.cwd())).resolve()
sys.path.insert(0,str(PRIVATE/'scripts'));sys.path.insert(0,str(ROOT/'scripts'));import lib
lib.__path__.insert(0,str(ROOT/'scripts/lib'))
from lib import th03_player_tail_candidate as tail,th03_yumemi_bomb_candidate as bomb,th03_score_candidate as score,th03_serial_schedule as schedule
spec=importlib.util.spec_from_file_location('tail_test_replay',ROOT/'scripts/replay_th03_main_exact_units.py');replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
BASE=PRIVATE/tail.BASELINE/'round1/source';RETAINED=PRIVATE/'.analysis/gpt-dots-player-tail-retained-probe-v06/run-first-v01/source'
DEFAULT=tomllib.loads((PRIVATE/'config/th03_main_exact_units.toml').read_text());CANDIDATE=tomllib.loads((ROOT/tail.CANDIDATE_PATH).read_text())
HAS_PRIVATE=(BASE/'obj/th03/main.obj').is_file() and (RETAINED/'obj/th03/main.obj').is_file()
class Binding(unittest.TestCase):
 def test_transitive_runtime_closure(self):
  text=(ROOT/'scripts/replay_th03_main_exact_units.py').read_text()
  for name in ('scripts/review_th03_cpu_link_order.py','scripts/lib/th03_tail_public_display.json'):
   self.assertIn('inputs["'+name+'"]',text);self.assertIn(name,schedule.PINS);self.assertNotIn(name,schedule.CANDIDATE_PINS)
 def test_supervisor_exact_pins(self):
  import ast,hashlib
  parsed=ast.parse((ROOT/'scripts/replay_th03_main_serial.py').read_text());values={n.targets[0].id:ast.literal_eval(n.value) for n in parsed.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('SCHEDULE_SHA','ORIGINAL_REPLAY_SHA')}
  self.assertEqual(values['SCHEDULE_SHA'],hashlib.sha256((ROOT/'scripts/lib/th03_serial_schedule.py').read_bytes()).hexdigest())
  self.assertEqual(values['ORIGINAL_REPLAY_SHA'],hashlib.sha256((ROOT/'scripts/replay_th03_main_exact_units.py').read_bytes()).hexdigest())
 def test_exact_descriptor_totals_support(self):
  tail.bind_candidate(DEFAULT,CANDIDATE,tail.CANDIDATE_PATH);self.assertEqual((len(CANDIDATE['units']),len(CANDIDATE['functions']),sum(f['size'] for f in CANDIDATE['functions'])),(4,21,3433))
  paths={p for u in CANDIDATE['units'] for p in replay.unit_source_paths(u)};self.assertTrue(paths<=set(tail.SOURCE_PINS));self.assertEqual([u['id'] for u in CANDIDATE['units']],list(tail.UNIT_DIGESTS))
 def test_descriptor_mutations_rejected(self):
  for mutate in (lambda x:x['units'].reverse(),lambda x:x['functions'][0].update(size=1),lambda x:x['units'][0].update(source='wrong.cpp')):
   x=copy.deepcopy(CANDIDATE);mutate(x)
   with self.assertRaises(ValueError):tail.bind_candidate(DEFAULT,x,tail.CANDIDATE_PATH)
 def test_default_and_candidate_dispatch(self):
  before=copy.deepcopy(DEFAULT);bomb.bind_default(DEFAULT);self.assertEqual(DEFAULT,before);combined=replay.add_candidate_owners(DEFAULT,CANDIDATE);self.assertEqual((len(combined['units']),len(combined['functions']),sum(f['size'] for f in combined['functions'])),(76,399,63194))
  with self.assertRaises(ValueError):tail.bind_candidate(DEFAULT,CANDIDATE,bomb.CANDIDATE_PATH)
  with self.assertRaises(ValueError):replay.add_candidate_owners(combined,CANDIDATE)
 @unittest.skipUnless(HAS_PRIVATE,'private retained proof fixtures unavailable')
 def test_root_response_equivalence(self):
  raw=(BASE/'th03_main.asm').read_bytes();new,refs=tail.transform(raw);self.assertEqual(tail.sha(new),tail.ROOT_AFTER);self.assertEqual(new,(RETAINED/'th03_main.asm').read_bytes());self.assertEqual(tail.response((BASE/'obj/th03/main.@l').read_bytes()),(RETAINED/'obj/th03/main.@l').read_bytes())
  with self.assertRaises(ValueError):tail.transform(raw+b'\n')
 def test_scoped_background_paths(self):
  extra={n:'hash' for n in tail.EXTRA_GAME_PATHS};self.assertEqual(tail.scoped_game_objects({},extra),extra)
  with self.assertRaises(ValueError):tail.scoped_game_objects(extra,extra)
@unittest.skipUnless(HAS_PRIVATE,'private retained proof fixtures unavailable')
class StageSchedule(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='tail-contract-',dir=ROOT.parent);self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve();self.env={'WINEPREFIX':'offline-only'};self.events=[];self.mutation=None
  self.scheduler=schedule.Schedule(self.execute,self.root,'stage',candidate=True)
  a=patch('subprocess.Popen',side_effect=AssertionError('native forbidden'));a.start();self.addCleanup(a.stop)
  a=patch.object(schedule.subprocess,'run',side_effect=self.build);a.start();self.addCleanup(a.stop)
  # Match future installed module's repository location; only data-root lookup changes.
  a=patch.object(tail,'__file__',str(PRIVATE/'scripts/lib/th03_player_tail_candidate.py'));a.start();self.addCleanup(a.stop)
 def source(self,n=1):
  work=self.scheduler.output/('round'+str(n))/'source';work.mkdir(parents=True)
  (work/'th03_main.asm').write_bytes((PRIVATE/'_reference/ReC98/th03_main.asm').read_bytes())
  for u in bomb.pre_bomb_config(DEFAULT)['units']:replay.apply_carrier_edits(u,work)
  for name in set(tail.SOURCE_PINS)|set(bomb.SOURCE_PINS):
   out=work/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((PRIVATE/name).read_bytes())
  for name in ('build.bat','Tupfile.lua','Tupfile.ini','bin/tup.exe'):
   out=work/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((BASE/name).read_bytes())
  bomb.stage_bomb(work,default=True)
  u=next(u for u in DEFAULT['units'] if bomb.is_bomb_owner(u));p=work/u['build_file'];text=p.read_text();self.assertEqual(text.count(u['build_anchor']),1);p.write_text(text.replace(u['build_anchor'],u['build_replacement'],1))
  self.assertEqual(tail.sha((work/'th03_main.asm').read_bytes()),tail.ROOT_SHA);self.assertFalse((work/'obj').exists());return work
 def execute(self,argv,work,env,log):
  self.assertEqual(env,self.env)
  if 'tcc -c' in argv[-1]:
   self.assertEqual(tail.sha((work/'build.bat').read_bytes()),schedule.BUILD_SHA);self.assertFalse((work/'.tup').exists())
   name=next((n for n,s in tail.OBJECTS.items() if ('src/main/'+('background/' if n.startswith('chain') else 'player/')+n+'.cpp') in argv[-1]),'bomb')
   if name=='bomb':
    self.assertEqual(list(work.rglob('*.obj')),[]);out=work/bomb.ALIAS;data=(RETAINED/bomb.OBJECT).read_bytes()
   else:
    self.assertTrue((work/bomb.OBJECT).is_file());out=work/tail.OBJECTS[name];data=(RETAINED/tail.OBJECTS[name]).read_bytes()
   out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);self.events.append(name)
   if self.mutation and name!='bomb':self.mutation(work,name)
  elif argv[-1]==r'bin\tup init':(work/'.tup').mkdir();(work/'.tup/db').write_bytes(b'offline database');self.events.append('init')
  elif argv[-1]==r'bin\tup options':log.write_bytes(b"Parsed option file: .tup/options\nupdater.num_jobs = '1' from .tup/options\n");self.events.append('options')
  else:self.fail('unexpected execute '+repr(argv))
  return {'exit_code':0,'simulated_test_only':True}
 def build(self,argv,*,cwd,env,stdout,stderr,timeout):
  self.assertEqual(argv,schedule.BUILD_ARGV);self.assertEqual(timeout,300);self.assertEqual((cwd/'.tup/options').read_bytes(),schedule.OPTIONS);self.assertEqual(tail.sha((cwd/'th03_main.asm').read_bytes()),tail.ROOT_AFTER);self.assertEqual(tail.sha((cwd/'build.bat').read_bytes()),bomb.BUILD_STAGED_SHA);self.events.append('build');return SimpleNamespace(returncode=0,stdout=b'offline no native')
 def bomb_first(self,work):return bomb.precompile(work,self.env,work.parent,self.scheduler,default=True)
 def test_two_fresh_stages_real_schedule(self):
  for n in (1,2):
   work=self.source(n);self.bomb_first(work);result=tail.precompile_and_stage(work,self.env,work.parent,self.scheduler);self.assertEqual(result['fresh_native_compilations'],4);self.assertEqual(self.scheduler(schedule.BUILD_ARGV,work,self.env,work.parent/'cold-build.log')['exit_code'],0)
  self.assertEqual(self.events,['bomb','warning','effects','chain1','chain2','init','options','build']*2);self.assertEqual(len(self.scheduler.rounds),2)
 def test_missing_bomb_boundary_rejected(self):
  work=self.source()
  with self.assertRaises((ValueError,FileNotFoundError)):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
  self.assertEqual(self.events,[])
 def test_stale_tail_rejected(self):
  work=self.source();self.bomb_first(work);(work/tail.OBJECTS['warning']).write_bytes(b'stale')
  with self.assertRaises(ValueError):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
  self.assertEqual(self.events,['bomb'])
 def test_existing_output_mutation_rejected(self):
  work=self.source();self.bomb_first(work);self.mutation=lambda w,n:(w/bomb.OBJECT).write_bytes(b'mutated')
  with self.assertRaisesRegex(ValueError,'outputs/mutation'):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
 def test_extra_output_rejected(self):
  work=self.source();self.bomb_first(work);self.mutation=lambda w,n:(w/'obj/extra.obj').write_bytes(b'extra')
  with self.assertRaisesRegex(ValueError,'outputs/mutation'):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
 def test_source_mutation_rejected(self):
  work=self.source();self.bomb_first(work);self.mutation=lambda w,n:(w/'src/main/player/warning.cpp').write_bytes(b'changed')
  with self.assertRaisesRegex(ValueError,'source changed'):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
 def test_crossmode_prestaged_build_rejected(self):
  work=self.source();self.bomb_first(work);p=work/'build.bat';p.write_bytes(p.read_bytes().replace(schedule.BEFORE,schedule.AFTER,1))
  with self.assertRaises(ValueError):tail.precompile_and_stage(work,self.env,work.parent,self.scheduler)
  self.assertEqual(self.events,['bomb'])
 def test_default_schedule_rejects_tail_candidate_carrier(self):
  work=self.source();self.bomb_first(work);tail.precompile_and_stage(work,self.env,work.parent,self.scheduler);self.scheduler.candidate=False
  with self.assertRaises(ValueError):self.scheduler(schedule.BUILD_ARGV,work,self.env,work.parent/'cold-build.log')
  self.assertNotIn('init',self.events)
@unittest.skipUnless(HAS_PRIVATE,'private retained proof fixtures unavailable')
class CompleteRetainedRound(unittest.TestCase):
 def test_full_round_with_explicit_artifact_fixture(self):
  # Offline fixture only: individual known manifest artifacts, never a recursive
  # proof-tree copy, and never an input to a native build.
  proof=tail.guard_baseline(PRIVATE);receipt=json.loads((PRIVATE/tail.BASELINE/'receipt.json').read_text());prefix='round1/source/'
  names=set(receipt['rounds'][0]['all_objects'])
  import re
  names.update(n[len(prefix):] for n in proof if n.startswith(prefix) and (re.fullmatch(r'bin/th0[1-5]/[^/]+\.(?:exe|com)',n[len(prefix):]) or n.endswith('.map')))
  names.update(set(tail.SOURCE_PINS)|set(bomb.SOURCE_PINS));names.update(('build.bat','obj/th03/main.@l','th03_main.asm'))
  with tempfile.TemporaryDirectory(prefix='tail-full-round-',dir=ROOT.parent) as tmp:
   work=Path(tmp)
   for name in names:
    source=(PRIVATE/name) if name in tail.SOURCE_PINS or name in bomb.SOURCE_PINS else BASE/name
    dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(source.read_bytes())
   for name in ('th03_main.asm','obj/th03/main.obj','obj/th03/main.@l','obj/th03/main.map','bin/th03/main.exe',*tail.OBJECTS.values()):
    dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((RETAINED/name).read_bytes())
   build=work/'build.bat';build.write_bytes(build.read_bytes().replace(schedule.BEFORE,schedule.AFTER,1))
   expected=tail.freeze_expected(PRIVATE)
   with patch('subprocess.Popen',side_effect=AssertionError('native forbidden')):
    result=tail.check_round(PRIVATE,work,(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes(),proof,expected)
   self.assertTrue(result['pass_']);self.assertEqual([r['baseline_round'] for r in result['baselines']],[1,2]);self.assertTrue(all(r['pass_'] for r in result['baselines']))
   mp=work/'obj/th03/main.map';text=mp.read_text('latin1');group=bomb.groups(text)
   self.assertEqual(group,'\n  Address         ');changed=group.replace('Address','Addresses',1)
   raw=mp.read_bytes();mp.write_bytes(raw.replace(group.replace('\n','\r\n').encode(),changed.replace('\n','\r\n').encode(),1))
   self.assertEqual(score.map_rows(mp.read_text('latin1')),score.map_rows(text))
   with self.assertRaisesRegex(ValueError,'group'):
    tail.check_round(PRIVATE,work,(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes(),proof,expected)
   mp.write_bytes(raw)
   for name in (next(n for n in sorted(names) if n.startswith('bin/') and n.endswith('.exe') and n!='bin/th03/main.exe'),next(n for n in sorted(receipt['rounds'][0]['game_objects']) if n not in ('obj/th03/main.obj',bomb.OBJECT,'obj/th03/score_hud.obj'))):
    dest=work/name;saved=dest.read_bytes();changed=bytearray(saved);changed[-1]^=1;dest.write_bytes(changed)
    with self.subTest(mutation=name),self.assertRaises((ValueError,AssertionError)):
     tail.check_round(PRIVATE,work,(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes(),proof,expected)
    dest.write_bytes(saved)
   with patch.object(bomb,'check_providers',return_value={'pass_':False}),self.assertRaisesRegex(ValueError,'providers'):
    tail.check_round(PRIVATE,work,(PRIVATE/'.analysis/targets/th03/main.exe').read_bytes(),proof,expected)


if __name__=='__main__':unittest.main(verbosity=2)
