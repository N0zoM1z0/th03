#!/usr/bin/env python3
"""Read-only source-bound 2458 CODE +112 DATA compiler/prefix/root/link diagnostic."""
import argparse,hashlib,json,types
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def validate_proof(p):
 need(p['schema']=='mainl-root-complete-data-backend-proof-v1','schema')
 need(not any(p[k] for k in ['source_acceptance','exact_acceptance','source_progress_changed','full_cold_build','runtime_rerun','fresh_product_repeat','default_backend','packed_acceptance']),'credit inflation')
 need(p['native_phase_count']==4,'four integration phases')
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
 generated=c.generate(*args,read(p['composition_inputs']['rootpre']))
 for n,b in generated.items():need(b==read(Path(p['work'])/n),'maintained composition differs from consumed '+n)
 m=json.loads(read(proposal/'manifest.json'));need(read(out/'manifest.json')==read(proposal/'manifest.json'),'native manifest copy')
 need(m['work']==p['work'] and m['output']==p['output'] and m['phases']==['compile','prefix','root','link'],'native namespace/phases')
 launch=read(proposal/'launch.sh').decode();need(sha(read(proposal/'manifest.json')) in launch and m['runner']['sha256'] in launch,'launch binding')
 for row in m['inputs']:need(sha(read(row['path']))==row['sha256'],'native source pin')
 consumed=json.loads(read(out/'materialized-inputs.json'));stamps=json.loads(read(out/'source-mtimes.json'))
 for n,row in m['repeat_inputs'].items():
  need(sha(read(Path(p['work'])/n))==row['sha256']==consumed[n]['sha256'],'consumed source drift');need(stamps[n]==row['mtime_ns'],'input stamp')
 done=json.loads(read(out/'completion.json'))
 need(done['complete'] and not done['errors'] and done['native_invocations']==4 and done['owned_lock_released'],'successful native completion')
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
 for version,phase,count,diagnostic in [('01','compile',1,'hfliplut.h'),('02','link',4,'_mainl_op_name')]:
  negative=Path('.analysis/mainl-root-complete-data-link-output-20261021-v'+version)
  nd=json.loads(read(negative/'completion.json'));nf=json.loads(read(negative/(phase+'-finished.json')))
  need(not nd['complete'] and nd['native_invocations']==count and nd['owned_lock_released'] and nd['errors'],'preserved negative completion')
  need(nf['exit_code']!=0 and nf['inventory_complete'] and not any(nf[k] for k in ['timeout','cleanup_uncertain','poison','survivors']),'preserved negative clean shutdown')
  need(diagnostic in read(negative/(phase+'.log')).decode(errors='replace'),'preserved actual failure')
 original=json.loads(read(p['compiler_probe_report']))
 need(original['diagnostic_checks_pass'] and original['hypothesis_checks_pass'] and original['candidate_code_bytes']==2458 and original['actual_cfg_branch_destination_gate'],'successful original compiler proof')
 need(sha(read(p['compiler_probe_object']))==original['object_sha256'],'compiler object tie')
 need(original['blocks']==result['root_prefix_compiler']['blocks']==[dict(offset=0,size=1019,far_count=43),dict(offset=1019,size=1023,far_count=53),dict(offset=2042,size=416,far_count=15)],'actual natural records')
 probeout=Path(p['compiler_probe_output']);pm=json.loads(read(probeout/'manifest.json'));pc=json.loads(read(probeout/'completion.json'));pz=json.loads(read(probeout/'compile-finished.json'));pa=json.loads(read(probeout/'compile-started.json'))
 need(pc['complete'] and pc['native_invocations']==1 and pc['owned_lock_released'] and not pc['errors'],'original compiler completion')
 need(pz['exit_code']==0 and pz['inventory_complete'] and not any(pz[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']),'original compile cleanup')
 need(pa['argv']==pm['native_argv']['compile'] and pa['cwd']==str(root/pm['work']) and pa['wait_seconds']==90 and pa['cleanup_seconds']==15,'original compile invocation')
 produced=json.loads(read(probeout/'compile-output.json'));raw=read(p['compiler_probe_object']);need(produced['sha256']==sha(raw) and produced['bytes']==len(raw),'original compile producer/product tie')
 need(maintained[p['cpp_path']]==read(Path(p['work'])/'rootdata.cpp'),'identical maintained compiler source')
 for row in pm['inputs']:need(sha(read(row['path']))==row['sha256'],'original compile input pin')
 need(result['prior_ordered_difference_count']==102 and result['global_ordered_difference_count']==0,'actual measured global order')
 need(read(Path(p['work'])/'bin/th03/mainl.exe')==read(m['target']['path']),'entire decoded target EXE equality')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_phases_replayed=4,native_invocations_now=0,complete_target_program_equal=True,decoded_target_file_equal=True,complete2458_literal111_equal=result['checks']['root_prefix_literal111'],suffix149_through676_preserved=result['checks']['literal_suffix_preserved'],staff_mixed107_preserved=result['checks']['staff_mixed107_equal'],registration71_preserved=result['checks']['mixed_71_order_preserved'],continue20_preserved=result['checks']['continue_literal20'],all_other_prior_publics_preserved=result['checks']['prior_public_addresses_preserved'],finite_public_views_preserved=result['checks']['finite_public_views'],data28_literal_equal=result['checks']['root_data_literal28'],mixed139_literal_equal=result['checks']['root_mixed_literal139'],include_source_transport_only=True,global_ordered_difference_count=0,prior_ordered_difference_count=102,exe_sha256=result['exe_sha256'],source_acceptance=False,source_progress_changed=False,exact_acceptance=False,full_cold_build=False,runtime_rerun=False,fresh_product_repeat=False,default_backend=False,packed_acceptance=False,negative_cases_preserved=2)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();r=replay(a.repo_root,json.loads((a.proof or a.repo_root/'config/mainl_root_complete_data_backend/proof.json').read_text()),a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
