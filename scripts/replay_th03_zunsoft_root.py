#!/usr/bin/env python3
"""Fixed fresh-logo receipt replay; no compiler, Wine or runtime execution."""
from pathlib import Path
import argparse,hashlib,json,types,sys,os,tempfile
MANIFEST_SHA='a1eead9202ec501fc79c9eac7aca25507bd8426ba9c55af3c28dee3844ad2796'
VERIFIER_SHA='812ad68b11f7e7fb9625366590c3f5408c896e84c8770f914d6caaa4aa0e4c6d'
STAGE_SHA='94cb712decc830b2eb71c0d58f50f3170c524d03c5b260a2f528db66928180a1'
CREDIT_FLAGS=['exact_acceptance','whole_payload_ownership','launcher_ownership','two_cold_builds','runtime_rerun']
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='zunsoft-maintained-root-proof-v1','schema')
 need(all(p[k] is False for k in CREDIT_FLAGS),'credit inflation')
 need((p['native_phases'],p['root_procedures'],p['root_code_bytes'],p['root_data_bytes'],p['root_bss_bytes'],p['runtime_images'],p['runtime_calls'])==(2,10,1299,15,293,2,2600),'bounded counts')
 need(len(p['pins'])==len({q['path'] for q in p['pins']}),'duplicate pins')
 need(p['manifest_sha256']==MANIFEST_SHA and p['verifier_sha256']==VERIFIER_SHA,'fixed recipe identities')
 need(len(p['maintained_sources'])==6,'six maintained source inputs')
def replay(root,p,source_root=None):
 validate_proof(p);root=Path(root).resolve();source_root=Path(source_root or root).resolve();pins={q['path']:q for q in p['pins']}
 def read(n):
  need(n in pins,'unbound '+n);f=root/n;need(not any(x.is_symlink() for x in (f,*f.parents)) and f.is_file(),'regular input');b=f.read_bytes();q=pins[n];need(sha(b)==q['sha256'] and len(b)==q['bytes'],'input drift '+n);return b
 for n in pins:read(n)
 proposal='.analysis/zunsoft-native-proposal-20261021-v01';out='.analysis/zunsoft-native-output-20261021-v01';verifier='.analysis/zunsoft-native-20261021-v02/verify.py';runtime='.analysis/zunsoft-native-20261021-v02/parent-runtime-verification.json'
 manifest=read(proposal+'/manifest.json');need(sha(manifest)==MANIFEST_SHA and read(out+'/manifest.json')==manifest,'executed manifest identity');m=json.loads(manifest)
 for n,q in p['maintained_sources'].items():
  f=source_root/n;need(f.is_file() and not any(x.is_symlink() for x in (f,*f.parents)),'maintained regular source');b=f.read_bytes();need(sha(b)==q['sha256'] and len(b)==q['bytes'] and b==read(m['work']+'/'+n),'maintained-to-consumed binding '+n)
 stagepath=source_root/'scripts/stage_th03_zunsoft.py';stagebytes=stagepath.read_bytes();need(sha(stagebytes)==STAGE_SHA,'maintained stage identity');stage=types.ModuleType('zunsoft_maintained_stage');stage.__file__=str(stagepath);exec(compile(stagebytes,str(stagepath),'exec'),stage.__dict__);overlay=stage.read_inputs(source_root);need(set(overlay)==set(p['maintained_sources']),'maintained input closure');need(all(b==read(m['work']+'/'+n) for n,b in overlay.items()),'regenerated overlay binding')
 policy_path=m['registry_policy']['path'];raw=read(policy_path);policy=types.ModuleType('zunsoft_fixed_registry');policy.__file__=str(root/policy_path);sys.modules[policy.__name__]=policy;exec(compile(raw,policy.__file__,'exec'),policy.__dict__)
 registry={n:q['sha256'] for n,q in m['registry_baseline'].items()}
 for phase in ['compile','link']:
  start=json.loads(read(out+'/'+phase+'-started.json'));transition=json.loads(read(out+'/'+phase+'-registry-transition.json'))
  before={n:read(out+'/'+phase+'-before-'+n) for n in ['user.reg','system.reg']};after={n:read(out+'/'+phase+'-after-'+n) for n in before}
  need({n:sha(b) for n,b in before.items()}==registry==json.loads(read(out+'/'+phase+'-before-registry.json')),'registry continuity')
  registry={n:sha(b) for n,b in after.items()};need(registry==json.loads(read(out+'/'+phase+'-after-registry.json')),'registry after hashes')
  recomputed=policy.validate_transition(before,after,phase_start_utc=start['started_utc'],phase_end_utc=transition['phase_end_utc'],child_tz='UTC');need(json.loads(json.dumps(recomputed))==transition and transition['ok'],'registry policy replay')
 need(registry=={n:q['sha256'] for n,q in json.loads(read(out+'/next-registry-baseline.json')).items()},'terminal registry continuity')
 raw=read(verifier);need(sha(raw)==VERIFIER_SHA,'fixed reviewed verifier');mod=types.ModuleType('zunsoft_fixed_verifier');mod.__file__=str(root/verifier)
 oldcwd=Path.cwd();oldargv=sys.argv[:];oldpath=sys.path[:]
 try:
  os.chdir(root);exec(compile(raw,mod.__file__,'exec'),mod.__dict__)
  with tempfile.TemporaryDirectory(prefix='zunsoft-offline-',dir=root/'.analysis') as tmp:
   output=Path(tmp)/'structural.json';sys.argv=[verifier,'--proposal',proposal,'--manifest-sha256',MANIFEST_SHA,'--output',str(output)];need(mod.main()==0,'fresh structural replay');structural=json.loads(output.read_text())
 finally:os.chdir(oldcwd);sys.argv=oldargv;sys.path[:]=oldpath
 observed=json.loads(read(runtime));need(observed['diagnostic_checks_pass'] and len(observed['checks'])==15 and all(v is True for v in observed['checks'].values()),'runtime receipt checks')
 need(observed['runtime_image_count']==2 and observed['runtime_calls_per_image']==1300 and observed['runtime_total_calls']==2600 and observed['runtime']['target']==observed['runtime']['current'],'one target plus one candidate model trace')
 need(observed['source_binding_manifest_sha256']==MANIFEST_SHA and not observed['historical_cache_used'] and all(observed[k] is False for k in ['exact_acceptance','whole_payload_ownership','launcher_ownership']),'runtime scope and source binding')
 for k,v in structural.items():
  if k in ['runtime','runtime_image_count','runtime_calls_per_image','runtime_total_calls']:continue
  if k=='checks':need(v=={n:x for n,x in observed[k].items() if n!='bounded_runtime_matrix'},'structural checks match runtime report')
  else:need(v==observed[k],'structural report differs '+k)
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_invocations_now=0,native_phases_replayed=2,structural_checks=14,retained_runtime_checks=15,retained_runtime_calls=2600,root_procedures=10,root_code_bytes=1299,root_data_bytes=15,root_bss_bytes=293,payload_diagnostic_bytes=10096,payload_sha256=observed['current_sha256'],source_binding=True,exact_acceptance=False,whole_payload_ownership=False,launcher_ownership=False,two_cold_builds=False,runtime_rerun=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/zunsoft_root/proof.json').read_text());r=replay(a.repo_root,p,a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
