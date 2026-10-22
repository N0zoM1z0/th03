#!/usr/bin/env python3
"""Offline two-cold resident source proof. No compiler, Wine, or runtime execution."""
from pathlib import Path
import argparse,hashlib,json,sys,types
BASE='.analysis/zun-resident-maintained-proposal-v01'
FIRST='.analysis/zun-resident-native-proposal-v01'
CORRECTED='.analysis/zun-resident-native-proposal-v02'
MANIFEST_SHAS=['86460dfdc3555f4ee84dffaff5864f086e2256ba701134854aa96e36699d20b4','d207d2120cc087efddee15f7e7dee893289621d96e1d188cfde1a858fc764461']
CREDIT_FLAGS=['exact_acceptance','whole_payload_ownership','launcher_ownership','runtime_rerun']
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(value,message):
 if not value:raise ValueError(message)
def validate_proof(p):
 need(p['schema']=='th03-zun-resident-source-proof-v1','proof schema')
 need(all(p[n] is False for n in CREDIT_FLAGS),'credit inflation')
 need(p['two_cold_builds'] is True and p['manifest_sha256s']==MANIFEST_SHAS,'two frozen recipes')
 need((p['native_phases'],p['root_procedures'],p['root_code_bytes'],p['root_data_bytes'],p['root_bss_bytes'],p['runtime_images'],p['runtime_calls'])==(4,2,322,307,0,2,40),'bounded counts')
 need(len(p['maintained_sources'])==10 and len(p['pins'])==len({q['path'] for q in p['pins']}),'source closure and unique pins')
 need(set(p['helper_closure'])=={'scripts/lib/__init__.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/zun.py','scripts/review_th03_zun_resident.py'},'audited local helper closure')
def validate_runtime(r):
 need(r['diagnostic_checks_pass'] is True and all(v is True for v in r['checks'].values()) and len(r['checks'])==21,'retained runtime gates')
 need((r['runtime_image_count'],r['runtime_calls_per_image'],r['runtime_total_calls'])==(2,20,40),'target and first candidate only')
 need(all(r[n] is False for n in ['source_acceptance','exact_acceptance','whole_payload_ownership','launcher_ownership','historical_cache_used']),'runtime scope')
 need(len(r['runtime']['target'])==len(r['runtime']['current'])==20 and r['runtime']['target']==r['runtime']['current'],'retained actual modeled rows')
 for row in r['runtime']['current']:
  need(row['preserved']=={'SI':0xabba,'DI':0xcdda,'BP':0x1234,'DS':0x2000,'SP':0xff02},'modeled ABI preservation')
def replay(root,p,source_root=None):
 root=Path(root).resolve();source_root=Path(source_root or root).resolve();validate_proof(p)
 if 'inventory' in p:
  q=p['inventory'];f=root/q['path'];need(p['pins']==[q] and not any(x.is_symlink() for x in (f,*f.parents)),'compact inventory binding');raw=f.read_bytes();need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'inventory identity');expanded=json.loads(raw)
  need({k:v for k,v in p.items() if k not in ['pins','inventory']}=={k:v for k,v in expanded.items() if k!='pins'},'compact metadata differs');p=expanded;validate_proof(p)
 pins={q['path']:q for q in p['pins']}
 def read(n):
  need(n in pins,'unbound '+n);f=root/n;need(not any(x.is_symlink() for x in (f,*f.parents)) and f.is_file(),'regular input '+n);raw=f.read_bytes();q=pins[n];need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'input drift '+n);return raw
 for n in pins:read(n)
 def load(name,path):
  raw=read(path);module=types.ModuleType(name);module.__file__=str(root/path);sys.modules[name]=module;exec(compile(raw,module.__file__,'exec'),module.__dict__);return module
 m=json.loads(read(FIRST+'/manifest.json'));need(sha(read(FIRST+'/manifest.json'))==MANIFEST_SHAS[0],'original manifest')
 for n,q in p['helper_closure'].items():need(q==m['sources'][n] and sha(read(n))==q['sha256'],'helper pre-import native binding '+n)
 # Only the maintained source overlay may be supplied separately for pre-install checks.
 # Helpers, target, artifacts, and all native evidence always come from the real repository root.
 f=source_root/'scripts/stage_th03_zun_resident.py';need(not any(x.is_symlink() for x in (f,*f.parents)),'regular stage');raw=f.read_bytes();need(sha(raw)==p['stage_sha256'],'maintained stage identity')
 stage=types.ModuleType('resident_maintained_stage');stage.__file__=str(f);exec(compile(raw,str(f),'exec'),stage.__dict__)
 plan,data=stage.read_inputs(source_root,source_root/'config/zun_resident/source.json');need(set(data)==set(p['maintained_sources']),'complete maintained closure')
 for n,q in p['maintained_sources'].items():need(sha(data[n])==q['sha256'] and len(data[n])==q['bytes'] and data[n]==read(m['work']+'/'+n),'maintained-to-consumed source '+n)
 need(read(m['work']+'/th03/res_yume.cpp')==b'#include "src/zun/res_yume.cpp"\n','root forwarding slot')
 need(sha(read(BASE+'/pair.py'))==p['pair_verifier_sha256'] and sha(read(BASE+'/structural.py'))==p['structural_verifier_sha256'],'new replay helper identities')
 pair=load('resident_pair_replay',BASE+'/pair.py').verify(root);stored_pair=json.loads(read(BASE+'/pair-v02.json'));need(pair==stored_pair and pair['pass_checks'] is True,'recomputed cold pair')
 structural=load('resident_structure_replay',BASE+'/structural.py').verify(root);stored=json.loads(read(BASE+'/structural-v02.json'));need(structural==stored and structural['diagnostic_checks_pass'] is True,'recomputed structure')
 original=json.loads(read(CORRECTED+'/structural.json'));omit={'inputs','verifier_sha256'}
 need({k:v for k,v in structural.items() if k not in omit}=={k:v for k,v in original.items() if k not in omit},'corrected original structural lineage')
 failure=json.loads(read(FIRST+'/structural.json'));need(failure['diagnostic_checks_pass'] is False and [n for n,v in failure['checks'].items() if v is not True]==['complete_root_import_vector'],'original failed verifier preserved')
 runtime=json.loads(read(CORRECTED+'/runtime.json'));validate_runtime(runtime)
 omit={'inputs','runtime','runtime_image_count','runtime_calls_per_image','runtime_total_calls','checks'}
 need({k:v for k,v in runtime.items() if k not in omit}=={k:v for k,v in original.items() if k not in omit},'runtime first candidate binding')
 need({k:v for k,v in runtime['checks'].items() if k!='bounded_runtime_matrix'}==original['checks'],'runtime structural binding')
 need(runtime['completion_sha256']==sha(read(m['output']+'/completion.json')),'unchanged pre-runtime completion binding')
 dependencies=structural['omf']['dependency_paths'];need(dependencies[:2]==['th03/res_yume.cpp','src/zun/res_yume.cpp'],'maintained OMF source lineage')
 for n in set(dependencies):
  if n.startswith('C:\\TC4\\INCLUDE\\'):
   vendor='.analysis/toolchain/wineprefix/drive_c/'+n[3:].replace('\\','/');matches=[q for q in m['inputs'] if q['path'].lower()==vendor.lower()];need(len(matches)==1 and sha(read(matches[0]['path']))==matches[0]['sha256'],'OMF vendor declaration '+n)
  else:need(n in m['repeat_inputs'] and read(m['work']+'/'+n)==read(m['repeat_inputs'][n]['path']),'OMF declared source '+n)
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),source_binding=True,root_code_bytes=322,root_data_bytes=307,root_bss_bytes=0,root_procedures=2,native_phases_replayed=4,two_cold_builds=True,raw_pair=['OBJ','COM','MAP'],whole_com_diagnostic_equal=True,retained_runtime_calls=40,modeled_candidates=1,repeat_candidate_runtime_inferred_from_raw_identity=True,native_invocations_now=0,**{n:False for n in CREDIT_FLAGS})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--source-root',type=Path);ap.add_argument('--proof',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/zun_resident/proof.json').read_text());result=replay(a.repo_root,p,a.source_root);raw=json.dumps(result,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
