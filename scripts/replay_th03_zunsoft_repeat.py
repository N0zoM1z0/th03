#!/usr/bin/env python3
"""Compose the original logo proof with its second cold build; no native/model runs."""
from pathlib import Path
import argparse,hashlib,json,os,sys,tempfile,types
FIRST='.analysis/zunsoft-native-proposal-20261021-v01'
REPEAT='.analysis/zunsoft-repeat-proposal-20261022-v01'
OUTPUT='.analysis/zunsoft-repeat-output-20261022-v01'
ORIGINAL_PROOF='config/zunsoft_root/proof.json'
ORIGINAL_REPLAY='scripts/replay_th03_zunsoft_root.py'
RUNTIME='.analysis/zunsoft-native-20261021-v02/parent-runtime-verification.json'
MANIFESTS=['a1eead9202ec501fc79c9eac7aca25507bd8426ba9c55af3c28dee3844ad2796','e1805fa1c8ba50b30f97410b871201120657886fc3952ad46beb77926696b559']
FLAGS=('exact_acceptance','whole_payload_ownership','launcher_ownership','runtime_rerun','packing_run','real_device_runtime')
HELPERS={'scripts/lib/__init__.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/zun.py','scripts/review_th03_zunsoft.py','scripts/stage_th03_zunsoft.py',ORIGINAL_REPLAY}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def regular(root,name):
 p=Path(name);need(not p.is_absolute() and '..' not in p.parts,'unsafe relative path');p=root/p;need(p.is_file() and not any(q.is_symlink() for q in (p,*p.parents)),'regular input '+name);return p

def validate_proof(p):
 need(p['schema']=='th03-zunsoft-repeat-proof-v1','schema')
 need(p['manifest_sha256s']==MANIFESTS and p['two_cold_builds'] is True,'two original frozen manifests')
 need((p['root_procedures'],p['root_code_bytes'],p['root_data_bytes'],p['root_bss_bytes'],p['native_phases'],p['runtime_images'],p['retained_runtime_calls'],p['modeled_candidates'])==(10,1299,15,293,4,2,2600,1),'bounded counts')
 need(all(p[k] is False for k in FLAGS),'credit inflation')
 need(p['original_proof_sha256']=='cfca06c722642d62b32bb0930a42d49dce8b02a4ab3d6878902174f812bdb877','preserved one-build proof')
 need(p['repeat_verifier_sha256']=='e30a969dd641ca9b311dd769959072720830459c1ce94757cce1df721b1b9fde','fixed raw verifier')
 need(p['raw_repeat_sha256']=='edded51b2d7b1d00fa70aad843e55f10c160ca9c78105372e4c0f7debc067a9b' and p['structural_sha256']=='f7289e290dd9e57d407239b7e481b875dbf96876af2c673b82b71374fe9d5aef','parent verification records')
 need(set(p['helper_closure'])==HELPERS and len(p['maintained_sources'])==6,'source/helper closure')
def validate_inventory(inv,p):
 need(inv['metadata']=={k:v for k,v in p.items() if k!='inventory'},'inventory metadata binding')
 pins=inv['pins'];need(len(pins)==len({q['path'] for q in pins}),'duplicate inventory path')
 need(inv['inputs']=={q['path']:{k:q[k] for k in ['sha256','bytes']} for q in pins},'cleanup retention mirror')
def validate_pair(r):
 need(r['checks_pass'] is True and (r['independent_cold_builds'],r['native_phases_observed'],r['retained_runtime_calls'],r['native_invocations_now'])==(2,4,2600,0),'actual cold pair counts')
 need(all(r[k] is False for k in ['runtime_rerun','exact_acceptance','whole_payload_ownership','launcher_ownership','packing_proven','real_device_runtime']),'pair scope')
 need(r['source_files']==21 and r['source_bytes_modes_mtimes_identical'] is True and r['tool_mtimes_identical'] is True and r['project_objects_reused']==0,'cold source identity')
 expected={'obj/th01/zunsoft.obj':(4133,'845de18164def1d384eadc59be287a22ca47b99a6d4d989c0dfa407c094a08a5'),'bin/th01/zunsoft.com':(10096,'beeb86dc055c585a32f4500c9eabb2e6cb1e0537bcdbc5f3763ebefa4308e297'),'obj/th01/zunsoft.map':(28657,'882ac7e3fba775f9225aa55adc276e17604620fa2e7608ae7cc18aa9081bc3ed')}
 need(set(r['raw_products'])==set(expected),'raw product inventory')
 for name,(size,digest) in expected.items():need(r['raw_products'][name]==dict(raw_equal=True,bytes=size,sha256=digest),'complete raw product '+name)
def replay(root,p,source_root=None):
 root=Path(root).resolve();source_root=Path(source_root or root).resolve();validate_proof(p)
 q=p['inventory'];raw=regular(root,q['path']).read_bytes();need(sha(raw)==q['sha256'] and len(raw)==q['bytes'],'inventory identity');inv=json.loads(raw);validate_inventory(inv,p);pins={q['path']:q for q in inv['pins']}
 def read(name):
  need(name in pins,'unbound '+name);b=regular(root,name).read_bytes();q=pins[name];need(sha(b)==q['sha256'] and len(b)==q['bytes'],'input drift '+name);return b
 def js(name):return json.loads(read(name))
 def load(name,path):
  mod=types.ModuleType(name);mod.__file__=str(root/path);sys.modules[name]=mod;exec(compile(read(path),mod.__file__,'exec'),mod.__dict__);return mod
 for name in pins:read(name)
 original=js(ORIGINAL_PROOF);need(sha(read(ORIGINAL_PROOF))==p['original_proof_sha256'] and original['two_cold_builds'] is False and original['native_phases']==2,'original record remains one build')
 manifests=[js(path+'/manifest.json') for path in [FIRST,REPEAT]]
 for path,digest in zip([FIRST,REPEAT],MANIFESTS):need(sha(read(path+'/manifest.json'))==digest,'frozen native manifest')
 # Bind only the audited import/build closure, never every historical tracked file.
 # This intentionally survives later unrelated docs/ledger/README updates.
 for name,q in p['helper_closure'].items():
  need(sha(read(name))==q['sha256'] and len(read(name))==q['bytes'],'helper identity '+name)
  need(all(manifests[1]['sources'][name][k]==q[k] for k in ['sha256','bytes']),'helper binding to actual second native snapshot '+name)
 need(p['maintained_sources']==original['maintained_sources'],'original maintained source closure')
 for name,q in p['maintained_sources'].items():
  b=regular(source_root,name).read_bytes();need(sha(b)==q['sha256'] and len(b)==q['bytes'],'maintained source identity '+name)
  for m in manifests:need(b==read(m['work']+'/'+name),'both consumed maintained sources '+name)
 prior=load('zunsoft_original_repeat_composition',ORIGINAL_REPLAY).replay(root,original,source_root)
 need(prior['pass_checks'] and prior['native_invocations_now']==0 and prior['retained_runtime_calls']==2600 and prior['two_cold_builds'] is False,'guarded original replay')
 oldcwd=Path.cwd();oldargv=sys.argv[:];oldpath=sys.path[:]
 try:
  os.chdir(root);verifier=load('zunsoft_raw_repeat_composition',REPEAT+'/verify_repeat.py');need(sha(read(REPEAT+'/verify_repeat.py'))==p['repeat_verifier_sha256'],'raw verifier identity')
  with tempfile.TemporaryDirectory(prefix='zunsoft-repeat-replay-',dir=root/'.analysis') as tmp:
   path=Path(tmp)/'pair.json';sys.argv=[REPEAT+'/verify_repeat.py','--proposal',REPEAT,'--manifest-sha256',MANIFESTS[1],'--output',str(path)];verifier.main();pair=json.loads(path.read_text())
 finally:os.chdir(oldcwd);sys.argv=oldargv;sys.path[:]=oldpath
 stored=js(OUTPUT+'/raw-repeat-verification.json');need(sha(read(OUTPUT+'/raw-repeat-verification.json'))==p['raw_repeat_sha256'] and pair==stored,'recomputed exact raw pair report');validate_pair(pair)
 structural=js(OUTPUT+'/structural-verification.json');runtime=js(RUNTIME)
 need(sha(read(OUTPUT+'/structural-verification.json'))==p['structural_sha256'],'second structural record')
 need(structural['diagnostic_checks_pass'] is True and len(structural['checks'])==14 and all(v is True for v in structural['checks'].values()),'second structural gates')
 need((structural['runtime'],structural['runtime_image_count'],structural['runtime_calls_per_image'],structural['runtime_total_calls'])==(None,0,0,0),'no new model execution')
 need(structural['source_binding_manifest_sha256']==MANIFESTS[1],'second structural source binding')
 omit={'inputs','checks','source_binding_manifest_sha256','runtime','runtime_image_count','runtime_calls_per_image','runtime_total_calls'}
 need({k:v for k,v in structural.items() if k not in omit}=={k:v for k,v in runtime.items() if k not in omit},'same verified layout and bytes as original modeled image')
 need(structural['checks']=={k:v for k,v in runtime['checks'].items() if k!='bounded_runtime_matrix'},'same fourteen structural gates')
 for name in pins:read(name)
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),source_binding=True,root_procedures=10,root_code_bytes=1299,root_data_bytes=15,root_bss_bytes=293,native_phases_replayed=4,two_cold_builds=True,raw_pair=['OBJ','COM','MAP'],whole_com_diagnostic_equal=True,retained_runtime_calls=2600,modeled_candidates=1,repeat_candidate_runtime_inferred_from_raw_identity=True,native_invocations_now=0,**{k:False for k in FLAGS})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--source-root',type=Path);ap.add_argument('--proof',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=json.loads((a.proof or a.repo_root/'config/zunsoft_repeat/proof.json').read_text());result=replay(a.repo_root,p,a.source_root);raw=json.dumps(result,indent=2)+'\n'
 if a.output:
  with a.output.open('x') as f:f.write(raw)
 print(raw)
if __name__=='__main__':main()
