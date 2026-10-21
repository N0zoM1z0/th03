#!/usr/bin/env python3
"""Read-only source-bound registration/music compiler and link diagnostic."""
import argparse,hashlib,json,types
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='mainl-regmusic-backend-proof-v1','schema')
 need(not any(p[k] for k in ['source_acceptance','exact_acceptance','source_progress_changed','full_cold_build','runtime_rerun','fresh_product_repeat']),'credit inflation')
 need(p['native_phase_count']==3,'three integration phases')
 need(len(p['pins'])==len({r['path'] for r in p['pins']}),'duplicate pins')
def replay(root,p,source_root=None):
 validate_proof(p);root=root.resolve();pins={r['path']:r for r in p['pins']}
 def read(n):
  n=str(n);need(n in pins,'unbound '+n);q=root/n;need(q.is_file() and not q.is_symlink(),'regular bound file');b=q.read_bytes();r=pins[n];need(sha(b)==r['sha256'] and len(b)==r['bytes'],'pin drift '+n);return b
 for n in pins:read(n)
 maintained={};source_root=Path(source_root or root)
 for row in p['source_bindings']:
  q=source_root/row['path'];need(q.is_file() and not q.is_symlink(),'maintained source absent');b=q.read_bytes();need(sha(b)==row['sha256'] and len(b)==row['bytes'],'maintained source drift');maintained[row['path']]=b
 def module(raw,path,name):
  mod=types.ModuleType(name);mod.__file__=str(path);exec(compile(raw,str(path),'exec'),mod.__dict__);return mod
 c=module(maintained[p['composer_path']],source_root/p['composer_path'],'maintained_snow_composer')
 base=Path(p['baseline']);work=root/p['work'];out=Path(p['output']);proposal=Path(p['proposal'])
 generated=c.generate(read(base/'th03_mainl.asm'),read(base/'obj/th03/mainl.@l'),maintained[p['staff_path']],maintained[p['root_body_path']],maintained[p['cpp_path']])
 # Declared historical source transport only; never normalize compiler products.
 registration_crlf=maintained[p['registration_path']].replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
 need(registration_crlf==read(Path(p['work'])/'src/mainl/regist.cpp'),'maintained registration CRLF transport differs')
 for n,b in generated.items():need(b==read(Path(p['work'])/n),'maintained composition differs from consumed '+n)
 m=json.loads(read(proposal/'manifest.json'));need(read(out/'manifest.json')==read(proposal/'manifest.json'),'native manifest copy')
 need(m['work']==p['work'] and m['output']==p['output'] and m['phases']==['compile','root','link'],'native namespace/phases')
 launch=read(proposal/'launch.sh').decode();need(sha(read(proposal/'manifest.json')) in launch and m['runner']['sha256'] in launch,'launch binding')
 for row in m['inputs']:need(sha(read(row['path']))==row['sha256'],'native source pin')
 consumed=json.loads(read(out/'materialized-inputs.json'));stamps=json.loads(read(out/'source-mtimes.json'))
 for n,row in m['repeat_inputs'].items():
  need(sha(read(Path(p['work'])/n))==row['sha256']==consumed[n]['sha256'],'consumed source drift');need(stamps[n]==row['mtime_ns'],'input stamp')
 done=json.loads(read(out/'completion.json'))
 need(done['complete'] and not done['errors'] and done['native_invocations']==3 and done['owned_lock_released'],'successful native completion')
 for phase in m['phases']:
  a=json.loads(read(out/(phase+'-started.json')));z=json.loads(read(out/(phase+'-finished.json')));t=json.loads(read(out/(phase+'-registry-transition.json')))
  need(a['argv']==m['native_argv'][phase] and a['cwd']==str(work/m.get('phase_cwds',{}).get(phase,'.')),'actual argv/cwd')
  need(a['wait_seconds']==90 and a['cleanup_seconds']==15,'phase bound')
  need(z['exit_code']==0 and not any(z[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']) and z['inventory_complete'] and z['initial_inventory_complete'] and t['ok'],'native success/cleanup')
  read(out/(phase+'.log'))
  produced=json.loads(read(out/(phase+'-output.json')));product=read(Path(p['work'])/m['native_outputs'][phase])
  need(sha(product)==produced['sha256'] and len(product)==produced['bytes'],'phase producer/product tie')
  if phase=='link':
   mapped=json.loads(read(out/'link-map-output.json'));mapbytes=read(Path(p['work'])/'obj/th03/mainl.map')
   need(sha(mapbytes)==mapped['sha256'] and len(mapbytes)==mapped['bytes'],'link MAP producer/product tie')
 result=module(read(m['verifier']['path']),root/m['verifier']['path'],'regmusic_link_verifier').verify(work,m)
 need(json.loads(json.dumps(result))==json.loads(read(out/'linked-verification.json')) and result['diagnostic_checks_pass'],'actual diagnostic recomputation')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_phases_replayed=3,native_invocations_now=0,registration_source_transport='LF-to-CRLF',complete_target_program_equal=result['checks']['full_target_program_equal'],scoped_61_order_equal=result['checks']['scoped_61_order_equal'],snow_six_order_preserved=result['checks']['snow_six_order_preserved'],exe_sha256=result['exe_sha256'],global_ordered_difference_count=result['global_ordered_difference_count'],prior_ordered_difference_count=result['prior_ordered_difference_count'],source_acceptance=False,source_progress_changed=False,exact_acceptance=False,full_cold_build=False,runtime_rerun=False,fresh_product_repeat=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();r=replay(a.repo_root,json.loads((a.proof or a.repo_root/'config/mainl_regmusic_backend/proof.json').read_text()),a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
