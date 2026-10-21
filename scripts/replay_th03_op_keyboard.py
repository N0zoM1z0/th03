#!/usr/bin/env python3
"""Offline maintained OP scanner receipt replay. No compiler, Wine or model rerun."""
from pathlib import Path
import argparse,hashlib,json,sys,types
MANIFEST_SHA='ea038d64d8802987e25e310d30060dbb180cccc186dddf57ac52ee865afdb3d7'
VERIFIER_SHA='62f710c1ee7726d93b783338c2385bd554ee94af06d5f75964c07f03985421ac'
CREDIT_FLAGS=['exact_acceptance','whole_product_ownership','maintained_cohort_preserved','two_cold_builds','runtime_rerun']
PROPOSAL='.analysis/op-keyboard-native-proposal-v01';OUT='.analysis/op-keyboard-native-output-v01'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='th03-op-keyboard-source-proof-v1','schema')
 need(all(p[k] is False for k in CREDIT_FLAGS),'credit inflation')
 need((p['native_phases'],p['scanner_bytes'],p['carrier_context_bytes'],p['runtime_images'],p['runtime_calls'])==(2,417,418,2,536),'bounded counts')
 need(p['manifest_sha256']==MANIFEST_SHA and p['verifier_sha256']==VERIFIER_SHA,'recipe identities')
 need(len(p['maintained_sources'])==5,'maintained closure')
 need(len(p['pins'])==len({q['path'] for q in p['pins']}),'duplicate pins')
def validate_phase(phase,start,finish,m,env):
 need(start['argv']==m['native_argv'][phase],'actual phase argv')
 need(Path(start['cwd']).parts[-len(Path(m['work']).parts):]==Path(m['work']).parts,'actual phase cwd')
 need(start['environment']==env['environment'],'phase environment')
 need(start['wait_seconds']==90 and start['cleanup_seconds']==15,'phase bounds')
 need(len(env['cpu'])==1 and env['nice']>=10,'resource bounds')
 need(start['environment']['DISPLAY']==start['environment']['WAYLAND_DISPLAY']=='' and start['environment']['TZ']=='UTC','headless UTC')
 need(finish['exit_code']==0 and type(finish['exit_code']) is int,'phase exit')
 need(all(finish[k] is False for k in ['timeout','cleanup_uncertain','poison']),'unsafe cleanup')
 need(finish['initial_inventory_complete'] is True and finish['inventory_complete'] is True and finish['survivors']==[] and finish['errors']==[],'owned cleanup inventory')
def validate_runtime(r):
 need(r['diagnostic_checks_pass'] is True and r['runtime_run'] is True,'runtime status')
 need(all(r[k] is False for k in ['source_acceptance','exact_acceptance','maintained_cohort_preserved']),'runtime scope')
 expected=dict(positions=278,complete=True,invocations=268,returns=264,prefixes=4);runtime=r['runtime']
 need(runtime['target_coverage']==runtime['candidate_coverage']==expected,'runtime counts')
 need(runtime['semantic_equal'] is True,'runtime semantic verdict')
 def semantic(rows):return [{k:v for k,v in row.items() if k not in ('before_sha256','after_sha256')} for row in rows]
 a,b=runtime['target_rows'],runtime['candidate_rows'];need(len(a)==len(b)==268 and semantic(a)==semantic(b),'retained actual model rows')
 for rows in (a,b):
  need(sum(x['terminal'] for x in rows)==264,'terminal returns')
  need(len({at for x in rows for at in x['visited']})==278,'retained coverage positions')
  for x in rows:need(x['physical_outside_stack_checked'] and x['unchanged_outside_state_checked'],'runtime memory scope')
def replay(root,p,source_root=None):
 validate_proof(p);root=Path(root).resolve();source_root=Path(source_root or root).resolve()
 if 'inventory' in p:
  q=p['inventory'];f=root/q['path'];need(p['pins']==[q],'compact inventory binding');need(not any(x.is_symlink() for x in (f,*f.parents)),'inventory regular file');raw=f.read_bytes();need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'inventory identity');expanded=json.loads(raw)
  need({k:v for k,v in p.items() if k not in ['inventory','pins']}=={k:v for k,v in expanded.items() if k!='pins'},'inventory metadata binding');p=expanded;validate_proof(p)
 pins={q['path']:q for q in p['pins']}
 def read(n):
  need(n in pins,'unbound '+n);f=root/n;need(not any(x.is_symlink() for x in (f,*f.parents)) and f.is_file(),'regular pinned input');raw=f.read_bytes();q=pins[n];need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'pin drift '+n);return raw
 for n in pins:read(n)
 raw=read(PROPOSAL+'/manifest.json');need(sha(raw)==MANIFEST_SHA and read(OUT+'/manifest.json')==raw,'consumed manifest identity');m=json.loads(raw)
 def load(name,path):
  mod=types.ModuleType(name);mod.__file__=str(root/path);sys.modules[name]=mod;exec(compile(read(path),mod.__file__,'exec'),mod.__dict__);return mod
 stagepath='scripts/stage_th03_op_keyboard.py';stagebytes=(source_root/stagepath).read_bytes();need(sha(stagebytes)==p['stage_sha256'],'stage identity');stage=types.ModuleType('op_scanner_stage');stage.__file__=str(source_root/stagepath);exec(compile(stagebytes,stage.__file__,'exec'),stage.__dict__)
 data=stage.read_inputs(source_root);need(set(data)==set(p['maintained_sources']),'source input closure')
 for n,body in stage.payload(source_root).items():need(body==read(m['work']+'/'+n),'staged actual consumed source '+n)
 for n,q in p['maintained_sources'].items():need(sha(data[n])==q['sha256'] and len(data[n])==q['bytes'],'maintained source hash')
 environment=json.loads(read(OUT+'/environment.json'));policy=load('op_registry_policy',m['registry_policy']['path']);registry={n:q['sha256'] for n,q in m['registry_baseline'].items()}
 for phase in ['compile','link']:
  start=json.loads(read(OUT+'/'+phase+'-started.json'));finish=json.loads(read(OUT+'/'+phase+'-finished.json'));transition=json.loads(read(OUT+'/'+phase+'-registry-transition.json'));validate_phase(phase,start,finish,m,environment);need(Path(start['cwd'])==root/m['work'],'absolute consumed work directory')
  before={n:read(OUT+'/'+phase+'-before-'+n) for n in ['user.reg','system.reg']};after={n:read(OUT+'/'+phase+'-after-'+n) for n in before}
  need({n:sha(v) for n,v in before.items()}==registry==json.loads(read(OUT+'/'+phase+'-before-registry.json')),'registry continuity')
  registry={n:sha(v) for n,v in after.items()};need(registry==json.loads(read(OUT+'/'+phase+'-after-registry.json')),'after registry hashes')
  recomputed=policy.validate_transition(before,after,phase_start_utc=start['started_utc'],phase_end_utc=transition['phase_end_utc'],child_tz='UTC');need(json.loads(json.dumps(recomputed))==transition and transition['ok'],'registry policy replay')
  output=m['native_outputs'][phase];pin=json.loads(read(OUT+'/'+phase+'-output.json'));need(sha(read(m['work']+'/'+output))==pin['sha256'],'actual phase output')
 need(registry=={n:q['sha256'] for n,q in json.loads(read(OUT+'/next-registry-baseline.json')).items()},'terminal registry')
 dependency='scripts/inventory_rec98_th03.py';path=root/dependency;need(not any(x.is_symlink() for x in (path,*path.parents)),'import helper regular input');raw=path.read_bytes();guard=m['sources'][dependency];need(sha(raw)==guard['sha256'] and len(raw)==guard['bytes'],'import helper identity')
 verifier=load('op_keyboard_fixed_verifier',PROPOSAL+'/verify.py');need(sha(read(PROPOSAL+'/verify.py'))==VERIFIER_SHA,'fixed verifier')
 fresh=json.loads(json.dumps(verifier.verify(root/m['work'],False)));stored=json.loads(read(OUT+'/structural-verification.json'));need(fresh==stored,'fresh structural replay')
 runtime=json.loads(read(OUT+'/runtime-verification.json'));validate_runtime(runtime)
 need({k:v for k,v in runtime.items() if k not in ['runtime','runtime_run']}=={k:v for k,v in fresh.items() if k not in ['runtime','runtime_run']},'runtime artifact binding')
 # OMF names prove the freshly compiled source path traversed both original wrapper slots.
 dependencies=fresh['object']['dependency_paths'];need(dependencies[:3]==['th03/input_s.cpp','th03/hardware/input_s.cpp','src/op/hardware/input_sense.cpp'],'OMF producer lineage')
 for name in set(dependencies):need(name in m['repeat_inputs'] and read(m['work']+'/'+name)==read(m['repeat_inputs'][name]['path']),'OMF dependency binding '+name)
 need(fresh['whole_program']['different_bytes']==6 and not fresh['whole_file_equal'] and not fresh['whole_ordered_relocations']['equal'],'preserved whole-image/ordered negatives')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_invocations_now=0,native_phases_replayed=2,scanner_bytes=417,carrier_context_bytes=418,nop_source_credit=0,retained_runtime_calls=536,source_binding=True,whole_program_different_bytes=6,whole_ordered_relocations_equal=False,**{k:False for k in CREDIT_FLAGS})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/op_keyboard/proof.json').read_text());result=replay(a.repo_root,p,a.source_root);raw=json.dumps(result,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
