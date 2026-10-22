#!/usr/bin/env python3
"""Guarded offline replay of three OP helper native producers. No native/model runs."""
from pathlib import Path
import argparse, hashlib, json, sys, types
PROPOSAL='.analysis/op-exit-helpers-native-proposal-v01'
OUT='.analysis/op-exit-helpers-native-output-v01'
MANIFEST_SHA='2cfe7239eb3749a3a79adef03e663904566538146efab4728edb52a5236832b9'
VERIFIER_SHA='56f65c943513d604e47ada916af46b7ac6ca907b57cbdaf186684600a0217222'
PHASES=['compile_exit_dos','compile_vplanset','compile_exit','link']
FLAGS=('source_acceptance','exact_acceptance','whole_product_ownership','cold_build','two_cold_builds','runtime_rerun','packing_run')
SOURCE_CLOSURE={'src/op/core/exit_dos.cpp','src/op/core/exit.cpp','src/op/hardware/vram_planes_set.cpp','compat/rec98/planar.h','compat/rec98/th01/hardware/vplanset.h','compat/rec98/th02/core/initexit.h','compat/rec98/libs/master.lib/master.hpp','compat/rec98/libs/master.lib/pc98_gfx.hpp','config/th03_op_exit_helpers_candidate.json','scripts/stage_th03_op_exit_helpers.py','scripts/replay_th03_op_exit_helpers.py'}
HELPER_CLOSURE={'scripts/lib/__init__.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/review_th03_decoded_code.py','scripts/inventory_rec98_th03.py','config/targets.toml'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def regular(root,name):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe input path');p=Path(root)/p
 need(not any(x.is_symlink() for x in (p,*p.parents)) and p.is_file(),'regular input '+name);return p

def validate_proof(p):
 need(p['schema']=='th03-op-exit-helpers-proof-v1','schema')
 need(all(p[n] is False for n in FLAGS),'credit inflation')
 need((p['native_phases'],p['fresh_owner_objects'],p['new_owner_bytes'],p['retained_context_objects'],p['preserved_prior_owners'],p['preserved_prior_bytes'])==(4,3,133,24,34,12436),'bounded scope')
 need(p['manifest_sha256']==MANIFEST_SHA and p['verifier_sha256']==VERIFIER_SHA,'recipe identity')
 need(set(p['maintained_closure'])==SOURCE_CLOSURE and set(p['helper_closure'])==HELPER_CLOSURE,'current source/helper closure')

def validate_phase(phase,start,finish,m,env):
 need(start['argv']==m['native_argv'][phase],'actual phase argv')
 need(Path(start['cwd']).parts[-len(Path(m['work']).parts):]==Path(m['work']).parts,'actual phase cwd')
 need(start['environment']==env['environment'],'phase environment')
 need(start['wait_seconds']==90 and start['cleanup_seconds']==15,'phase bounds')
 need(len(env['cpu'])==1 and env['nice']>=10,'resource bounds')
 need(start['environment']['DISPLAY']==start['environment']['WAYLAND_DISPLAY']=='' and start['environment']['TZ']=='UTC','headless UTC')
 need(type(finish['exit_code']) is int and finish['exit_code']==0,'phase exit')
 need(all(finish[n] is False for n in ('timeout','cleanup_uncertain','poison')),'unsafe cleanup')
 need(finish['initial_inventory_complete'] is True and finish['inventory_complete'] is True and finish['survivors']==[] and finish['errors']==[],'owned cleanup inventory')

def validate_report(r):
 need(r['diagnostic_checks_pass'] is True and r['source_integrity_checked'] is True,'native diagnostics')
 need(all(r[n] is False for n in ('source_acceptance','exact_acceptance','whole_product_ownership','cold_build','runtime_run')),'diagnostic scope')
 need(r['new_helper_bytes']==133 and r['new_helper_all_raw_ordered_pass'] is True,'new owner bytes')
 need([(x['name'],x['offset'],x['size']) for x in r['new_helpers']]==[('game_exit_to_dos',8,25),('vram_planes_set',33,41),('game_exit',274,67)],'new owner extents')
 for x in r['new_helpers']:
  need(all(x[n] is True for n in ('target_raw_equal','baseline_raw_equal','target_ordered_equal','baseline_ordered_equal','far_cdecl_return')),'new owner comparisons')
 need(len(r['objects'])==3 and len(r['retained_project_context'])==24,'fresh/retained object partition')
 need((r['prior_owner_count'],r['prior_owner_bytes'],len(r['prior_owners']))==(34,12436,34) and r['prior_owners_preserved'] is True,'prior owned scope')
 need(all(all(x[n] is True for n in ('baseline_raw_equal','baseline_ordered_equal','map_preserved')) for x in r['prior_owners']),'prior owner preservation')
 need(r['all_map_publics_preserved'] is True and r['baseline_whole_program_and_order_preserved'] is True,'baseline identity')
 need(r['whole_program']['target_different_bytes']==6 and r['whole_ordered_relocations']['target_different_positions']==313 and r['whole_ordered_relocations']['target_equal'] is False and r['whole_file_equal_target'] is False,'global target negatives')

def guard_current(root,p,source_root,m):
 # Guard the real current import closure before importing ANY repository helper.
 # Only maintained source/overlay files may come from the explicit pre-install root.
 for n,q in p['helper_closure'].items():
  b=regular(root,n).read_bytes();need(q=={k:m['sources'][n][k] for k in ('sha256','bytes')} and sha(b)==q['sha256'] and len(b)==q['bytes'],'current helper before import '+n)
 for n,q in p['maintained_closure'].items():
  b=regular(source_root,n).read_bytes();need(sha(b)==q['sha256'] and len(b)==q['bytes'],'current maintained source/helper '+n)

def replay(root,p,source_root=None):
 root=Path(root).resolve();source_root=Path(source_root or root).resolve();validate_proof(p)
 q=p['inventory'];raw=regular(root,q['path']).read_bytes();need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'inventory identity');inv=json.loads(raw)
 need(inv['metadata']=={k:v for k,v in p.items() if k!='inventory'},'inventory metadata')
 rows=inv['pins'];need(len(rows)==len({x['path'] for x in rows}),'duplicate inventory pins');pins={x['path']:x for x in rows}
 need(inv['inputs']=={n:{'sha256':q['sha256'],'bytes':q['bytes']} for n,q in pins.items()},'cleanup retention mirror')
 def read(n):
  need(n in pins,'unbound '+n);b=regular(root,n).read_bytes();q=pins[n];need(sha(b)==q['sha256'] and len(b)==q['bytes'],'input drift '+n);return b
 def js(n):return json.loads(read(n))
 for n in pins:read(n)
 m=js(PROPOSAL+'/manifest.json');need(sha(read(PROPOSAL+'/manifest.json'))==MANIFEST_SHA and read(PROPOSAL+'/manifest.json')==read(OUT+'/manifest.json'),'consumed native recipe')
 guard_current(root,p,source_root,m)
 def load(name,path,body=None,base=root):
  raw=read(path) if body is None else body;mod=types.ModuleType(name);mod.__file__=str(base/path);sys.modules[name]=mod;exec(compile(raw,mod.__file__,'exec'),mod.__dict__);return mod
 stagepath='scripts/stage_th03_op_exit_helpers.py';stage=load('op_exit_maintained_stage',stagepath,regular(source_root,stagepath).read_bytes(),source_root)
 cfg,data=stage.read_inputs(source_root);need(set(data)==SOURCE_CLOSURE-{'config/th03_op_exit_helpers_candidate.json',stagepath,'scripts/replay_th03_op_exit_helpers.py'},'maintained body/compat closure')
 baseline_root=Path(m['baseline_exe']['path']).parents[2]
 for u in cfg['units']:
  for n,k in ((u['wrapper'],'original_wrapper_sha256'),(u['original_body'],'original_body_sha256')):need(sha(read(str(baseline_root/n)))==u[k],'original producer source '+n)
 archive='.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar';need(sha(read(archive))==cfg['reference_archive_sha256'],'original frozen reference archive')
 boundary=js(m['target_boundary_report']['path'])
 for n,digest in boundary['inputs'].items():need(sha(read(n))==digest,'target boundary input '+n)
 overlay=stage.payload(source_root);need(len(overlay)==13,'physical TU overlay size')
 for n,b in overlay.items():need(b==read(m['work']+'/'+n),'maintained-to-consumed source '+n)
 need(m['phases']==PHASES and len(m['retained_objects'])==24 and len(m['new_owner_objects'])==3 and not set(m['retained_objects'])&set(m['new_owner_objects']),'producer partition')
 need(not m['compose_sources'] and m['predecessor'] is None and not m['accumulated_objects'],'fresh owner outputs')
 need(set(m['retained_objects'])=={n for n in m['repeat_inputs'] if Path(n).suffix.lower() in ('.obj','.exe','.map','.lib','.com')},'only declared retained binaries')
 material=js(OUT+'/materialized-inputs.json');times=js(OUT+'/source-mtimes.json');need(set(material)==set(times)==set(m['repeat_inputs']),'materialized closure')
 for n,q in m['repeat_inputs'].items():
  a=regular(root,q['path']);b=regular(root,m['work']+'/'+n);need(read(q['path'])==read(m['work']+'/'+n),'snapshot to consumed '+n)
  need(a.stat().st_ino!=b.stat().st_ino and a.stat().st_mtime_ns==b.stat().st_mtime_ns==q['mtime_ns']==times[n],'source copy/mtime identity')
  need(material[n]=={k:q[k] for k in ('sha256','bytes','mode')},'materialized metadata')
 environment=js(OUT+'/environment.json');policy=load('op_exit_registry_policy',m['registry_policy']['path']);registry={n:q['sha256'] for n,q in m['registry_baseline'].items()}
 for phase in PHASES:
  a=js(OUT+'/'+phase+'-started.json');z=js(OUT+'/'+phase+'-finished.json');tr=js(OUT+'/'+phase+'-registry-transition.json');validate_phase(phase,a,z,m,environment);need(Path(a['cwd'])==root/m['work'],'absolute consumed cwd')
  before={n:read(OUT+'/'+phase+'-before-'+n) for n in ('user.reg','system.reg')};after={n:read(OUT+'/'+phase+'-after-'+n) for n in before}
  need({n:sha(b) for n,b in before.items()}==registry==js(OUT+'/'+phase+'-before-registry.json'),'registry continuity');registry={n:sha(b) for n,b in after.items()};need(registry==js(OUT+'/'+phase+'-after-registry.json'),'registry after')
  actual=policy.validate_transition(before,after,phase_start_utc=a['started_utc'],phase_end_utc=tr['phase_end_utc'],child_tz='UTC');need(json.loads(json.dumps(actual))==tr and tr['ok'],'registry policy')
  output=read(m['work']+'/'+m['native_outputs'][phase]);receipt=js(OUT+'/'+phase+'-output.json');need(sha(output)==receipt['sha256'] and len(output)==receipt['bytes'],'actual phase output')
 need(registry=={n:q['sha256'] for n,q in js(OUT+'/next-registry-baseline.json').items()},'terminal registry')
 done=js(OUT+'/completion.json');need(done['complete'] is True and done['errors']==[] and done['owned_lock_released'] is True and done['native_invocations']==4 and done['phases']==PHASES and done['runtime_run'] is False and done['source_acceptance'] is False and done['exact_acceptance'] is False,'completion')
 need(sha(read(m['verifier']['path']))==VERIFIER_SHA,'native verifier identity');verifier=load('op_exit_native_verifier',m['verifier']['path']);verifier.ROOT=root
 fresh=json.loads(json.dumps(verifier.verify(root/m['work'],m)));need(fresh==js(OUT+'/linked-verification.json'),'fresh structural replay');validate_report(fresh)
 for obj in fresh['objects']:
  for n in set(obj['dependency_paths']):need(n in m['repeat_inputs'] and read(m['work']+'/'+n)==read(m['repeat_inputs'][n]['path']),'actual OMF source dependency '+n)
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),current_helper_closure=len(HELPER_CLOSURE),maintained_closure=len(SOURCE_CLOSURE),source_binding=True,native_phases_replayed=4,native_invocations_now=0,fresh_owner_objects=3,new_owner_bytes=133,retained_context_objects=24,preserved_prior_owners=34,preserved_prior_bytes=12436,candidate_sha256=fresh['candidate_sha256'],whole_program_different_bytes=6,whole_ordered_relocations_equal=False,**{n:False for n in FLAGS})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--source-root',type=Path);ap.add_argument('--proof',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/op_exit_helpers/proof.json').read_text());r=replay(a.repo_root,p,a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
