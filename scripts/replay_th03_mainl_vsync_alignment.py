#!/usr/bin/env python3
"""Read-only bound historical alignment, native repeat and packing replay."""
import argparse,hashlib,json,types
from pathlib import Path
def sha(raw):return hashlib.sha256(raw).hexdigest()
def need(ok,message):
 if not ok:raise ValueError(message)
def load_json(p):return json.loads(p.read_text())
def validate_proof(p):
 need(p['schema']=='mainl-vsync-alignment-proof-v1','schema')
 need(not any(p[k] for k in ['source_acceptance','exact_acceptance','source_progress_changed','full_cold_build','runtime_rerun']),'credit inflation')
 need([r['label'] for r in p['runs']]==['alignment','repeat','packing'],'distinct stages required')
 need(len(p['pins'])==len({r['path'] for r in p['pins']}),'duplicate pins')
 need(p['native_phase_count']==11,'four plus two plus five native phases')
def replay(root,p,source_root=None):
 validate_proof(p);root=root.resolve();pins={r['path']:r for r in p['pins']}
 def read(n):
  n=str(n);need(n in pins,'unbound input '+n);q=root/n;need(q.is_file() and not q.is_symlink(),'regular bound input');b=q.read_bytes();r=pins[n];need(len(b)==r['bytes'] and sha(b)==r['sha256'],'pin drift '+n);return b
 for n in pins:read(n)
 source_root=Path(source_root or root);maintained={}
 for row in p['source_bindings']:
  q=source_root/row['path'];need(q.is_file() and not q.is_symlink(),'maintained source absent')
  raw=q.read_bytes();need(sha(raw)==row['sha256'] and len(raw)==row['bytes'],'maintained source drift '+row['path']);maintained[row['path']]=raw
 composer_path='scripts/lib/mainl_vsync_alignment_source.py';c=types.ModuleType('current_alignment_composer');c.__file__=str(source_root/composer_path);exec(compile(maintained[composer_path],c.__file__,'exec'),c.__dict__)
 base=Path(p['composition_input_root']);generated=c.compose(read(base/'th03_mainl.asm'),read(base/'libs/master.lib/vs[data].asm'),maintained[c.SOURCE],read(base/'th03/formats/cdg[data].asm'),maintained[c.CDG_SOURCE])
 first=Path(p['runs'][0]['work'])
 for name,raw in generated.items():need(raw==read(first/name),'current maintained composition differs from actual consumed source '+name)
 def module(row,name):
  b=read(row['path']);need(sha(b)==row['sha256'],'module pin');v=types.ModuleType(name);v.__file__=str(root/row['path']);exec(compile(b,v.__file__,'exec'),v.__dict__);return v
 results={};count=0
 for run in p['runs']:
  out=Path(run['output']);proposal=Path(run['proposal']);work=root/run['work'];m=json.loads(read(proposal/'manifest.json'))
  need(read(out/'manifest.json')==read(proposal/'manifest.json'),'native manifest')
  need(m['work']==run['work'] and m['output']==run['output'],'native namespace')
  launch=read(proposal/'launch.sh').decode();need(sha(read(proposal/'manifest.json')) in launch and m['runner']['sha256'] in launch,'launch binding')
  done=json.loads(read(out/'completion.json'))
  need(done['complete'] and done['owned_lock_released'] and not done['errors'] and done['native_invocations']==len(m['phases']),'native completion')
  need(not done['exact_acceptance'] and not done['full_historical_replay'],'native acceptance inflation')
  for r in m['inputs']:need(sha(read(r['path']))==r['sha256'],'native input pin')
  consumed=json.loads(read(out/'materialized-inputs.json'));stamps=json.loads(read(out/'source-mtimes.json'))
  for name,row in m['repeat_inputs'].items():
   b=read(Path(run['work'])/name);need(sha(b)==row['sha256']==consumed[name]['sha256'],'consumed input differs');need(stamps[name]==row['mtime_ns'],'observed source stamp')
  v=module(m['verifier'],'bound_alignment_'+run['label'])
  for phase in m['phases']:
   start=json.loads(read(out/(phase+'-started.json')));finished=json.loads(read(out/(phase+'-finished.json')));transition=json.loads(read(out/(phase+'-registry-transition.json')));log=read(out/(phase+'.log'))
   need(start['argv']==m['native_argv'][phase] and start['cwd']==str(work/m.get('phase_cwds',{}).get(phase,'.')),'actual argv/cwd')
   need(start['wait_seconds']==90 and start['cleanup_seconds']==15,'native bound')
   expected=1 if run['label']=='packing' and phase!='selfcheck' else 0
   need(finished['exit_code']==expected,'native exit convention')
   need(not any(finished[k] for k in ['timeout','cleanup_uncertain','poison','survivors','errors']) and finished['inventory_complete'] and finished['initial_inventory_complete'],'native cleanup')
   need(transition['ok'],'registry transition')
   if run['label']=='packing':
    actual=v.check_phase(work,m,phase,finished,log);need(actual==json.loads(read(out/(phase+'-semantic-check.json'))) and actual['pass'],'packing phase replay')
   elif phase.startswith('ordinary_'):
    actual=v.verify_fixture(work,phase);need(actual==json.loads(read(out/(phase+'-verification.json'))) and actual['pass'],'fixture coverage replay')
   count+=1
  result=v.verify(work,m);receipt='calibration-verification.json' if run['label']=='packing' else 'linked-verification.json'
  need(result==json.loads(read(out/receipt)) and result['diagnostic_checks_pass'],'fresh diagnostic recomputation')
  need(not result['source_progress_changed'] and not result['exact_acceptance'] and not result['full_cold_build'],'result scope inflation')
  results[run['label']]=result
 a,r,d=(results[n] for n in ('alignment','repeat','packing'))
 need(all(x['raw_equal'] for x in r['raw_repeat_pairs']) and len(r['raw_repeat_pairs'])==3,'three raw repeat products')
 need(a['exe_sha256']==r['exe_sha256']==d['decoded_sha256'],'packing input bridge')
 need(a['checks']['target_program_equal'] and r['checks']['target_program_equal'] and not d['source_decoded_program_differences'],'complete target program equality')
 need(d['raw_repeat_equal'] and d['first_roundtrip_equal'] and d['second_roundtrip_equal'] and d['restoration_is_same_tool_separate_invocation'],'packing roundtrip')
 need(not d['target_fed'] and d['source_fed'],'source input role')
 need(count==11,'native stage count')
 return dict(schema=p['schema'],pass_checks=True,pinned_files=len(pins),native_phases_replayed=count,native_invocations_now=0,complete_target_program_equal=True,raw_root_exe_map_repeat=True,exe_sha256=r['exe_sha256'],packed_sha256=d['packed_first_sha256'],packed_bytes=d['packed_first_bytes'],packed_difference_count=d['packed_difference_count'],canonical_packed_equal=d['canonical_packed_equal'],ordered_relocation_difference_count=r['global_ordered_difference_count'],full_cold_build=False,runtime_rerun=False,source_acceptance=False,source_progress_changed=False,exact_acceptance=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--proof',type=Path);ap.add_argument('--source-root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();p=a.proof or a.repo_root/'config/mainl_vsync_alignment/proof.json';r=replay(a.repo_root,load_json(p),a.source_root);raw=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw)
 print(raw)
if __name__=='__main__':main()
