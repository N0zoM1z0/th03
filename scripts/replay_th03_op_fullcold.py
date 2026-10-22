#!/usr/bin/env python3
"""Replay retained OP-only native receipts and structural diagnostics, never native/runtime."""
from pathlib import Path
import argparse, hashlib, json, sys, types
sha=lambda b:hashlib.sha256(b).hexdigest()
FLAGS=('exact_acceptance','source_acceptance','whole_product_ownership','runtime_rerun','packing_run')
def need(v,m):
 if not v:raise ValueError(m)
def regular(root,n):
 p=Path(n);need(not p.is_absolute() and '..' not in p.parts,'unsafe path');p=Path(root)/p
 need(not any(x.is_symlink() for x in (p,*p.parents)) and p.is_file(),'regular input '+n);return p
def validate_proof(p):
 need(p['schema']=='th03-op-fullcold-proof-v1','schema')
 need(all(p[k] is False for k in FLAGS),'credit inflation')
 need((p['rounds'],p['native_phases'],p['project_objects_per_round'],p['source_owners'],p['source_bytes'],p['cohort_bytes'])==(2,56,27,34,12436,9530),'bounded scope')
def validate_report(r,round):
 need(r['diagnostic_checks_pass'] and r['source_integrity_checked'],'diagnostics')
 need(all(r[k] is False for k in FLAGS),'diagnostic credit')
 need(r['all_owners_raw_pass'] and not r['all_owners_ordered_pass'],'owner negatives')
 need(r['candidate_cohort_raw_and_ordered_pass'] and r['candidate_cohort_units']==33 and r['candidate_cohort_bytes']==9530,'cohort')
 need(len(r['owners'])==34 and sum(int(x['size']) for x in r['owners'])==12436,'owner scope')
 bad=[x for x in r['owners'] if not x['ordered_relocations_equal']]
 need(len(bad)==1 and bad[0]['id'].endswith('character-selection') and int(bad[0]['size'])==2906,'selection negative')
 need(not r['whole_file_equal'] and r['whole_program']['different_bytes']==6 and not r['whole_ordered_relocations']['equal'],'whole negatives')
 need(r['whole_ordered_relocations']['different_positions']==313,'literal relocation order')
 need(len(r['raw_repeat_pairs'])==(29 if round==2 else 0) and r['two_round_raw_repeat_equal']==(round==2),'repeat scope')
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
def replay(root,p,source_root=None,stage_path=None,stage_config=None):
 validate_proof(p);root=Path(root).resolve();source_root=Path(source_root or root).resolve()
 q=p['inventory'];raw=regular(root,q['path']).read_bytes();need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'inventory pin');inv=json.loads(raw)
 need(inv['metadata']=={k:v for k,v in p.items() if k!='inventory'},'inventory metadata')
 pins=inv['pins'];need(len(pins)==len({x['path'] for x in pins}),'duplicate pins');pins={x['path']:x for x in pins}
 need(inv['inputs']=={n:{'sha256':q['sha256'],'bytes':q['bytes']} for n,q in pins.items()},'cleanup retention mirror')
 def read(n):
  need(n in pins,'unbound '+n);b=regular(root,n).read_bytes();q=pins[n];need(sha(b)==q['sha256'] and len(b)==q['bytes'],'input drift '+n);return b
 def js(n):return json.loads(read(n))
 for n in pins:read(n)
 def load(n,path):
  mod=types.ModuleType(n);mod.__file__=str(root/path);sys.modules[n]=mod;exec(compile(read(path),mod.__file__,'exec'),mod.__dict__);return mod
 st=Path(stage_path or source_root/'scripts/stage_th03_op_fullcold.py');b=st.read_bytes();need(sha(b)==p['stage_sha256'],'stage identity');stage=types.ModuleType('fullcold_stage');stage.__file__=str(st);exec(compile(b,str(st),'exec'),stage.__dict__)
 data=stage.payload(source_root,**({'config':Path(stage_config)} if stage_config else {}));need(len(data)==308,'source composition size')
 registry=None;first=None;reports=[];count=0
 for rnd in (1,2):
  for group in range(1,7):
   out=f'.analysis/op-fullcold-r{rnd}-g{group}-v01-output';prop=out.replace('-output','-proposal');m=js(out+'/manifest.json');need(read(out+'/manifest.json')==read(prop+'/manifest.json'),'consumed manifest')
   need((m['round'],m['group'],m['native_phase_count'])==(rnd,group,5 if group<6 else 3),'group shape')
   need(m['retained_objects']=={} and m['compose_sources'] is False,'no project object reuse')
   if first is None:first=m
   need(m['toolchain_inputs']==first['toolchain_inputs'] and m['fixed_mtimes']==first['fixed_mtimes'],'toolchain repeat declaration')
   if group==1:
    for n,t in m['fixed_mtimes'].items():need(regular(root,n).stat().st_mtime_ns==t,'tool timestamp drift')
    for n,q in m['repeat_inputs'].items():
     a=regular(root,q['path']);b=regular(root,m['work']+'/'+n);need(a.stat().st_ino!=b.stat().st_ino,'source snapshot reused inode')
     need(a.stat().st_mtime_ns==b.stat().st_mtime_ns==946684800000000000,'source timestamp drift')
     need(a.stat().st_mode&511==b.stat().st_mode&511==420,'source mode drift')
     if rnd==2:need(b.stat().st_ino!=regular(root,first['work']+'/'+n).stat().st_ino,'round reused source inode')
   for n,b in data.items():need(read(m['work']+'/'+n)==b,'current source to consumed '+n)
   material=js(out+'/materialized-inputs.json');times=js(out+'/source-mtimes.json');need(set(material)==set(times)==set(data),'materialized closure')
   for n,b in data.items():need(material[n]['sha256']==sha(b) and material[n]['bytes']==len(b) and material[n]['mode']==420 and times[n]==946684800000000000,'materialization identity')
   env=js(out+'/environment.json');policy=load('fullcold_registry',m['registry_policy']['path']);baseline={n:q['sha256'] for n,q in m['registry_baseline'].items()}
   if registry is not None:need(registry==baseline,'group registry continuity')
   registry=baseline
   for phase in m['phases']:
    a=js(out+'/'+phase+'-started.json');z=js(out+'/'+phase+'-finished.json');tr=js(out+'/'+phase+'-registry-transition.json');validate_phase(phase,a,z,m,env);need(Path(a['cwd'])==root/m['work'],'actual cwd')
    before={n:read(out+'/'+phase+'-before-'+n) for n in ('user.reg','system.reg')};after={n:read(out+'/'+phase+'-after-'+n) for n in before}
    need({n:sha(v) for n,v in before.items()}==registry==js(out+'/'+phase+'-before-registry.json'),'registry before')
    registry={n:sha(v) for n,v in after.items()};need(registry==js(out+'/'+phase+'-after-registry.json'),'registry after')
    actual=policy.validate_transition(before,after,phase_start_utc=a['started_utc'],phase_end_utc=tr['phase_end_utc'],child_tz='UTC');need(json.loads(json.dumps(actual))==tr and tr['ok'],'registry policy')
    output=read(m['work']+'/'+m['native_outputs'][phase]);receipt=js(out+'/'+phase+'-output.json');need(sha(output)==receipt['sha256'] and len(output)==receipt['bytes'],'actual produced output');count+=1
   need(registry=={n:q['sha256'] for n,q in js(out+'/next-registry-baseline.json').items()},'terminal registry')
   done=js(out+'/completion.json');need(done['complete'] and done['errors']==[] and done['owned_lock_released'] and done['native_invocations']==len(m['phases']) and done['phases']==m['phases'],'completion')
   if group==6:
    verifier=load('fullcold_verify',m['verifier']['path']);verifier.ROOT=root;fresh=json.loads(json.dumps(verifier.verify(root/m['work'],m)));stored=js(out+'/linked-verification.json');need(fresh==stored,'fresh structural recomputation');validate_report(fresh,rnd);reports.append(fresh)
 need(count==56,'native count');need(reports[0]['candidate_sha256']==reports[1]['candidate_sha256'],'same EXE')
 return dict(pass_checks=True,native_phases_replayed=count,native_invocations_now=0,two_independent_source_builds=True,raw_repeat_products=29,source_owners=34,source_bytes=12436,raw_and_ordered_candidate_cohort_bytes=9530,selection_ordered_negative=True,whole_program_different_bytes=6,**{k:False for k in FLAGS})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--stage-path',type=Path);ap.add_argument('--stage-config',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/op_fullcold/proof.json').read_text());r=replay(a.repo_root,p,a.source_root,a.stage_path,a.stage_config);raw=json.dumps(r,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
