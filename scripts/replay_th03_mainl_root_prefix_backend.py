#!/usr/bin/env python3
"""Read-only source-bound 1081-byte compiler/root/link diagnostic."""
import argparse,hashlib,json,types
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='mainl-root-prefix-backend-proof-v1','schema')
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
 composition=json.loads(read(proposal/'composition.json'))
 for n in ['src/mainl/linked_game/cfg_resident.cpp','src/mainl/linked_game/win.cpp']:
  need(maintained[n].replace(b'\n',b'\r\n')==read(Path(p['work'])/n),'declared include LF-to-CRLF source transport')
 args=[read(p['composition_inputs'][n]) for n in ['root','response','root_body']]+[maintained[p['cpp_path']]]
 generated=c.generate(*args)
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
 original=json.loads(read(p['compiler_probe_report']))
 need(original['diagnostic_checks_pass'] and original['hypothesis_checks_pass'] and original['candidate_code_bytes']==1081 and original['ordered_far_sites_equal'],'successful original compiler proof')
 need(sha(read(p['compiler_probe_object']))==original['object_sha256'],'compiler object tie')
 need(original['blocks']==result['root_prefix_compiler']['blocks']==[dict(offset=0,size=1019,far_count=43),dict(offset=1019,size=62,far_count=5)],'actual natural records')
 failed=json.loads(read(p['failed_compiler_report']))
 need(failed['diagnostic_checks_pass'] and not failed['hypothesis_checks_pass'] and failed['candidate_code_bytes']==1077,'preserved failed1077 hypothesis')
 need(sha(read(p['failed_compiler_object']))==failed['object_sha256'],'failed compiler object tie')
 old_cpp=read(p['failed_compiler_source']);new_cpp=maintained[p['cpp_path']]
 need(old_cpp.replace(b' if((resident->game_mode != GM_STORY) || (resident->pid_winner != 0)) {',b' if(resident->game_mode != GM_STORY) {\n  return 1;\n }\n if(resident->pid_winner != 0) {')==new_cpp,'sole equivalent early-return correction')
 failout=Path(p['failed_link_output']);fc=json.loads(read(failout/'completion.json'));fz=json.loads(read(failout/'link-finished.json'))
 need(not fc['complete'] and fc['native_invocations']==3 and fc['owned_lock_released'] and fz['exit_code']==1 and not any(fz[k] for k in ['timeout','cleanup_uncertain','poison','survivors']),'preserved link failure')
 need(b'Undefined symbol cdg_free_all' in read(failout/'link.log'),'actual link failure cause')
 for n in ['th03_mainl.asm','src/mainl/root/root.asm']:
  before=read(Path(p['failed_work'])/n);after=read(Path(p['work'])/n)
  need(before.replace(b'cdg_free_all',b'CDG_FREE_ALL')==after,'exact external spelling correction')
 for n in ['rootpre.cpp','obj/th03/mainl.@l']:
  need(read(Path(p['failed_work'])/n)==read(Path(p['work'])/n),'unaffected source identical')
 need(result['prior_ordered_difference_count']==134 and result['global_ordered_difference_count']==102,'actual measured global order')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_phases_replayed=3,native_invocations_now=0,complete_target_program_equal=True,prefix1081_literal48_equal=result['checks']['root_prefix_literal48'],suffix149_through676_preserved=result['checks']['literal_suffix_preserved'],staff_mixed107_preserved=result['checks']['staff_mixed107_equal'],registration71_preserved=result['checks']['mixed_71_order_preserved'],continue20_preserved=result['checks']['continue_literal20'],all_prior_publics_preserved=result['checks']['prior_public_addresses_preserved'],failed1077_and_link_attempts_preserved=True,boundary_verifier_correction_preserved=True,include_source_transport_only=True,global_ordered_difference_count=102,prior_ordered_difference_count=134,exe_sha256=result['exe_sha256'],source_acceptance=False,source_progress_changed=False,exact_acceptance=False,full_cold_build=False,runtime_rerun=False,fresh_product_repeat=False)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();r=replay(a.repo_root,json.loads((a.proof or a.repo_root/'config/mainl_root_prefix_backend/proof.json').read_text()),a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
