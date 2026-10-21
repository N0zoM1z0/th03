#!/usr/bin/env python3
"""Read-only fixed-receipt replay of two current-source cold rounds; no native execution."""
from pathlib import Path
import argparse,hashlib,json,types,sys,os
VERIFIER_SHA='76463b7dc2d4ac69dbf7ce69c006252607e132c0d84c447b6b5b88be11d7929d'
STAGE_SHA='a5d6df2963c493ab8d6a4cf0a4c049b3621b9b5c23c25375767ff90bc2d9d6a5'
FINAL_MANIFESTS={'1': '58ecc650da00142d81536660def3de5442310254e2ad96f894183297a1f5de95', '2': '5783ebf023a9e4ec19c801204343cca19a21bfd8098b677ca5b94e9756426951'}
CREDIT_FLAGS=['source_acceptance','source_progress_changed','exact_acceptance','default_backend','runtime_rerun']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='mainl-current-fullcold-proof-v1','schema')
 need(all(p[k] is False for k in CREDIT_FLAGS),'formal credit inflation')
 need(p['rounds']==2 and p['groups']==20 and p['native_phases']==94,'complete cold experiment required')
 need(len(p['pins'])==len({r['path'] for r in p['pins']}),'duplicate pins')
def replay(root,p,source_root=None):
 validate_proof(p);root=Path(root).resolve();source_root=Path(source_root or root).resolve();pins={r['path']:r for r in p['pins']}
 def read(n):
  n=str(n);need(n in pins,'unbound '+n);q=root/n;need(q.is_file() and not q.is_symlink(),'regular input');b=q.read_bytes();row=pins[n];need(sha(b)==row['sha256'] and len(b)==row['bytes'],'pin drift '+n);return b
 for n in pins:read(n)
 def load(raw,path,name):
  mod=types.ModuleType(name);sys.modules[name]=mod;mod.__file__=str(path);exec(compile(raw,str(path),'exec'),mod.__dict__);return mod
 stagepath=source_root/'scripts/stage_th03_mainl_fullcold.py';stagebytes=stagepath.read_bytes();need(sha(stagebytes)==STAGE_SHA,'fixed maintained source composer')
 sys.path.insert(0,str(root/'scripts'));oldcwd=Path.cwd()
 try:
  os.chdir(root);stage=load(stagebytes,stagepath,'fixed_fullcold_source_stage');files,provenance,stages,graph,archive_sha=stage.compose_all()
 finally:os.chdir(oldcwd)
 policy_path='.analysis/zun-init-retained-continuation-20261021-v01/registry_policy.py';policyraw=read(policy_path)
 need(sha(policyraw)=='1ed9aa60a8ef1c619d9cadf01a62fffb5a1f17d9c93764fbd30b503fbaf597c7','fixed registry policy')
 policy=load(policyraw,root/policy_path,'fixed_fullcold_registry')
 need(len(files)==1904 and len(graph)==36,'source closure geometry')
 need(not any(Path(n).suffix.lower() in {'.obj','.exe','.map','.lib','.dll','.com'} for n in files),'source stage cannot carry native products')
 count=0;reports=[];first_inputs=None
 for rnd in [1,2]:
  prior=None;produced={};manifest=None
  for group in range(1,11):
   stem=f'.analysis/mainl-fullcold-r{rnd}-g{group}-20261021-v02';out=Path(stem+'-output');proposal=Path(stem+'-proposal')
   raw=read(proposal/'manifest.json');m=json.loads(raw);manifest=m
   need(read(out/'manifest.json')==raw,'actual manifest copy')
   if group==10:need(sha(raw)==FINAL_MANIFESTS[str(rnd)],'fixed final manifest')
   need(m['round']==rnd and m['group']==group and m['work']==f'.analysis/toolchain/wineprefix/drive_c/MFC{rnd}02','fresh round namespace')
   need(not m['retained_objects'] and m['native_round_phase_count']==47,'no retained project objects')
   launch=read(proposal/'launch.sh').decode();need(sha(raw) in launch and m['runner']['sha256'] in launch,'frozen launch pins')
   for row in m['inputs']:need(sha(read(row['path']))==row['sha256'],'actual input identity')
   materialized=json.loads(read(out/'materialized-inputs.json'));stamps=json.loads(read(out/'source-mtimes.json'));work=Path(m['work'])
   need(set(materialized)==set(m['repeat_inputs']),'only declared carrier inputs')
   for n,row in m['repeat_inputs'].items():
    current=read(work/n);need(sha(current)==row['sha256']==materialized[n]['sha256'] and len(current)==row['bytes'] and stamps[n]==row['mtime_ns'],'consumed source identity/time')
   need({n for n in materialized if Path(n).suffix.lower() in {'.obj','.lib','.exe','.map','.com'}}=={'clbase.lib','DIET.EXE'},'no prebuilt project or private CRT')
   if group==1:
    recipe=json.loads(read(m['source_recipe']['path']));need(recipe['archive_sha256']==archive_sha and recipe['object_graph']==graph,'source archive/graph regeneration')
    for n,b in files.items():need(b==read(work/n) and sha(b)==recipe['source_inventory'][n]['sha256'],'regenerated source '+n)
    for n,row in recipe['maintained_inputs'].items():need(sha((root/n).read_bytes())==row['sha256'],'maintained source binding '+n)
    identity={n:(r['sha256'],r['bytes'],r['mtime_ns']) for n,r in m['repeat_inputs'].items()}
    if first_inputs is None:first_inputs=identity
    else:need(identity==first_inputs,'identical round source bytes/timestamps')
   completion=json.loads(read(out/'completion.json'))
   need(completion['complete'] and completion['owned_lock_released'] and not completion['errors'] and completion['native_invocations']==len(m['phases']),'terminal clean group')
   need(m['accumulated_objects']==produced,'continuous producer receipts')
   if prior:need(m['predecessor']['sha256']==sha(read(prior/'completion.json')),'predecessor terminal binding')
   else:need(m['predecessor'] is None,'fresh first group')
   registry={n:q['sha256'] for n,q in m['registry_baseline'].items()}
   for phase in m['phases']:
    a=json.loads(read(out/(phase+'-started.json')));z=json.loads(read(out/(phase+'-finished.json')));transition=json.loads(read(out/(phase+'-registry-transition.json')))
    need(a['argv']==m['native_argv'][phase] and a['cwd']==str(root/work/m.get('phase_cwds',{}).get(phase,'.')),'actual native argv/cwd')
    need(a['wait_seconds']==90 and a['cleanup_seconds']==15,'native bound')
    need(z['exit_code']==(1 if phase in ['pack','restore'] else 0) and z['inventory_complete'] and z['initial_inventory_complete'] and not any(z[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']) and transition['ok'],'native result/cleanup/registry')
    before={n:read(out/(phase+'-before-'+n)) for n in ['user.reg','system.reg']};after={n:read(out/(phase+'-after-'+n)) for n in before}
    need({n:sha(b) for n,b in before.items()}==registry==json.loads(read(out/(phase+'-before-registry.json'))),'registry baseline continuity')
    registry={n:sha(b) for n,b in after.items()};need(registry==json.loads(read(out/(phase+'-after-registry.json'))),'registry after snapshot')
    recomputed=policy.validate_transition(before,after,phase_start_utc=a['started_utc'],phase_end_utc=transition['phase_end_utc'],child_tz='UTC')
    need(json.loads(json.dumps(recomputed))==transition,'registry transition recomputation')
    log=read(out/(phase+'.log'))
    if phase in ['pack','restore']:need(b'Success!' in log,'DIET success banner')
    names=[m['native_outputs'][phase]]+m.get('extra_outputs',{}).get(phase,[])
    receipt=json.loads(read(out/(phase+'-output.json')));need(sha(read(work/names[0]))==receipt['sha256'],'native producer receipt')
    if len(names)>1:rows=json.loads(read(out/(phase+'-all-outputs.json')))
    else:rows={names[0]:receipt}
    if phase=='link':rows['obj/th03/mainl.map']=json.loads(read(out/'link-map-output.json'))
    for n,row in rows.items():need(n not in produced and sha(read(work/n))==row['sha256'] and len(read(work/n))==row['bytes'],'fresh output identity');produced[n]=row
    count+=1
   need(registry=={n:q['sha256'] for n,q in json.loads(read(out/'next-registry-baseline.json')).items()},'next registry baseline')
   need(produced==json.loads(read(out/'accumulated-objects.json')),'exact accumulated products');prior=out
  need(len(produced)==940,'complete native product inventory')
  verifier=read(manifest['verifier']['path']);need(sha(verifier)==VERIFIER_SHA,'fixed final verifier')
  result=load(verifier,root/manifest['verifier']['path'],'fixed_fullcold_verifier').verify(root/manifest['work'],manifest)
  need(json.loads(json.dumps(result))==json.loads(read(prior/'linked-verification.json')) and result['diagnostic_checks_pass'],'recomputed fullcold final proof')
  need(result['build_output_count']==940 and result['packing']['canonical_packed_equal'] and result['packing']['raw_roundtrip_equal'],'cold packed product')
  if rnd==2:need(len(result['raw_repeat_pairs'])==940 and result['two_round_raw_repeat_equal'] and all(x['raw_equal'] for x in result['raw_repeat_pairs']),'all940 raw repeat pairs')
  reports.append(dict(round=rnd,exe_sha256=result['exe_sha256'],packing=result['packing'],products=940,raw_pairs=len(result['raw_repeat_pairs'])))
 need(count==94,'all94 native phase receipts')
 failed=Path('.analysis/mainl-fullcold-r1-g2-20261021-v01-output');negative=json.loads(read(failed/'completion.json'));extract=json.loads(read(failed/'extract-finished.json'))
 need(not negative['complete'] and negative['native_invocations']==2 and negative['owned_lock_released'] and any('FileNotFoundError' in x for x in negative['errors']),'preserved filename harness failure')
 need(extract['exit_code']==0 and extract['inventory_complete'] and not any(extract[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']),'preserved successful actual extraction')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_invocations_now=0,native_phases_replayed=count,groups_replayed=20,source_files_regenerated=1904,project_objects_per_round=36,authored_crt_objects_per_round=6,contextual_crt_members_per_round=893,raw_repeat_pairs=940,decoded_and_packed_equal=True,preserved_filename_harness_failure=True,rounds=reports,source_acceptance=False,source_progress_changed=False,exact_acceptance=False,default_backend=False,runtime_rerun=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/mainl_fullcold_current/proof.json').read_text());result=replay(a.repo_root,p,a.source_root);raw=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
